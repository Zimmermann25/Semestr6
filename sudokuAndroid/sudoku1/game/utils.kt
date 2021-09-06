package com.example.sudoku1.game

//manual mapping grid indexes to correct grid square 3x3
var dictWithSquaresId = mutableMapOf(0 to mutableListOf(0, 1, 2, 9, 10, 11, 18, 19, 20),
    1 to mutableListOf(3, 4, 5, 12, 13, 14, 21, 22, 23),
    2 to mutableListOf(6, 7, 8, 15, 16, 17, 24, 25, 26),
    3 to mutableListOf(27, 28, 29, 36, 37, 38, 45, 46, 47),
    4 to mutableListOf(30, 31, 32, 39, 40, 41, 48, 49, 50),
    5 to mutableListOf(33, 34, 35, 42, 43, 44, 51, 52, 53),
    6 to mutableListOf(54, 55, 56, 63, 64, 65, 72, 73, 74),
    7 to mutableListOf(57, 58, 59, 66, 67, 68, 75, 76, 77),
    8 to mutableListOf(60, 61, 62, 69, 70, 71, 78, 79, 80)
)
fun <T> shuffle(list: MutableList<T>) {//shuffle func to generate grid
    list.shuffle()
}
fun Boolean.toInt() = if (this) 1 else 0

fun intToBool(value:Int):Boolean{
    if(value > 0) return true
    return false
}

//key is cell index, and value is shuffled list with values from 1 to 9
fun dictWithPossibleNumbersArr(): MutableMap<Int, MutableList<Int> > {
    val valuesDict = mutableMapOf<Int, MutableList<Int> >()
    val baseArr = mutableListOf(1,2,3,4,5,6,7,8,9)
    for (i in 0..80){
        shuffle(baseArr)
        valuesDict[i] = baseArr.toMutableList() //VERY important is to create copy of list
    }
    //now i add in the end of every array value, which will store previously used index of given array
    for (i in 0..80){//it will be used to track which value should be placed next if given value could not be placed at given cell
        valuesDict[i]?.add(0) // wanted safe operator
    }
    return valuesDict
}

fun rowCheck(number:Int, gridIndex:Int, arr:MutableList<Int> = mutableListOf()):Boolean{
    val rowIndex = gridIndex/9
    for (i in 0..8){
        if(number==arr[i + rowIndex*9] && gridIndex != (i+rowIndex*9)) return false
    }
    return true
}

fun colCheck(number:Int, gridIndex:Int, arr:MutableList<Int> = mutableListOf()):Boolean{
    val colIndex = gridIndex%9
    for(i in 0..8){
        //println("number $number, arr: $arr, ind: ${i*9 + colIndex} ")
        if( number == arr[i*9 + colIndex] && gridIndex != (i*9 + colIndex) )return false
    }
    return true
}

fun calculateId(numIndex:Int): Int{ //before check if value is unique in square i need to know id of this square
    val row = numIndex/27; //dzielenie całkowite
    val whichColumn = numIndex % 9; //konkretna kolumna
    val colId = whichColumn/3;
    val squareId = 3*row + colId;
    return squareId
}

fun squareCheck(number:Int, numIndex:Int, arr:MutableList<Int> = mutableListOf()):Boolean{
    val currentSquare = calculateId(numIndex);
    for(i in 0..8){
        val indexCompare = dictWithSquaresId.getValue(currentSquare)[i];
        if( number == arr[indexCompare] && indexCompare != numIndex) return false
    }
    return true
}

fun checkNumberInsert(numberToInsert:Int, gridIndex:Int, grid:MutableList<Int>):Boolean{
    val rowOk = rowCheck(numberToInsert, gridIndex, grid)
    if(rowOk){//here is cascade of conditions, if any will be wrong, I dont need to go through another and waste time
        val colOk = colCheck(numberToInsert, gridIndex, grid)
        if(colOk){
            val squareOk = squareCheck(numberToInsert, gridIndex, grid)
            if(squareOk){
                return true
            }
        }
    }
    return false
}


fun insertTry(currentGridIndex:Int, grid:MutableList<Int>, arrNumDict:MutableMap<Int, MutableList<Int>>): List<Int> {
    val numberIndexToInsert = arrNumDict.getValue(currentGridIndex)[9]
    val numberToInsert = arrNumDict.getValue(currentGridIndex)[numberIndexToInsert]
    var lastIndex:Int = 0
    lastIndex = arrNumDict.getValue(currentGridIndex).size - 1 //for grid generation, last index will always be 9
    arrNumDict.getValue(currentGridIndex)[lastIndex] += 1

    if(checkNumberInsert(numberToInsert, currentGridIndex, grid)){
        return listOf(1, numberToInsert)
    }
    return listOf(0, 0) // first 0 mean that i cant insert value, second value can be anything
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

fun rowCheck2(number:Int, gridIndex:Int, arr:MutableList<MutableList<Int>> = mutableListOf()):Boolean{
    val rowIndex = gridIndex/9
    for (i in 0..8){
        if(number==arr[i + rowIndex*9][0] && gridIndex != (i+rowIndex*9)) return false
    }
    return true
}

fun colCheck2(number:Int, gridIndex:Int, arr:MutableList<MutableList<Int>> = mutableListOf()):Boolean{
    val colIndex = gridIndex % 9
    for(i in 0..8){
        //println("number $number, arr: $arr, ind: ${i*9 + colIndex} ")
        if( number == arr[i*9 + colIndex][0] && gridIndex != (i*9 + colIndex) )return false
    }
    return true
}

fun squareCheck2(number:Int, gridIndex:Int, arr:MutableList<MutableList<Int>> = mutableListOf()):Boolean{
    val currentSquare = calculateId(gridIndex);
    for(i in 0..8){
        val indexCompare = dictWithSquaresId.getValue(currentSquare)[i];
        if( number == arr[indexCompare][0] && indexCompare != gridIndex) return false
    }
    return true
}

fun checkNumberInsert2(numberToInsert:Int, gridIndex:Int, grid:MutableList<MutableList<Int> >):Boolean{
    val rowOk = rowCheck2(numberToInsert, gridIndex, grid)
    if(rowOk){//here is cascade of conditions, if any will be wrong, I dont need to go through another and waste time
        val colOk = colCheck2(numberToInsert, gridIndex, grid)
        if(colOk){
            val squareOk = squareCheck2(numberToInsert, gridIndex, grid)
            if(squareOk){
                return true
            }
        }
    }
    return false
}

//valuesArr - 2 dim arr with numbers which looks good at given position and we shall check it
fun insertTry2(currentGridIndex:Int, grid:MutableList<MutableList<Int>>, arrNumDict:MutableMap<Int, MutableList<Int>>): List<Int> {

    var lastIndex:Int = 0
    lastIndex = arrNumDict.getValue(currentGridIndex).size - 1 // should always work
    val numberIndexToInsert = arrNumDict.getValue(currentGridIndex)[lastIndex]
    val numberToInsert = arrNumDict.getValue(currentGridIndex)[numberIndexToInsert]

    arrNumDict.getValue(currentGridIndex)[lastIndex] += 1
    if(checkNumberInsert2(numberToInsert, currentGridIndex, grid)){
        return listOf(1, numberToInsert) //1 mean true, we can insert this value to grid
    }
    return listOf(0, 0)//0 - false, cant insert this number to grid
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
            val tempList = mutableListOf(1, 2, 3, 4, 5, 6, 7, 8, 9, 0)//last zero is to trace value index of inserted value

            for (i in 0..8) {//elimnation in columns
                val curNum = partiallyFilledGrid[i * 9 + curCol][0]
                val curNumIndex = tempList.indexOf(curNum)
                if (curNum != 0 && curNumIndex > -1) { // -1 mean that value isnt present in array
                    tempList.removeAt(curNumIndex) // check if it removes correctly
                }
            }

            for (i in 0..8) {//elimination in rows
                val curNum = partiallyFilledGrid[i + curRow * 9][0]
                val curNumIndex = tempList.indexOf(curNum)//modyfikacja dla uzycia w JS
                if (curNum != 0 && curNumIndex > -1) {
                    tempList.removeAt(curNumIndex)
                }
            }

            val curSquare = calculateId(k)
            for (i in 0..8) {
                val idToCheck = dictWithSquaresId.getValue(curSquare)[i]
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









