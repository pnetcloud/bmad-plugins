---
name: data-pipeline-go
description: ETL data pipeline patterns for Go with Temporal orchestration and Kafka messaging. Use when building ingest, transform, or batch processing activities.
---

# Data Pipeline Patterns (Go + Temporal + Kafka)

Curated from generic ETL/stream/orchestration best practices, rewritten for our stack:
Go, `segmentio/kafka-go`, `pgx`, Temporal workflows.

## When to Use

- Building Kafka consumer activities (IngestBlocks, etc.)
- Designing batch INSERT pipelines (raw_* tables)
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
func (s *PgxRawStore) InsertRawSwaps(ctx context.Context, swaps []RawSwap) (int64, error) {
    batch := &pgx.Batch{}
    for _, sw := range swaps {
        batch.Queue(`
            INSERT INTO raw_swaps (chain_id, block_number, tx_hash, log_index,
                block_time, pair_address, factory, protocol,
                token0_address, token1_address,
                token0_in, token0_out, token1_in, token1_out,
                task_code, collected_at)
            VALUES ($1,$2,$3,$4,$5,$6,$7,$8,$9,$10,$11,$12,$13,$14,$15,NOW())
            ON CONFLICT DO NOTHING`,
            sw.ChainID, sw.BlockNumber, sw.TxHash, sw.LogIndex,
            sw.BlockTime, sw.PairAddress, sw.Factory, sw.Protocol,
            sw.Token0Address, sw.Token1Address,
            sw.Token0In, sw.Token0Out, sw.Token1In, sw.Token1Out,
            sw.TaskCode,
        )
    }
    br := s.pool.SendBatch(ctx, batch)
    defer br.Close()

    var inserted int64
    for range swaps {
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
❌ No ON CONFLICT → crashes on retried/duplicate blocks
❌ float64 for token amounts → precision loss (use TEXT for big.Int)
❌ SELECT * in production → specify columns explicitly
```

## 3. Temporal Long-Lived Workflow — ContinueAsNew

```go
const maxIterations = 100

func IngestWorkflow(ctx workflow.Context, state IngestState) error {
    for state.Iteration < maxIterations {
        var result IngestOutput
        err := workflow.ExecuteActivity(actCtx, "ingest_blocks", input).Get(ctx, &result)
        if err != nil {
            return err
        }

        state.TotalBlocks += result.Blocks
        state.Iteration++

        if result.Blocks == 0 {
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
| DB PK | `(chain_id, block_number, tx_hash, log_index)` |
| SQL | `ON CONFLICT DO NOTHING` (append-only) |
| Temporal | Same Workflow ID → singleton per network |
| Activity | Stateless — all state in DB/Kafka |

## 5. Data Validation at Ingest

```go
// Validate BEFORE batch INSERT — reject bad rows
func validateRawSwap(sw *RawSwap) error {
    if sw.TxHash == "" {
        return fmt.Errorf("empty tx_hash")
    }
    if sw.LogIndex < 0 || sw.LogIndex > 32767 { // smallint range
        return fmt.Errorf("log_index %d out of smallint range", sw.LogIndex)
    }
    if sw.PairAddress == "" {
        return fmt.Errorf("empty pair_address")
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
✅ Last ingested block — per network, freshness indicator
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

- [chaindata.prd.md §24.7-24.8](docs/00-planning/prd/datasets/chaindata.prd.md) — raw schema + ingest workflow
- [Epic 2 stories](docs/10-implementation/data-platform/) — implementation stories
- `services/migrator/schema/chaindata_raw.hcl` — Atlas schema
