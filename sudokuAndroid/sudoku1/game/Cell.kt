package com.example.sudoku1.game

class Cell(val row:Int, val col: Int, var value:Int,
           var isStartingCell: Boolean = false,
           var notes: MutableSet<Int> = mutableSetOf<Int>()) // val to store it in a class, set beacuse of notes will be unique