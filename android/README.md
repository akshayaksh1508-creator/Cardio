# Fire-Boltt Android App

Open this folder in Android Studio.

## Current implementation
This project provides the application architecture and BLE adapter scaffold.

It does NOT claim that one set of BLE UUIDs works for every Fire-Boltt watch.

For a real watch:
1. Pair the watch.
2. Confirm the exact model.
3. Inspect its available GATT services/characteristics or supported health-data API.
4. Add those UUIDs/decoders to `FireBolttBleAdapter.kt`.
5. Test notifications/read operations.
6. Map measurements to `HealthReading`.
7. POST normalized readings to the Python backend.

If the watch exposes health information only through its companion app/cloud service, use that supported data path instead of reverse-engineering private traffic.
