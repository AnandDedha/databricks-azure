# Operations Runbook

## Common Issues
- **Ingestion stops**: check Auto Loader checkpoint (`_checkpoints`) for corruption; restart with `trigger(once)` or repair.
- **Schema drift**: add schema hints or DLT expectations to quarantine rows.
- **Late data**: leverage watermarks for streaming or partition-overwrite for batch backfills.
- **Table bloat**: schedule `OPTIMIZE` and `VACUUM` with compliant retention.

## Performance & Cost
- Use **Photon**.
- Partition by date; avoid tiny files (use `OPTIMIZE` on Silver/Gold).
- Right-size job clusters; cap autoscaling.
