package com.example.cardioai

import android.Manifest
import android.os.Build
import android.os.Bundle
import android.widget.*
import androidx.activity.ComponentActivity
import androidx.core.app.ActivityCompat

class MainActivity : ComponentActivity(), FireBolttAdapter.Listener {

    private lateinit var adapter: FireBolttBleAdapter
    private lateinit var status: TextView

    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)

        val layout = LinearLayout(this).apply {
            orientation = LinearLayout.VERTICAL
            setPadding(32, 32, 32, 32)
        }

        status = TextView(this).apply {
            text = "Fire-Boltt Cardio AI\nReady to scan"
            textSize = 18f
        }

        val scan = Button(this).apply {
            text = "Scan Fire-Boltt"
            setOnClickListener { adapter.startScan() }
        }

        layout.addView(status)
        layout.addView(scan)
        setContentView(layout)

        adapter = FireBolttBleAdapter(this)
        adapter.setListener(this)

        requestBluetoothPermissions()
    }

    private fun requestBluetoothPermissions() {
        if (Build.VERSION.SDK_INT >= Build.VERSION_CODES.S) {
            ActivityCompat.requestPermissions(
                this,
                arrayOf(
                    Manifest.permission.BLUETOOTH_SCAN,
                    Manifest.permission.BLUETOOTH_CONNECT
                ),
                100
            )
        } else {
            ActivityCompat.requestPermissions(
                this,
                arrayOf(Manifest.permission.ACCESS_FINE_LOCATION),
                101
            )
        }
    }

    override fun onDeviceFound(name: String, address: String) {
        runOnUiThread {
            status.text = "Found: $name\n$address\nTap integration code to connect."
        }
    }

    override fun onConnected(name: String) {
        runOnUiThread { status.text = "Connected: $name\nDiscovering services..." }
    }

    override fun onDisconnected() {
        runOnUiThread { status.text = "Disconnected" }
    }

    override fun onHealthReading(reading: HealthReading) {
        runOnUiThread {
            status.text = "HR: ${reading.heartRate}\nSpO₂: ${reading.spo2}\nHRV: ${reading.hrv}"
        }
    }

    override fun onError(message: String) {
        runOnUiThread { status.text = "Error: $message" }
    }
}
