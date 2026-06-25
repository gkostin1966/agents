# DEEPBLUE-466 DEV Call Checklist (One-Page)

Use this during a live MITS troubleshooting call. Keep it short, timestamped, and evidence-first.

## 0) Start

- [ ] Confirm call date/time + timezone:
- [ ] Confirm participants:
- [ ] Confirm Elements URL: `https://dev.umich.elements.symplectic.org/`
- [ ] Confirm Elements username used:

## 1) Snapshot Current Config (no changes yet)

- [ ] DSpace version = `DSpace 7.0+`
- [ ] API Base URL = `https://backend.demo.deepblue-documents.lib.umich.edu/server`
- [ ] OAI-PMH URL = `https://backend.demo.deepblue-documents.lib.umich.edu/server/oai/request`
- [ ] REST account email currently configured:
- [ ] Automated Metadata Updates state (ON/OFF):
- [ ] Screenshot taken of settings page

## 2) Baseline Repro

- [ ] Attempt one deposit with no config changes
- [ ] Record timestamp:
- [ ] Record item identifier/title:
- [ ] Record HTTP status (`401` / `403` / other):
- [ ] Capture failing endpoint URL:
- [ ] Capture response snippet / error text:

## 3) Credential + Permission Quick Checks

- [ ] REST account in use is expected for demo (`deepblue@umich.edu`) or mismatch noted
- [ ] Target collection identified
- [ ] Confirm account has collection deposit permission (yes/no/unknown)

## 4) Controlled Toggle Test (Automated Metadata Updates)

- [ ] Run one attempt in current state (ON or OFF)
- [ ] Toggle setting
- [ ] Run one attempt in opposite state
- [ ] Record status transition (`403 -> 401`, `401 -> 403`, no change)
- [ ] Revert setting to original state

## 5) Decision

- [ ] Most likely cause selected:
  - [ ] credential mismatch
  - [ ] permission issue
  - [ ] endpoint/config mismatch
  - [ ] unknown, needs server-side logs

## 6) Send Back to MITS (same day)

- [ ] Email includes:
  - [ ] config snapshot
  - [ ] two timestamped attempts
  - [ ] endpoint + status + response excerpts
  - [ ] permission check result
  - [ ] explicit ask for server log correlation at timestamps

