package com.example.sudoku1.game

//as input goes 2 dim list with info about value and if this cell is constant or not
fun solveGrid(gridToSolve:MutableList<MutableList<Int>>): MutableList<Int>{ // output is one dim list
    var howManySteps = 0
    //arrNumDict - key is cell index, and value is list with possible values at given position, and value to trace index at last position
    val arrNumDict: MutableMap<Int, MutableList<Int>> = elimination2Dim(gridToSolve)
    val listWithEmptyCellsIndexes:MutableList<Int> = emptyIndexesGet(gridToSolve)//here will be list only with indexes to fill
    var listWithEmptyCellsIndex = 0
    while(listWithEmptyCellsIndex < listWithEmptyCellsIndexes.size){
        if(howManySteps % 100000 ==0){
            println(howManySteps)
            println(gridToSolve)
        }
        var cantInsert = false
        var currentGridIndex = listWithEmptyCellsIndexes[listWithEmptyCellsIndex]
        val lastPossibleIndex = arrNumDict.getValue(currentGridIndex).size - 1//check whether we use all values from list for given cell or not

        // if no possible values for given cell left earlier, it mean that we have to reset counter of that cell array, and do backtrack
        if(arrNumDict.getValue(currentGridIndex)[lastPossibleIndex] == lastPossibleIndex){
            howManySteps +=1
            arrNumDict.getValue(currentGridIndex)[lastPossibleIndex] = 0
            currentGridIndex = listWithEmptyCellsIndexes[listWithEmptyCellsIndex-1]
            gridToSolve[currentGridIndex][0] = 0//none of values which we tried to place there was good, it mean, that we made mistake before
            listWithEmptyCellsIndex -= 1//back to previous not constant cell, after reset value in current cell
        }else{
            howManySteps += 1

            //need to declare before while
            var valuesFromInsert2Func = insertTry2(currentGridIndex, gridToSolve, arrNumDict)
            var allOk = valuesFromInsert2Func[0]
            var numberToInsert = valuesFromInsert2Func[1]

            while(allOk != 1){//try to insert every number which is still possible at this cell
                howManySteps += 1
                if(arrNumDict.getValue(currentGridIndex)[lastPossibleIndex] < lastPossibleIndex){//if not used values left left for given position try to insert
                    valuesFromInsert2Func = insertTry2(currentGridIndex, gridToSolve, arrNumDict)
                    allOk = valuesFromInsert2Func[0]
                    numberToInsert = valuesFromInsert2Func[1]
                }
                else if(arrNumDict.getValue(currentGridIndex)[lastPossibleIndex] == lastPossibleIndex){
                    arrNumDict.getValue(currentGridIndex)[lastPossibleIndex] = 0
                    currentGridIndex = listWithEmptyCellsIndexes[listWithEmptyCellsIndex-1]
                    gridToSolve[currentGridIndex][0] = 0
                    listWithEmptyCellsIndex -= 2 // -2, because at the end of main while is listWithEmptyCellsIndex += 1
                    cantInsert = true//it mean that we was not able to place any value at given position
                    break//if tried every value at given position and no success, break the loop
                }
            }//second while

            if(!cantInsert) gridToSolve[currentGridIndex][0] = numberToInsert//if found value which fit to given cell, then place it
            listWithEmptyCellsIndex += 1//always increment by one in else block
            //if value was placed, go to another cell, if not, then listWithEmptyCellsIndex -2 + 1 = listWithEmptyCellsIndex-1
            //it mean that we backtrack to previous position

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