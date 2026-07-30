---
name: core-development-data-pipeline-go
description: ETL data pipeline patterns for Go with Temporal orchestration and Kafka messaging. Use when building ingest, transform, or batch processing activities.
---

# Data Pipeline Patterns (Go + Temporal + Kafka)

Curated from generic ETL/stream/orchestration best practices for a stack using
Go, `segmentio/kafka-go`, `pgx`, Temporal workflows.

## When to Use

- Building Kafka consumer activities (for example, ProcessBatch)
- Designing batch INSERT pipelines for append-only ingest tables
- Implementing idempotent data processing
- Configuring Temporal workflows for long-lived data pipelines

## 1. Kafka Consumer — Manual Commit After DB Write

```go
// At-least-once: commit AFTER successful DB write.
// ON CONFLICT DO NOTHING handles duplicates from re-delivery.
func (a *Activities) IngestBatch(ctx context.Context, batchSize int) (int, error) {
    var msgs []kafka.Message
    for i := 0; i < batchSize; i++ {
        msg, err := a.reader.FetchMessage(ctx)
        if err != nil {
            break // timeout or EOF — process what we have
        }
        msgs = append(msgs, msg)
    }
    if len(msgs) == 0 {
        return 0, nil
    }

    // 1. Parse + transform
    rows := decodeMessages(msgs)

    // 2. DB write (batch INSERT)
    if err := a.store.BatchInsert(ctx, rows); err != nil {
        return 0, err // Temporal retries; Kafka offsets NOT committed
    }

    // 3. Commit offsets ONLY after DB success
    if err := a.reader.CommitMessages(ctx, msgs...); err != nil {
        // DB written but offset not committed = re-delivery next time
        // ON CONFLICT DO NOTHING handles the dupe — safe
        return len(msgs), nil
    }
    return len(msgs), nil
}
```

### Anti-patterns

```
❌ Commit offsets before DB write → data loss on crash
❌ Auto-commit enabled → offsets advance before processing
❌ FetchMessage without timeout → blocks activity forever
❌ One INSERT per message → N round-trips instead of 1
```

## 2. Batch INSERT — pgx.Batch with ON CONFLICT

```go
func (s *PgxStore) InsertRecords(ctx context.Context, records []IngestRecord) (int64, error) {
    batch := &pgx.Batch{}
    for _, record := range records {
        batch.Queue(`
            INSERT INTO ingest_records (
                source_id, sequence, event_id, item_index,
                occurred_at, entity_key, payload, collected_at
            )
            VALUES ($1,$2,$3,$4,$5,$6,$7,NOW())
            ON CONFLICT DO NOTHING`,
            record.SourceID, record.Sequence, record.EventID, record.ItemIndex,
            record.OccurredAt, record.EntityKey, record.Payload,
        )
    }
    br := s.pool.SendBatch(ctx, batch)
    defer br.Close()

    var inserted int64
    for range records {
        ct, err := br.Exec()
        if err != nil {
            return inserted, fmt.Errorf("batch exec: %w", err)
        }
        inserted += ct.RowsAffected()
    }
    return inserted, nil
}
```

### Anti-patterns

```
❌ Individual INSERTs in a loop → N round-trips
❌ INSERT ON CONFLICT UPDATE for append-only data → wasted writes
❌ No ON CONFLICT → crashes on retried/duplicate records
❌ float64 for large exact values → precision loss (use an exact representation)
❌ SELECT * in production → specify columns explicitly
```

## 3. Temporal Long-Lived Workflow — ContinueAsNew

```go
const maxIterations = 100

func IngestWorkflow(ctx workflow.Context, state IngestState) error {
    for state.Iteration < maxIterations {
        var result IngestOutput
        err := workflow.ExecuteActivity(actCtx, "process_batch", input).Get(ctx, &result)
        if err != nil {
            return err
        }

        state.TotalRecords += result.Records
        state.Iteration++

        if result.Records == 0 {
            _ = workflow.Sleep(ctx, 1*time.Second) // no data, backoff
        }
    }
    // Reset iteration, keep cumulative state
    state.Iteration = 0
    return workflow.NewContinueAsNewError(ctx, IngestWorkflow, state)
}
```

### Anti-patterns

```
❌ Unbounded loop without ContinueAsNew → event history grows forever
❌ Sleep in activity instead of workflow → blocks worker slot
❌ No heartbeat in long activity → Temporal kills it silently
❌ State lost on ContinueAsNew → always pass state forward
```

## 4. Idempotency Checklist

| Layer | Technique |
|-------|-----------|
| Kafka | Manual offset commit after processing |
| DB PK | Stable source, sequence, event, and item identity |
| SQL | `ON CONFLICT DO NOTHING` (append-only) |
| Temporal | Same Workflow ID → singleton per logical source |
| Activity | Stateless — all state in DB/Kafka |

## 5. Data Validation at Ingest

```go
// Validate BEFORE batch INSERT — reject bad rows
func validateRecord(record *IngestRecord) error {
    if record.EventID == "" {
        return fmt.Errorf("empty event_id")
    }
    if record.ItemIndex < 0 || record.ItemIndex > 32767 { // smallint range
        return fmt.Errorf("item_index %d out of smallint range", record.ItemIndex)
    }
    if record.EntityKey == "" {
        return fmt.Errorf("empty entity_key")
    }
    return nil
}
```

### Anti-patterns

```
❌ Load without validation → corrupt rows in DB
❌ Silent drops → log rejected rows for debugging
❌ uint64 → smallint without bounds check → runtime panic
```

## 6. Monitoring Checklist

```
✅ Kafka consumer lag — growing lag = ingest slower than collect
✅ Batch size histogram — track actual vs configured batch size
✅ INSERT rate — rows/sec per table
✅ ON CONFLICT skipped rate — high = too many duplicates
✅ Activity duration p95 — trending up = performance issue
✅ Workflow iteration count — sanity check for ContinueAsNew
✅ Last ingested sequence — per source, freshness indicator
```

## 7. Graceful Shutdown

```go
// KafkaReader must be closed on worker shutdown
type kafkaReaderAdapter struct {
    reader *kafka.Reader
}

func (a *kafkaReaderAdapter) Close() error {
    return a.reader.Close() // commits final offsets, releases consumer group
}

// Register cleanup in worker lifecycle
defer kafkaReader.Close()
```

## Related

- Review the owning project's data contract for schema and ingest workflow.
- Review its delivery stories or equivalent acceptance records.
- Review the repository's schema or migration source of truth.
