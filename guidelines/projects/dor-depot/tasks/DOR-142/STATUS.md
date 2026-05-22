# STATUS — DOR-142

## Last Updated
2026-05-22 — Full test suite run: 129 tests passed, 0 failures. One open subtask remains (developer sign-off).

## Current Branch
`DOR-142/ingest-validation-final`
(Also present locally: `DOR-142/ingest-validation-paranoid`, `DOR-142/ingest-validation-pull-request`, `DOR-142/get-content-file-fixity-records`)

## Open Tasks

- [ ] Verify with the developer that the task is complete

## Open Plans

| File | Purpose | Status |
|------|---------|--------|
| *(none)* | — | — |

## Recent Activity

- Session initialized; DOR-142 task directory and TODO/STATUS created for the first time.
- Branch `DOR-142/ingest-validation-final` has 13 commits above `main` covering full ingest validation implementation.
- `ingest-validation-paths.md` documents all code paths in `IntegrityService.performIngestValidation`.
- ADR-0001 added covering listener retry semantics.
- Full test suite run: **129 tests passed, 0 failures, 0 errors, 0 skipped** (`BUILD SUCCESSFUL`).

## Key Context

- `IntegrityService` now handles both `PerformIngestValidation` (listener + public API) and `BinContentsModified` (version-pinned auto-validation).
- Only `OcflNoSuchFileException` is swallowed per-file; all other runtime exceptions propagate for AMQP retry.
- `IngestValidation*` events (`Passed`, `DiscrepancyDetected`, `TargetMissing`) are intentionally **not** `@Externalized` — they are internal-only.
- `getContentFileFixityRecords` API was added to `PreservationGateway` / `OcflPreservationGateway` to fetch SHA-512 manifest digests without re-reading file bytes.
- Spotless clean as of HEAD (`722e18a`).

## Next Steps

1. Ask the developer to review the branch and sign off.
2. On sign-off, write `pr-summary.md` and open it for copy/paste.
3. Check off the final "Verify with the developer" subtask and create `DONE.md`.

