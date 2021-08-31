package com.example.sudoku1.view

import android.content.Intent
import androidx.appcompat.app.AppCompatActivity
import android.os.Bundle
import android.widget.Button
import com.example.sudoku1.R
import com.example.sudoku1.viewmodel.PlaySudokuViewModel
import kotlinx.android.synthetic.main.activity_main.*
import kotlinx.android.synthetic.main.activity_settings.*

class SettingsActivity : AppCompatActivity() {

    private lateinit var settingsButtons: List<Button>
    var levelValue:Int = 0
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
            intent.putExtra("myInt", levelValue)
            val intValue: Int = intent.getIntExtra("myIntPlay", 0)
            println("received: $intValue")
            startActivity(intent)
        }

    }

    fun changeLevelValue(index:Int){
        levelValue = index
    }

}