package com.example.sudoku1.game
import android.view.View
import android.widget.LinearLayout
import android.widget.Toast
import androidx.lifecycle.MutableLiveData

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

    var emptyFieldsLeft = 81
    var currentGridLevel:Int = 0// easy by default, it s use to save gridLevel(settingsLevelValue) value which is passed to playSudokuFunc from PlaySudokuActivity and SettingsActivity

    var playFuncClicked:Boolean = false//cant solve or give hint when user didnt hit play button
    init{
        print("init print++++++++++++++++++++++++++++++++++++++++++++++++++")
    }

    fun handleInput(number:Int){
        if (selectedRow==-1 || selectedCol ==-1) return
        val cell = board.getCell(selectedRow, selectedCol)
        if (cell.isStartingCell) return

        if(isTakingNotes){
            if(cell.notes.contains(number)){
                cell.notes.remove(number)
            }else{
                cell.notes.add(number)
            }
            highlightedKeysLiveData.postValue(cell.notes)

        }else{
            if(cell.value ==0){
                emptyFieldsLeft -=1// if input to empty cell then decrease by one
            }
            cell.value = number
            gridToSolve[selectedRow*9 + selectedCol] = mutableListOf<Int>(number, 0)
        }
        cellsLiveData.postValue(board.cells)

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
        print("fieldsLeft: $emptyFieldsLeft")
        if(emptyFieldsLeft ==0){
            val oneDimGridToSolve:MutableList<Int> = mutableListOf()
            println(gridToSolve.size)
            for (i in 0..gridToSolve.size){
                oneDimGridToSolve[i] = gridToSolve[i][0]
            }

            println("oneDim: $oneDimGridToSolve")
            //val result = checkSolution(oneDimGridToSolve)
            //println("result: $result")
        }

    }

    fun changeNoteTakingState(){
        if(selectedRow >= 0 && selectedCol >=0){
            isTakingNotes = !isTakingNotes
            isTakingNotesLiveData.postValue(isTakingNotes)
            val curNotes = if (isTakingNotes){
                board.getCell(selectedRow, selectedCol).notes
            }else{
                setOf<Int>()
            }
            highlightedKeysLiveData.postValue(curNotes)
        }

    }

    fun delete(){
        if(selectedRow >= 0 && selectedCol >=0){
            emptyFieldsLeft +=1
            val cell = board.getCell(selectedRow, selectedCol)
            if (!isTakingNotes){
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
        generatedFullGrid = gridGenerate()

        val howManyLeave = when(gridLevel){
            0 -> 35
            1 -> 30
            2 -> 25
            else -> 0 //  gridLevel 3 mean empty grid, but when required else block
        }
        currentGridLevel = gridLevel

        emptyFieldsLeft = 81 - howManyLeave
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
            if(currentGridLevel ==3){ //empty grid from settings, use my solving algorithm
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
        if(playFuncClicked){
            emptyFieldsLeft -=1
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

    //TODO - show result on screen(green good, red bad), func to check whether good, highlight the same values as currentInput
    fun checkIfGoodValue(row:Int, col:Int, value:Int){

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
                var curIndex = dyktaZId.getValue(squareId)[squareIdCellIndex]
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