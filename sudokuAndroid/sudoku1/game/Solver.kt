package com.example.sudoku1.game

//as input goes 2 dim list with info about value and if this cell is constant or not
fun solveGrid(gridToSolve:MutableList<MutableList<Int>>): MutableList<Int>{ // output is one dim list
    var howManySteps = 0 // for efficiency purposes only
    val arrNumDict: MutableMap<Int, MutableList<Int>> = elimination2Dim(gridToSolve)
    val listWithKeys:MutableList<Int> = emptyIndexesGet(gridToSolve)
    var goodNums = 0
    while(goodNums < listWithKeys.size){
        var cantInsert = false
        var currentIndex = listWithKeys[goodNums]
        val lastIndex = arrNumDict.getValue(currentIndex).size - 1

        if(arrNumDict.getValue(currentIndex)[lastIndex] == lastIndex){
            howManySteps +=1
            arrNumDict.getValue(currentIndex)[lastIndex] = 0
            currentIndex = listWithKeys[goodNums-1]
            gridToSolve[currentIndex][0] = 0
            goodNums -= 1
        }else{
            howManySteps += 1
            val curRowIndex = currentIndex/9
            val curColIndex = currentIndex % 9
            var valuesFromInsert2Func = insertTry2(currentIndex, curRowIndex, curColIndex, gridToSolve, arrNumDict)
            var allOk = valuesFromInsert2Func[0]
            var numberToInsert = valuesFromInsert2Func[1]

            while(allOk != 1){//try to insert every number which is still possible
                howManySteps += 1
                if(arrNumDict.getValue(currentIndex)[lastIndex] < lastIndex){
                    valuesFromInsert2Func = insertTry2(currentIndex, curRowIndex, curColIndex, gridToSolve, arrNumDict)
                    allOk = valuesFromInsert2Func[0]
                    numberToInsert = valuesFromInsert2Func[1]
                }
                else if(arrNumDict.getValue(currentIndex)[lastIndex] == lastIndex){
                    arrNumDict.getValue(currentIndex)[lastIndex] = 0
                    currentIndex = listWithKeys[goodNums-1]
                    gridToSolve[currentIndex][0] = 0
                    goodNums -= 2
                    cantInsert = true
                    break
                }
            }//second while

            if(!cantInsert) gridToSolve[currentIndex][0] = numberToInsert
            goodNums += 1

        }//main else
    } // main while

    //change current output to one dim output
    val oneDimSolvedArr: MutableList<Int> = mutableListOf()
    for(i in 0..80){
        oneDimSolvedArr.add(gridToSolve[i][0])
    }
    print("steps required to solve: $howManySteps")
    println("oneDimSolved $oneDimSolvedArr")
    return oneDimSolvedArr
}