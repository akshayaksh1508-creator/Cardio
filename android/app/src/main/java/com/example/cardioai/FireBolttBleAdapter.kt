package com.example.cardioai

import android.bluetooth.*
import android.bluetooth.le.*
import android.content.Context
import android.os.ParcelUuid

/**
 * Generic BLE scaffold.
 *
 * Do NOT assume these callbacks provide health data for every Fire-Boltt model.
 * The exact model's services/characteristics must be identified before decoding
 * packets.
 */
class FireBolttBleAdapter(private val context: Context) : FireBolttAdapter {

    private val bluetoothManager =
        context.getSystemService(Context.BLUETOOTH_SERVICE) as BluetoothManager

    private val adapter = bluetoothManager.adapter
    private var scanner: BluetoothLeScanner? = null
    private var callback: ScanCallback? = null
    private var gatt: BluetoothGatt? = null
    private var listener: FireBolttAdapter.Listener? = null

    override fun setListener(listener: FireBolttAdapter.Listener) {
        this.listener = listener
    }

    override fun startScan() {
        scanner = adapter.bluetoothLeScanner
        callback = object : ScanCallback() {
            override fun onScanResult(type: Int, result: ScanResult) {
                val name = result.device.name ?: "Unknown BLE device"
                listener?.onDeviceFound(name, result.device.address)
            }

            override fun onScanFailed(errorCode: Int) {
                listener?.onError("BLE scan failed: $errorCode")
            }
        }
        scanner?.startScan(callback)
    }

    override fun stopScan() {
        callback?.let { scanner?.stopScan(it) }
        callback = null
    }

    override fun connect(deviceAddress: String) {
        val device = adapter.getRemoteDevice(deviceAddress)
        gatt = device.connectGatt(context, false, object : BluetoothGattCallback() {
            override fun onConnectionStateChange(
                g: BluetoothGatt,
                status: Int,
                newState: Int
            ) {
                if (newState == BluetoothProfile.STATE_CONNECTED) {
                    listener?.onConnected(device.name ?: deviceAddress)
                    g.discoverServices()
                } else if (newState == BluetoothProfile.STATE_DISCONNECTED) {
                    listener?.onDisconnected()
                }
            }

            override fun onServicesDiscovered(g: BluetoothGatt, status: Int) {
                if (status != BluetoothGatt.GATT_SUCCESS) {
                    listener?.onError("Service discovery failed: $status")
                    return
                }

                // TODO:
                // Identify the exact Fire-Boltt model's health-data
                // characteristics and register notifications/read them.
            }

            override fun onCharacteristicChanged(
                g: BluetoothGatt,
                characteristic: BluetoothGattCharacteristic
            ) {
                // TODO: decode model-specific packet into HealthReading.
            }
        })
    }

    override fun disconnect() {
        gatt?.disconnect()
        gatt?.close()
        gatt = null
    }
}
