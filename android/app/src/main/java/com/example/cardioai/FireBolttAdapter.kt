package com.example.cardioai

interface FireBolttAdapter {
    fun startScan()
    fun stopScan()
    fun connect(deviceAddress: String)
    fun disconnect()
    fun setListener(listener: Listener)

    interface Listener {
        fun onDeviceFound(name: String, address: String)
        fun onConnected(name: String)
        fun onDisconnected()
        fun onHealthReading(reading: HealthReading)
        fun onError(message: String)
    }
}
