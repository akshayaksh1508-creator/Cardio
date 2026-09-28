# Fire-Boltt Integration Notes

## Key limitation
"Bluetooth smartwatch" does not guarantee that arbitrary Android apps can read every health metric.

Fire-Boltt models may use different companion apps and communication implementations. Some data may be available through standard BLE GATT, while other data may only be exposed through a manufacturer/companion ecosystem.

## Integration strategy

### Layer 1 — FireBolttAdapter
The Android application asks the adapter for normalized observations:

HealthReading(
    timestamp,
    heartRate,
    spo2,
    hrv,
    steps,
    activity,
    sleepMinutes,
    temperature
)

### Layer 2 — Model-specific implementation
For a selected Fire-Boltt model:
1. Pair the watch with Android.
2. Discover BLE services.
3. Identify standard or vendor-specific health characteristics.
4. Verify read/notify permissions.
5. Decode the payload.
6. Map it to HealthReading.

### Layer 3 — Backend
The backend never needs to know Fire-Boltt GATT UUIDs. It receives normalized JSON.

## Important
Do not copy UUIDs from another Fire-Boltt model and assume they work. Test the exact watch.

## Development fallback
The included DemoFireBolttAdapter generates readings so the Android UI and backend can be developed before the exact watch protocol is integrated.
