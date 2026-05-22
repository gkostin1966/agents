## Finalize Ingest Validation

Complete and ship the ingest validation feature on branch `DOR-142/ingest-validation-final`.

- [x] Add `getContentFileFixityRecords` API to `PreservationGateway` / `OcflPreservationGateway`
- [x] Implement `performIngestValidation` in `IntegrityService` using fixity-record gateway API
- [x] Handle both Curio and GLAM header digest shapes in `extractDigest`
- [x] Support versioned (pinned) validation triggered by `BinContentsModified`
- [x] Harden edge-case handling (missing headers, unreadable headers, missing fixity records)
- [x] Narrow exception handling — only swallow `OcflNoSuchFileException`; let other runtime exceptions propagate for retry
- [x] Add `@ApplicationModuleListener` retry semantics (ADR-0001)
- [x] Extract shared test constants into `IngestValidationTestConstants`
- [x] Add `ingest-validation-paths.md` path documentation
- [x] Run full test suite and confirm all tests pass
- [ ] Verify with the developer that the task is complete

