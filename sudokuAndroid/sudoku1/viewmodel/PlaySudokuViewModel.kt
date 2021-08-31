package com.example.sudoku1.viewmodel

import androidx.lifecycle.ViewModel
import com.example.sudoku1.game.SudokuGame

class PlaySudokuViewModel : ViewModel(){
    val sudokuGame = SudokuGame()
}

