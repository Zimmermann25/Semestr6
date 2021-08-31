package com.example.sudoku1.game

var dyktaZId = mutableMapOf(0 to mutableListOf(0, 1, 2, 9, 10, 11, 18, 19, 20),
    1 to mutableListOf(3, 4, 5, 12, 13, 14, 21, 22, 23),
    2 to mutableListOf(6, 7, 8, 15, 16, 17, 24, 25, 26),
    3 to mutableListOf(27, 28, 29, 36, 37, 38, 45, 46, 47),
    4 to mutableListOf(30, 31, 32, 39, 40, 41, 48, 49, 50),
    5 to mutableListOf(33, 34, 35, 42, 43, 44, 51, 52, 53),
    6 to mutableListOf(54, 55, 56, 63, 64, 65, 72, 73, 74),
    7 to mutableListOf(57, 58, 59, 66, 67, 68, 75, 76, 77),
    8 to mutableListOf(60, 61, 62, 69, 70, 71, 78, 79, 80)
)
fun <T> shuffle(list: MutableList<T>) {
    list.shuffle()
}
fun Boolean.toInt() = if (this) 1 else 0

fun intToBool(value:Int):Boolean{
    if(value > 0) return true
    return false
}

fun dictWithPossibleNumbersArr(): MutableMap<Int, MutableList<Int> > {
    val valuesDict = mutableMapOf<Int, MutableList<Int> >()
    val baseArr = mutableListOf(1,2,3,4,5,6,7,8,9)
    for (i in 0..80){
        shuffle(baseArr)
        valuesDict[i] = baseArr.toMutableList() //VERY important is to create copy of list
    }
    for (i in 0..80){//this value will remember index of lastly used value
        valuesDict[i]?.add(0) // wanted safe operator
    }
    return valuesDict
}

fun rowCheck(number:Int, numberIndex:Int, rowIndex:Int, arr:MutableList<Int> = mutableListOf()):Boolean{
    for (i in 0..8){
        if(number==arr[i + rowIndex*9] && numberIndex != (i+rowIndex*9)) return false
    }
    return true
}

fun colCheck(number:Int, numberIndex:Int, colIndex:Int, arr:MutableList<Int> = mutableListOf()):Boolean{
    for(i in 0..8){
        //println("number $number, arr: $arr, ind: ${i*9 + colIndex} ")
        if( number == arr[i*9 + colIndex] && numberIndex != (i*9 + colIndex) )return false
    }
    return true
}

fun calculateId(numIndex:Int): Int{
    val row = numIndex/27; //dzielenie całkowite
    val whichColumn = numIndex % 9; //konkretna kolumna
    val colId = whichColumn/3;
    val squareId = 3*row + colId;
    return squareId
}

fun squareCheck(number:Int, numIndex:Int, arr:MutableList<Int> = mutableListOf()):Boolean{
    val currentSquare = calculateId(numIndex);
    for(i in 0..8){
        val indexCompare = dyktaZId.getValue(currentSquare)[i];
        if( number == arr[indexCompare] && indexCompare != numIndex) return false
    }
    return true
}

fun insertTry(goodNums:Int, curRowIndex:Int, curColIndex:Int, emptyInsertedArr:MutableList<Int>, valuesArr:MutableMap<Int, MutableList<Int>>): List<Int> {
    val numberIndexToInsert = valuesArr.getValue(goodNums)[9]
    val numberToInsert = valuesArr.getValue(goodNums)[numberIndexToInsert]
    val rowOk = rowCheck(numberToInsert, goodNums, curRowIndex, emptyInsertedArr)
    //println("after rowCheck ok")
   // println("numberToInsert:$numberToInsert, goodNums:$goodNums, curColIndex:$curColIndex, emptyArr:$emptyInsertedArr")
    val colOk = colCheck(numberToInsert, goodNums, curColIndex, emptyInsertedArr)
    //println("after colCheck ok")
    val squareOk = squareCheck(numberToInsert, goodNums, emptyInsertedArr)
    valuesArr.getValue(goodNums)[9] += 1 // zwiększenie wartości zmiennej indeksującej
    val allOk = (rowOk && colOk && squareOk).toInt()//wtf, really have to write fun for it?
    val returnList = listOf(allOk, numberToInsert)
    return returnList // tu byl blad, jesli zwracam wiecej niz jedną wartość, to musi byc array*/

}

// delete given amount of numbers from generated grid, to allow user solve it
fun truncateGeneratedGrid(howManyLeave:Int, generatedGridArr:MutableList<Int>): MutableList< MutableList<Int>>{
    var counter = 0
    val indexesToDel = (0..80).toMutableList()
    shuffle(indexesToDel) // i will shuffle indexes, and 81 - howManyLeave indexes starting from the beginning will be removed
    while( counter < 81-howManyLeave){
        generatedGridArr[ indexesToDel[counter] ] = 0
        counter +=1
    }
    //now i also have to mark which fields will be constant in grid and which will be left for user to fill
    println("indexes: $indexesToDel")
    val createdGrid:MutableList<MutableList<Int>>  = mutableListOf<MutableList<Int>>()
    for(i in 0..80){
        if(generatedGridArr[i] ==0) createdGrid.add(mutableListOf(0, 0))
        else createdGrid.add(mutableListOf(generatedGridArr[i], 1))
        //old value from generated grid, and 1 mean true - this is permanent value in grid
    }
    print("createdGrid: $createdGrid")
    return createdGrid
}


//BENEATH ARE FUNCTIONS REQUIRED TO SOLVE GRID, ALMOST THE SAME AS ABOVE, BUT USING 2 DIM LIST INSTEAD OF 1, and new function elimination2D

fun rowCheck2(number:Int, numberIndex:Int, rowIndex:Int, arr:MutableList<MutableList<Int>> = mutableListOf()):Boolean{
    for (i in 0..8){
        if(number==arr[i + rowIndex*9][0] && numberIndex != (i+rowIndex*9)) return false
    }
    return true
}

fun colCheck2(number:Int, numberIndex:Int, colIndex:Int, arr:MutableList<MutableList<Int>> = mutableListOf()):Boolean{
    for(i in 0..8){
        //println("number $number, arr: $arr, ind: ${i*9 + colIndex} ")
        if( number == arr[i*9 + colIndex][0] && numberIndex != (i*9 + colIndex) )return false
    }
    return true
}

fun squareCheck2(number:Int, numIndex:Int, arr:MutableList<MutableList<Int>> = mutableListOf()):Boolean{
    val currentSquare = calculateId(numIndex);
    for(i in 0..8){
        val indexCompare = dyktaZId.getValue(currentSquare)[i];
        if( number == arr[indexCompare][0] && indexCompare != numIndex) return false
    }
    return true
}


fun insertTry2(goodNums:Int, curRowIndex:Int, curColIndex:Int, emptyInsertedArr:MutableList<MutableList<Int>>, valuesArr:MutableMap<Int, MutableList<Int>>): List<Int> {
    //println("insertTry2 values arr: $valuesArr")
    var lastIndex:Int = 0
    lastIndex = valuesArr.getValue(goodNums).size - 1 // should always work

    val numberIndexToInsert = valuesArr.getValue(goodNums)[lastIndex]
    val numberToInsert = valuesArr.getValue(goodNums)[numberIndexToInsert]
    val rowOk = rowCheck2(numberToInsert, goodNums, curRowIndex, emptyInsertedArr)
    valuesArr.getValue(goodNums)[lastIndex] +=1
    if(rowOk){//here is cascade of conditions, if any will be wrong, I dont need to go through another and waste time
        val colOk = colCheck2(numberToInsert, goodNums, curColIndex, emptyInsertedArr)
        if(colOk){
            val squareOk = squareCheck2(numberToInsert, goodNums, emptyInsertedArr)
            if(squareOk){
                return listOf(1, numberToInsert) //1 mean true, we can insert this value to grid
            }
        }
    }
    return listOf(0, numberToInsert)//0 - false, cant insert this number to grid

}

fun emptyIndexesGet(partiallyFilledGrid: MutableList<MutableList<Int>>): MutableList<Int>{
    val listWithGoodKeys = mutableListOf<Int>()//in this list i will store indexes of grid to solve
    for(k in 0..80){
        if (partiallyFilledGrid[k][0] == 0){
            listWithGoodKeys.add(k)
        }
    }
    return listWithGoodKeys
}

//this function eleminates values which cant be placed at given positions, because it already exists in row/col/square
fun elimination2Dim(partiallyFilledGrid: MutableList<MutableList<Int>>): MutableMap<Int, MutableList<Int>>  {//Any because i will have (dict and list) in list
    val eliminationDict:MutableMap<Int, MutableList<Int>> = mutableMapOf()

    for(k in 0..80) {
        if (partiallyFilledGrid[k][0] == 0) { // check whether is free cell or cell with const value
            val curRow = k / 9
            val curCol = k % 9
            val tempList = mutableListOf(1, 2, 3, 4, 5, 6, 7, 8, 9, 0)

            for (i in 0..8) {//wartości z itego wiersza odpowiadanjące danej kolumnie(po prostu pionowo xd)
                val curNum = partiallyFilledGrid[i * 9 + curCol][0]
                val curNumIndex = tempList.indexOf(curNum)//modyfikacja dla uzycia w JS
                if (curNum != 0 && curNumIndex > -1) { ////czy taki numer jest jeszcze w tablicy
                    tempList.removeAt(curNumIndex) // check if it removes correctly
                }
            }

            for (i in 0..8) {//poziomo
                val curNum = partiallyFilledGrid[i + curRow * 9][0]
                val curNumIndex = tempList.indexOf(curNum)//modyfikacja dla uzycia w JS
                if (curNum != 0 && curNumIndex > -1) {
                    tempList.removeAt(curNumIndex)
                }
            }

            val curSquare = calculateId(k)
            for (i in 0..8) {
                val idToCheck = dyktaZId.getValue(curSquare)[i]
                val curNum = partiallyFilledGrid[idToCheck][0]
                val curNumIndex = tempList.indexOf(curNum)
                if (curNum != 0 && curNumIndex > -1) {
                    tempList.removeAt(curNumIndex)
                }
            }

            eliminationDict[k] = tempList

        }//if

    }//for
    return eliminationDict
}


fun convertOneDimListToTwoDim(){

}







