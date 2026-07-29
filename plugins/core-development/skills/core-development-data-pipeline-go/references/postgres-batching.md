# PostgreSQL Batching with pgx

Use this reference when choosing or reviewing the database write path. Verify
the installed pgx major version and schema before copying an API shape.

## Contents

- Select the write method
- Batch result handling
- COPY and staging
- Conflict and transaction semantics
- Types and resource bounds

## Select the Write Method

Choose from evidence:

| Method | Appropriate when | Main risks |
| --- | --- | --- |
| Multi-row SQL | modest batches and explicit conflict clauses | statement size and parameter limits |
| `pgx.Batch` | several statements or per-row command tags in one round trip | result ordering and hidden close errors |
| `CopyFrom` | high-throughput insertion into a compatible table | all-or-nothing input errors and limited conflict handling |
| COPY to staging, then merge | high throughput plus validation, deduplication, or upsert | more schema and transaction complexity |

Benchmark representative row width, batch count, indexes, constraints, network,
and concurrency. A copied threshold from another system is not a tuning result.

## Batch Result Handling

`SendBatch` sends queued queries together. In pgx v5, the returned
`BatchResults` must be closed before the connection is reused. Consume results
in the same order as queued operations and check:

1. the error from every `Exec`, `Query`, or `QueryRow`;
2. row counts or returned identifiers when they are part of the contract;
3. the final error from `Close`.

Do not rely only on `defer results.Close()` when the returned close error can
change success. A safe shape makes the close result part of the returned error:

```go
results := tx.SendBatch(ctx, batch)

for range expectedResults {
    if _, err := results.Exec(); err != nil {
        _ = results.Close()
        return fmt.Errorf("execute batch result: %w", err)
    }
}
if err := results.Close(); err != nil {
    return fmt.Errorf("close batch results: %w", err)
}
```

Adapt transaction ownership and error joining to the repository's conventions.
Do not reuse the connection until results are closed.

## COPY and Staging

`CopyFrom` is designed for efficient bulk insertion. It does not directly
provide the full behavior of an `INSERT ... ON CONFLICT` statement. When the
delivery contract requires deduplication or upsert:

1. copy validated rows into a task-owned staging table;
2. merge into the destination with an explicit conflict target and update rule;
3. verify counts for copied, inserted, updated, rejected, and duplicated rows;
4. clean staging data within the same ownership and transaction model.

Do not interpolate untrusted table or column names. Use fixed schema identifiers
or pgx identifier quoting with an allowlisted design.

Check errors returned by `CopyFrom` and by a custom `CopyFromSource`. Bound
buffered input so a large message batch does not become an unbounded
`[][]any`.

## Conflict and Transaction Semantics

Define the intended atomic unit: one message, one partition batch, the complete
multi-partition fetch, or a derived aggregate. Avoid a transaction larger than
the actual consistency requirement.

For every conflict clause, name:

- the unique constraint or columns;
- whether an identical replay is ignored or returns existing state;
- what happens when the same key carries different content;
- ordering rules for versioned updates;
- which constraint failures remain errors.

Do not use a blanket conflict-ignore clause as a substitute for validation.
Check PostgreSQL error codes where error classification affects retry or
quarantine.

## Types and Resource Bounds

- Preserve exact numeric values with types that match the domain and schema; do
  not route arbitrary-precision values through `float64`.
- Bounds-check narrowing conversions before assigning database types.
- Specify columns explicitly for inserts and reads.
- Bound batch rows, encoded bytes, statement parameters, transaction duration,
  and concurrent connections.
- Keep cancellation and statement timeouts shorter than the overall Activity or
  process shutdown deadline.

## Primary Reference

- [`pgx/v5` package documentation](https://pkg.go.dev/github.com/jackc/pgx/v5)
