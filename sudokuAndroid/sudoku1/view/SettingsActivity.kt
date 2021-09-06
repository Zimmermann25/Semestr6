package com.example.sudoku1.view

import android.content.Intent
import androidx.appcompat.app.AppCompatActivity
import android.os.Bundle
import android.widget.Button
import com.example.sudoku1.R
import kotlinx.android.synthetic.main.activity_settings.*

class SettingsActivity : AppCompatActivity() {

    private lateinit var settingsButtons: List<Button>
    var levelValue:Int = 0 //0 is code for easy, 1 for medium, 2 for hard, >2 for own grid
    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        setContentView(R.layout.activity_settings)

        settingsButtons = listOf(buttonEasy, buttonMedium, buttonHard, buttonOwnGrid)

        settingsButtons.forEachIndexed{ index, button -> //+1, because indexing starts from 0, and values from 1
            button.setOnClickListener{ changeLevelValue(index ) }
        }

        settingsButtonOk.setOnClickListener{
            println("SettingsActivityOnclick")
            val intent = Intent(this, PlaySudokuActivity::class.java)
            intent.putExtra("levelValue", levelValue) //send level code from settings to playSudokuActivity
            startActivity(intent)
        }

    }

    fun changeLevelValue(index:Int){
        levelValue = index
    }

}