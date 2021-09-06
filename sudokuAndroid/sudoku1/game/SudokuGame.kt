package com.example.sudoku1.game

import androidx.lifecycle.MutableLiveData


class Cell(val row:Int, val col: Int, var value:Int,
           var isStartingCell: Boolean = false,
           var notes: MutableSet<Int> = mutableSetOf<Int>()) // val to store it in a class, set beacuse of notes will be unique


class Board(val size: Int, val cells: MutableList<Cell>){

    fun getCell(row:Int, col:Int) = cells[row*size + col] // one dim array

    fun setCell(row:Int, col: Int, value:Int){
        cells[row*size + col].value = value
        println("setCell")
    }

}

class SudokuGame{

    var selectedCellLiveData = MutableLiveData<Pair<Int, Int>>()
    var cellsLiveData = MutableLiveData<List<Cell>>()
    val isTakingNotesLiveData = MutableLiveData<Boolean>()
    val highlightedKeysLiveData = MutableLiveData<Set<Int>>()

    private var selectedRow = -1// it mean that user didnt click on grid yet
    private var selectedCol = -1
    private var isTakingNotes = false

    val cells = MutableList(81){i -> Cell(i/9, i%9, 0 )}
    var board: Board = Board(9, cells) // object to hold actual grid data

    var generatedFullGrid: MutableList<Int> = mutableListOf() //one dim
    var gridToSolve: MutableList<MutableList<Int>> = mutableListOf()

    var currentGridLevel:Int = 0// easy by default, it s use to save gridLevel(settingsLevelValue) value which is passed to playSudokuFunc from PlaySudokuActivity and SettingsActivity

    var playFuncClicked:Boolean = false//cant solve or give hint when user didnt hit play button
    init{
        print("init print++++++++++++++++++++++++++++++++++++++++++++++++++")
    }

    fun handleInput(number:Int):Boolean{
        if (selectedRow==-1 || selectedCol ==-1) return false
        val cell = board.getCell(selectedRow, selectedCol)
        if (cell.isStartingCell) return false //dont update constant cell

        if(isTakingNotes){
            if(cell.notes.contains(number)){
                cell.notes.remove(number)
            }else{
                cell.notes.add(number)
            }
            highlightedKeysLiveData.postValue(cell.notes)

        }else{
            val check = checkNumberInsert2(number,selectedRow*9 + selectedCol, gridToSolve)
            if(check){
                cell.value = number
                gridToSolve[selectedRow*9 + selectedCol] = mutableListOf<Int>(number, 0) // 0 mean not constant field
            }else{
                return false
            }
        }
        cellsLiveData.postValue(board.cells)
        return true
    }


    fun updateSelectedCell(row:Int, col:Int){
        val cell = board.getCell(row, col)
        println("selectedCell: ${9*cell.row +cell.col}")
        if (!cell.isStartingCell){
            selectedRow = row
            selectedCol = col
            selectedCellLiveData.postValue(Pair(row, col))

            if(isTakingNotes){
                highlightedKeysLiveData.postValue(cell.notes)
            }
        }
    }

    fun changeNoteTakingState(){
        if(selectedRow >= 0 && selectedCol >=0){
            isTakingNotes = !isTakingNotes
            isTakingNotesLiveData.postValue(isTakingNotes)
            val curNotes = if (isTakingNotes){
                board.getCell(selectedRow, selectedCol).notes
            }else{
                setOf<Int>()// dont display notes
            }
            highlightedKeysLiveData.postValue(curNotes)
        }

    }

    fun delete(){
        if(selectedRow >= 0 && selectedCol >=0){
            val cell = board.getCell(selectedRow, selectedCol)
            if (isTakingNotes){
                cell.notes.clear()
                highlightedKeysLiveData.postValue(setOf()) //empty set
            }else{
                cell.value = 0
                gridToSolve[selectedRow*9 + selectedCol] = mutableListOf<Int>(0, 0)//value 0 and  0 which mean variable cell
            }
            cellsLiveData.postValue(board.cells)
        }
    }

    fun playSudokuFunc(gridLevel:Int = 0){
        playFuncClicked = true
        val howManyLeave = when(gridLevel){
            0 -> 79 // 79 for test purposes, 35 normally
            1 -> 30
            2 -> 25
            else -> 0 //  gridLevel 3 mean empty grid, but when required else block
        }
        if(howManyLeave>0){ //dont generate grid after clicking play button if user want empty grid
            generatedFullGrid = gridGenerate()
        }else{
            generatedFullGrid = MutableList(81){0} // fill whole grid with zeros
        }
        currentGridLevel = gridLevel

        print("howManyLeave: $howManyLeave")
        gridToSolve = truncateGeneratedGrid(howManyLeave, generatedFullGrid.toMutableList())//important to use copy
        val cells = MutableList(81){i -> Cell(i/9, i%9, gridToSolve[i][0], intToBool(gridToSolve[i][1]) )}
        board = Board(9, cells)
        selectedCellLiveData.postValue(Pair(selectedRow, selectedCol))
        cellsLiveData.postValue(board.cells)
        isTakingNotesLiveData.postValue(isTakingNotes)
        println(board.cells)
    }

    fun solveSudokuFunc(){
        if(playFuncClicked){
            println("gridToSolve: $gridToSolve")
            var solvedGrid:MutableList<Int> = generatedFullGrid//generated partially filled grid, use full generated grid, dont solve it from scratch
            if(currentGridLevel >=3){ //empty grid from settings, use my solving algorithm
                solvedGrid = solveGrid(this.gridToSolve)
            }

            var solvedCells = MutableList(81){i -> Cell(
                i/9,
                i%9,
                if (intToBool(gridToSolve[i][1])) gridToSolve[i][0] else solvedGrid[i] , //if value was const then use it, otherwise use values from solved
                intToBool(gridToSolve[i][1]) )}

            board = Board(9, solvedCells)
            cellsLiveData.postValue(board.cells)
        }
    }

    fun hintSudokuFunc(){
        if(playFuncClicked && currentGridLevel<3){//hint function is not available for own empty grid
            val yetEmpty:MutableList<Int> = mutableListOf() //empty cells
            val filledByUser:MutableList<Int> = mutableListOf()//only for grids with more than one solution
            //first find only empty grids and try to fill them
            for( row in 0..8){
                for(col in 0..8){
                    val curCell = board.getCell(row, col)
                    if(!curCell.isStartingCell ){
                        if(curCell.value < 1 || curCell.value > 9){
                            yetEmpty.add(row*9 + col)
                        }else{
                            filledByUser.add(row*9 + col)
                        }
                    }

                }
            }
            var indexToHint:Int = -1
            if(yetEmpty.size >0){
                indexToHint = yetEmpty.random()
                println("indexToHint: $indexToHint")
            }else if(filledByUser.size >0){
                indexToHint = filledByUser.random()
            }//if None of above will occur it mean that grid is solved

            println("generatedFullGrid[indexToHint], $generatedFullGrid[indexToHint]")
            board.setCell(indexToHint/9, indexToHint%9, generatedFullGrid[indexToHint])
            selectedCellLiveData.postValue(Pair(selectedRow, selectedCol))
            cellsLiveData.postValue(board.cells) // refresh screen
        }

    }

    fun checkSolution():Boolean{
        var gridToSolve:MutableList<Int> = mutableListOf()
        board.cells.forEach{
            gridToSolve.add(it.value) // one dim array now
        }
        println("onedim: $gridToSolve")

        for(row in 0..8){ //check corectness of every row
            var currentSum = 0
            var currentProduct = 1
            for( col in 0..8){
                currentSum += gridToSolve[row*9 + col]
                currentProduct *= gridToSolve[row*9 + col]
                println(gridToSolve[row*9 + col])
            }
            println("product: $currentProduct, sum: $currentSum")
            if(currentProduct != 362880 || currentSum != 45){ //1*2*3*4*5*6*7*8*9 = 362880
                println("error in rows $currentProduct, sum: $currentSum")
                return false
            }
        }

        for(row in 0..8){ //check corectness of every col
            var currentSum = 0
            var currentProduct = 1
            for( col in 0..8){
                currentSum += gridToSolve[col*9 + row]
                currentProduct *= gridToSolve[col*9 + row]
            }
            if(currentProduct != 362880 || currentSum != 45){ //1*2*3*4*5*6*7*8*9 = 362880
                println("error in cols")
                return false
            }
        }

        for(squareId in 0..8){
            var currentSum = 0
            var currentProduct = 1
            for(squareIdCellIndex in 0..8){
                var curIndex = dictWithSquaresId.getValue(squareId)[squareIdCellIndex]
                currentSum += gridToSolve[curIndex]
                currentProduct *= gridToSolve[curIndex]
            }
            if(currentProduct != 362880 || currentSum != 45){ //1*2*3*4*5*6*7*8*9 = 362880
                println("error in squares")
                return false
            }
        }

        return true
    }



}