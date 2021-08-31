package com.example.sudoku1.game


fun gridGenerate(): MutableList<Int>{
    val generatedGrid = mutableListOf<Int>()
    for(i in 0..80){
        generatedGrid.add(i, 0)//fill list with values 0
    }

    var howMany = 0 // steps counter, for efficiency testing only
    val arrNumDictForGenerateGrid = dictWithPossibleNumbersArr()
    var goodNums = 0 //how many valid values are currently on grid
    println("dict, $arrNumDictForGenerateGrid")
    while( goodNums< 81){
        var cantInsert = false;

        if(arrNumDictForGenerateGrid.getValue(goodNums)[9] ==9){
            arrNumDictForGenerateGrid.getValue(goodNums)[9] = 0
            generatedGrid[goodNums-1] = 0
            goodNums -=1
            howMany +=1
        }else{
            val curRowIndex = goodNums/9
            val curColIndex = goodNums % 9
            var listFromFunc = insertTry(goodNums, curRowIndex, curColIndex, generatedGrid, arrNumDictForGenerateGrid)
            var allOk = listFromFunc[0]
            var numberToInsert = listFromFunc[1]
            howMany +=1

            while (allOk != 1){ // need to use 1 instead of true
                howMany +=1
                if ( arrNumDictForGenerateGrid.getValue(goodNums)[9] < 9 ){
                    listFromFunc = insertTry(goodNums, curRowIndex, curColIndex, generatedGrid, arrNumDictForGenerateGrid)
                    allOk = listFromFunc[0]
                    numberToInsert = listFromFunc[1]
                }
                else if ( arrNumDictForGenerateGrid.getValue(goodNums)[9] == 9){
                    arrNumDictForGenerateGrid.getValue(goodNums)[9] = 0
                    generatedGrid[goodNums - 1] = 0
                    goodNums -=2
                    cantInsert = true
                    break
                }
            }//while allOk

            if ( !cantInsert)generatedGrid[goodNums] = numberToInsert
            goodNums+=1

        }// while else
    }//while loop

    return generatedGrid
}


