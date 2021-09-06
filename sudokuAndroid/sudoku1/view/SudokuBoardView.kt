package com.example.sudoku1.view


import android.content.Context
import android.graphics.*
import android.util.AttributeSet
import android.view.MotionEvent
import android.view.View
import com.example.sudoku1.game.Cell
import kotlin.math.min

import androidx.lifecycle.ViewModel
import com.example.sudoku1.game.SudokuGame

class PlaySudokuViewModel : ViewModel(){
    val sudokuGame = SudokuGame()
}

class SudokuBoardView(context: Context, attributeSet: AttributeSet) : View(context, attributeSet) {

    private var sqrSize = 3
    private var size = 9

    //placeholders, correct value is set in onDraw method
    private var cellSizePixels = 0F
    private var noteSizePixels = 0F

    private var selectedRow = -1
    private var selectedCol = -1

    private var listener: OnTouchListener? = null

    private var cells: List<Cell>? = null

    private val thickLinePaint = Paint().apply{
        style = Paint.Style.STROKE
        color = Color.BLACK
        strokeWidth = 7F
    }

    private val thinLinePaint = Paint().apply{
        style = Paint.Style.STROKE
        color = Color.BLACK
        strokeWidth = 2F
    }

    private val selectedCellPaint = Paint().apply{
        style = Paint.Style.FILL_AND_STROKE
        color = Color.parseColor("#2137bb")
    }

    private val conflictingCellPaint = Paint().apply{//cells in the same row, col, and little3x3 square
        style = Paint.Style.FILL_AND_STROKE
        color = Color.parseColor("#666666")
    }

    private val textPaint = Paint().apply {
        style = Paint.Style.FILL_AND_STROKE
        color = Color.BLACK
    }

    private val startingCellTextPaint = Paint().apply(){
        style = Paint.Style.FILL_AND_STROKE
        color = Color.BLACK
        typeface = Typeface.DEFAULT_BOLD
    }

    private val startingCellPaint = Paint().apply{
        style = Paint.Style.FILL_AND_STROKE
        color = Color.parseColor("#654321")
    }

    private val noteTextPaint = Paint().apply{
        style = Paint.Style.FILL_AND_STROKE
        color = Color.BLACK
    }

    override fun onMeasure(widthMeasureSpec: Int, heightMeasureSpec: Int) {
        super.onMeasure(widthMeasureSpec, heightMeasureSpec)
        val sizePixels = min(widthMeasureSpec, heightMeasureSpec)
        setMeasuredDimension(sizePixels, sizePixels)
    }

    override fun onDraw(canvas: Canvas){
        updateMeasurements(width)

        fillCells(canvas)
        drawText(canvas)
        drawLines(canvas)

    }

    private fun updateMeasurements(width:Int){
        cellSizePixels = (width/size).toFloat()
        noteSizePixels = cellSizePixels / sqrSize.toFloat()
        noteTextPaint.textSize = cellSizePixels / sqrSize.toFloat()
        textPaint.textSize = cellSizePixels / 1.5F
        startingCellTextPaint.textSize = cellSizePixels / 1.5F
    }


    private fun fillCells(canvas: Canvas){
        cells?.forEach{ //row by row
            val row = it.row
            val col = it.col

            if ( it.isStartingCell){
                fillCell(canvas, row, col, startingCellPaint)
            }else if(row == selectedRow && col == selectedCol){
                fillCell(canvas, row, col, selectedCellPaint)
            }else if (row == selectedRow || col == selectedCol){ // conflick in row or col
                fillCell(canvas, row, col, conflictingCellPaint)
            }//quite nice trick using floor division to obtain current 3x3 square which is conflicting without usage of mine calculateId func
            else if(selectedRow >= 0 && selectedCol >= 0 && row/3 == selectedRow/3 && col/3 == selectedCol/3 ){
                fillCell(canvas, row, col, conflictingCellPaint)//conflick in little 3x3 square
            }
        }
    }

    private fun fillCell(canvas: Canvas, row:Int, col:Int, paint:Paint){
        canvas.drawRect(col*cellSizePixels, row*cellSizePixels, (col+1)*cellSizePixels, (row+1)*cellSizePixels, paint)
    }

    private fun drawLines(canvas:Canvas){
        canvas.drawRect(0F, 0F, width.toFloat(), height.toFloat(), thickLinePaint)

        for (i in 1 until size){
            val paintToUse = when (i % sqrSize){
                0-> thickLinePaint
                else -> thinLinePaint
            }
            canvas.drawLine(//vertical lines
                i * cellSizePixels,
                0F,
                i * cellSizePixels,
                height.toFloat(),
                paintToUse
            )
            //horizontal lines
            canvas.drawLine(
                0F,
                i * cellSizePixels,
                width.toFloat(),
                i * cellSizePixels,
                paintToUse
            )
        }
    }

    private fun drawText(canvas: Canvas){
        cells?.forEach{cell->
            val value = cell.value

            val textBounds = Rect()//empty rectangel yet

            if(value==0){ // 0 is like a placeholder, and mean that we can draw notes
                cell.notes.forEach { note ->    // every note in notes set
                    val rowInCell = (note - 1) / sqrSize
                    val colInCell = (note - 1) % sqrSize
                    val valueString = note.toString()
                    noteTextPaint.getTextBounds(valueString, 0, valueString.length, textBounds)
                    val textWidth = noteTextPaint.measureText(valueString)
                    val textHeight = textBounds.height()

                    canvas.drawText(
                        valueString,
                        (cell.col*cellSizePixels) + (colInCell*noteSizePixels) + noteSizePixels/2 - textHeight/2f,
                        (cell.row*cellSizePixels) + (rowInCell*noteSizePixels) + noteSizePixels/2 + textWidth/2f,
                        noteTextPaint
                    )
                }

            }else if(value in 1..9){//draw number
                val row = cell.row
                val col = cell.col
                val valueString = cell.value.toString()
                val paintToUse = if(cell.isStartingCell) startingCellTextPaint else textPaint

                paintToUse.getTextBounds(valueString, 0, valueString.length, textBounds)
                val textWidth = textPaint.measureText(valueString)
                val textHeight = textBounds.height()

                canvas.drawText(valueString,
                    (col * cellSizePixels) + cellSizePixels/2 - textWidth/2,
                    (row * cellSizePixels) + cellSizePixels/2 + textHeight/2,
                    paintToUse)
            }
        }
    }

    override fun onTouchEvent(event: MotionEvent): Boolean {
        return when(event.action){
            MotionEvent.ACTION_DOWN ->{
                handleTouchEvent(event.x, event.y)
                true
            }
            else -> false
        }
    }

    private fun handleTouchEvent(x:Float, y: Float){
        val possibleSelectedRow = (y / cellSizePixels).toInt()
        val possibleSelectedCol = (x / cellSizePixels).toInt()
        listener?.onCellTouch(possibleSelectedRow, possibleSelectedCol) //refresh view when something will change
    }

    fun updateSelectedCellUI(row:Int, col:Int){
        selectedCol = col
        selectedRow = row
        invalidate()
    }

    fun updateCells(cells:List<Cell> ){
        this.cells = cells
        invalidate()
    }

    fun registerListener(listener: OnTouchListener){
        this.listener = listener
    }

    interface wrongValueInsertionToast{
        fun wrongValueInsertionToast()
    }

    interface OnTouchListener{// very weird for me, but works
        fun onCellTouch(row:Int, col:Int)
    }


}