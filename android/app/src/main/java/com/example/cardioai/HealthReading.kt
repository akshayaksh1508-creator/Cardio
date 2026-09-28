package com.example.cardioai

data class HealthReading(
    val timestamp: Long,
    val heartRate: Int? = null,
    val spo2: Int? = null,
    val hrv: Int? = null,
    val steps: Int? = null,
    val activity: String? = null,
    val sleepMinutes: Int? = null,
    val temperature: Double? = null
)
