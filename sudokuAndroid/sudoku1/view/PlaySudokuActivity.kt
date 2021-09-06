package com.example.sudoku1.view


import android.content.Intent
import android.graphics.Color
import androidx.lifecycle.Observer
import androidx.lifecycle.ViewModelProviders
import androidx.appcompat.app.AppCompatActivity
import android.os.Bundle
import android.os.SystemClock
import android.widget.Button
import androidx.core.content.ContextCompat
import com.example.sudoku1.game.Cell
import kotlinx.android.synthetic.main.activity_main.*
import android.widget.Toast


class PlaySudokuActivity : AppCompatActivity(), SudokuBoardView.OnTouchListener {

    private lateinit var viewModel: PlaySudokuViewModel
    private lateinit var numberButtons: List<Button>

    var isTakingNotes:Boolean = false //check if notes are inserted or grid values

    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        setContentView(com.example.sudoku1.R.layout.activity_main)


        SudokuBoardView.registerListener(this)//data input listeners
        viewModel = ViewModelProviders.of(this).get(PlaySudokuViewModel::class.java)
        viewModel.sudokuGame.selectedCellLiveData.observe(this, Observer{ updateSelectedCellUI(it) })//to change it dynamically
        viewModel.sudokuGame.cellsLiveData.observe(this, Observer{updateCells(it)})
        viewModel.sudokuGame.isTakingNotesLiveData.observe(this, Observer{updateNoteTakingUI(it)})
        viewModel.sudokuGame.highlightedKeysLiveData.observe(this, Observer{updateHighlightedKeys(it)})

        numberButtons = listOf(oneButton, twoButton, threeButton, fourButton, fiveButton, sixButton, sevenButton,
            eightButton, nineButton)

        numberButtons.forEachIndexed{ index, button -> //+1, because indexing starts from 0, and values from 1
            button.setOnClickListener{
                val inputResult = viewModel.sudokuGame.handleInput(index + 1 )
                if(!inputResult){
                    wrongNumberInsertionToast()
                }
            }
        }

        settingsButton.setOnClickListener{
            println("switch activity in Play")
            val intent = Intent(this@PlaySudokuActivity, SettingsActivity::class.java)
            startActivity(intent)
        }

        val settingsLevelValue:Int = intent.getIntExtra("levelValue", 0)//0 is code for easy, 1 for medium, 2 for hard, >2 for own grid

        notesButton.setOnClickListener{
            viewModel.sudokuGame.changeNoteTakingState()
            isTakingNotes = !isTakingNotes
        }//mark if taking notes after click button

        deleteButton.setOnClickListener{viewModel.sudokuGame.delete()}
        playButton.setOnClickListener{
            viewModel.sudokuGame.playSudokuFunc(settingsLevelValue)
            stopwatch.base = SystemClock.elapsedRealtime()
            stopwatch.start()
        }
        solveButton.setOnClickListener{
            viewModel.sudokuGame.solveSudokuFunc()
            stopwatch.stop()
        }

        hintButton.setOnClickListener{viewModel.sudokuGame.hintSudokuFunc()}
        checkSolutionButton.setOnClickListener{
            val result = resultMessage()
            if(result)stopwatch.stop()
        }
    }

    fun updateCells(cells: List<Cell>?) = cells?.let{
        SudokuBoardView.updateCells(cells)//inside block will run only if cells arent null, and will become "it" inside
    }

    fun updateSelectedCellUI(cell: Pair<Int, Int>?) = cell?.let {
        SudokuBoardView.updateSelectedCellUI(cell.first, cell.second)
    }

    fun updateNoteTakingUI(isNoteTaking: Boolean?) = isNoteTaking?.let{
        val color = if(it) ContextCompat.getColor(this, com.example.sudoku1.R.color.primaryColor) else Color.LTGRAY
        notesButton.setBackgroundColor(color)
    }

    //need to modify a little bit to avoid losing color after making notes, maybe check if its in notes mode?
    fun updateHighlightedKeys(set: Set<Int>?) = set?.let{
        numberButtons.forEachIndexed{ index, button ->
            var color = ContextCompat.getColor(this, com.example.sudoku1.R.color.purple_500)//background color for grid updating mode*/
            if(isTakingNotes){
                if (set.contains(index+1))
                    color = ContextCompat.getColor(this, com.example.sudoku1.R.color.primaryColor) //background for notes taking
                else
                    color = ContextCompat.getColor(this, com.example.sudoku1.R.color.myGray) //background color for grid updating mode*/
            }

            button.setBackgroundColor(color)
        }
    }

    override fun onCellTouch(row:Int, col:Int){
        viewModel.sudokuGame.updateSelectedCell(row, col)
    }

    fun resultMessage():Boolean{
        if(viewModel.sudokuGame.checkSolution()){
            Toast.makeText(this, "Solution correct", Toast.LENGTH_SHORT).show()
            return true
        }
        else{
            Toast.makeText(this, "Solution incorrect", Toast.LENGTH_SHORT).show()
        }
        return false
    }

    fun wrongNumberInsertionToast(){
        Toast.makeText(this, "WRONG INSERTION", Toast.LENGTH_SHORT).show()
        println("bad value")
    }



}

