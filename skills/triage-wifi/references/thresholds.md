# Wifi thresholds

A metric is a problem when it crosses these lines.

| Metric | Threshold | Direction |
|---|---|---|
| `retry_rate` | 0.15 | above |
| `noise_floor_dbm` | -85 | above |
| `client_rssi_dbm` | -70 | below |
| `channel_utilisation` | 0.60 | above |
| `disconnects_per_hour` | 3 | above |

Two or more breaches on one radio point at the radio; one breach on many clients points at the
air.
