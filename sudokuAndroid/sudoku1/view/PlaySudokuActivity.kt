package com.example.sudoku1.view


//import com.example.sudoku1.view.SettingsActivity
import android.content.Intent
import android.graphics.Color
import android.graphics.PorterDuff
import androidx.lifecycle.Observer
import androidx.lifecycle.ViewModelProviders
import androidx.appcompat.app.AppCompatActivity
import android.os.Bundle
import android.os.SystemClock
import android.widget.Button
import androidx.core.content.ContextCompat
import com.example.sudoku1.R
import com.example.sudoku1.game.Cell
import com.example.sudoku1.view.custom.SudokuBoardView
import com.example.sudoku1.viewmodel.PlaySudokuViewModel
import kotlinx.android.synthetic.main.activity_main.*
import android.view.Window
import android.view.WindowManager
import android.view.View
import android.widget.Toast


class PlaySudokuActivity : AppCompatActivity(), SudokuBoardView.OnTouchListener {

    private lateinit var viewModel: PlaySudokuViewModel
    private lateinit var numberButtons: List<Button>

    var activityVal = 0

    override fun onSaveInstanceState(savedInstanceState: Bundle) {
        super.onSaveInstanceState(savedInstanceState)
        println("onSave")
        // Save UI state changes to the savedInstanceState.
        // This bundle will be passed to onCreate if the process is
        // killed and restarted.
        savedInstanceState.putBoolean("MyBoolean", true)
        savedInstanceState.putDouble("myDouble", 1.9)
        savedInstanceState.putInt("MyInt", 1)
        savedInstanceState.putString("MyString", "Welcome back to Android")
        // etc.
    }

    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        setContentView(com.example.sudoku1.R.layout.activity_main)


        //timer
        val startTime:Long = 0
        stopwatch.base = SystemClock.elapsedRealtime() + startTime
        stopwatch.start()

        SudokuBoardView.registerListener(this)
        viewModel = ViewModelProviders.of(this).get(PlaySudokuViewModel::class.java)
        viewModel.sudokuGame.selectedCellLiveData.observe(this, Observer{ updateSelectedCellUI(it) })//to change it dynamically
        viewModel.sudokuGame.cellsLiveData.observe(this, Observer{updateCells(it)})
        viewModel.sudokuGame.isTakingNotesLiveData.observe(this, Observer{updateNoteTakingUI(it)})
        viewModel.sudokuGame.highlightedKeysLiveData.observe(this, Observer{updateHighlightedKeys(it)})

        numberButtons = listOf(oneButton, twoButton, threeButton, fourButton, fiveButton, sixButton, sevenButton,
            eightButton, nineButton)

        numberButtons.forEachIndexed{ index, button -> //+1, because indexing starts from 0, and values from 1
            button.setOnClickListener{ viewModel.sudokuGame.handleInput(index + 1 ) }
        }

        settingsButton.setOnClickListener{
            println("switch activity in Play")
            val intent = Intent(this@PlaySudokuActivity, SettingsActivity::class.java)
            val settingsLevelValue:Int = intent.getIntExtra("myInt", 1)
            intent.putExtra("myIntPlay", 111)
            print("levelId")
            startActivity(intent)
        }

        val settingsLevelValue:Int = intent.getIntExtra("myInt", 0)
        println("onCreate: $settingsLevelValue")

        notesButton.setOnClickListener{viewModel.sudokuGame.changeNoteTakingState()}//mark if taking notes after click button
        deleteButton.setOnClickListener{viewModel.sudokuGame.delete()}
        playButton.setOnClickListener{viewModel.sudokuGame.playSudokuFunc(settingsLevelValue)}
        solveButton.setOnClickListener{viewModel.sudokuGame.solveSudokuFunc()}
        hintButton.setOnClickListener{viewModel.sudokuGame.hintSudokuFunc()}
        checkSolutionButton.setOnClickListener{resultMessage()}
    }

    private fun updateCells(cells: List<Cell>?) = cells?.let{
        SudokuBoardView.updateCells(cells)//inside block will run only if cells arent null, and will become "it" inside
    }

    private fun updateSelectedCellUI(cell: Pair<Int, Int>?) = cell?.let {
        SudokuBoardView.updateSelectedCellUI(cell.first, cell.second)
    }

    private fun updateNoteTakingUI(isNoteTaking: Boolean?) = isNoteTaking?.let{
        val color = if(it) ContextCompat.getColor(this, com.example.sudoku1.R.color.primaryColor) else Color.LTGRAY
        notesButton.setBackgroundColor(color)
    }

    private fun updateHighlightedKeys(set: Set<Int>?) = set?.let{
        numberButtons.forEachIndexed{ index, button ->
            val color = if (set.contains(index+1)) ContextCompat.getColor(this, com.example.sudoku1.R.color.primaryColor) else Color.LTGRAY
            button.setBackgroundColor(color)
        }
    }

    override fun onCellTouch(row:Int, col:Int){
        viewModel.sudokuGame.updateSelectedCell(row, col)
    }

    fun resultMessage(){
        if(viewModel.sudokuGame.checkSolution()){
            Toast.makeText(this, "Solution correct", Toast.LENGTH_SHORT).show()
        }
        else{
            Toast.makeText(this, "Solution incorrect", Toast.LENGTH_SHORT).show()
        }

    }

    override fun onRestoreInstanceState(savedInstanceState: Bundle) {
        println("onRestore")
        super.onRestoreInstanceState(savedInstanceState)
        // Restore UI state from the savedInstanceState.
        // This bundle has also been passed to onCreate.
        val myBoolean = savedInstanceState.getBoolean("MyBoolean")
        val myDouble = savedInstanceState.getDouble("myDouble")
        val myInt = savedInstanceState.getInt("MyInt")
        val myString = savedInstanceState.getString("MyString")
    }


}

