package com.example.sudoku1.game

class Board(val size: Int, val cells: MutableList<Cell>){

    fun getCell(row:Int, col:Int) = cells[row*size + col] // one dim array

    fun setCell(row:Int, col: Int, value:Int){
        cells[row*size + col].value = value
        println("setCell")
    }

}