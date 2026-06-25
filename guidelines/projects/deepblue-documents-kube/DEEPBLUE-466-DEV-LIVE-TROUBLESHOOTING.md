# DEEPBLUE-466 DEV Live Troubleshooting Runbook

Use this runbook during a live session in Elements DEV to isolate `401` vs `403` deposit failures and collect actionable evidence for MITS.

## Scope

- Environment: Elements DEV (`https://dev.umich.elements.symplectic.org/`)
- Integration target: Deep Blue demo backend
- Objective: Identify whether failure is caused by credentials, permissions, endpoint mismatch, or crosswalk/license configuration.

## Preconditions

- You can sign in to Elements DEV with your assigned account.
- You can access the DSpace data source settings page in Elements DEV.
- You have one known test record ready to attempt deposit.

## Baseline values to confirm

Confirm these values before testing:

- DSpace version: `DSpace 7.0+`
- API Base URL: `https://backend.demo.deepblue-documents.lib.umich.edu/server`
- OAI-PMH URL: `https://backend.demo.deepblue-documents.lib.umich.edu/server/oai/request`
- REST account email: expected demo service account `deepblue@umich.edu` (verify what is currently configured)

## Live troubleshooting procedure

1. Capture session start metadata
   - Date/time with timezone
   - Elements username used
   - Data source name

2. Capture current data source configuration (before changes)
   - Screenshot settings page
   - Record all fields listed in "Baseline values to confirm"
   - Record whether Automated Metadata Updates is enabled or disabled

3. Reproduce baseline failure
   - Attempt one deposit with no settings changes
   - Record resulting error code (`401` or `403`)
   - Capture timestamp and item identifier used

4. Collect request/response diagnostics
   - In browser dev tools, capture failing network request details:
     - Request URL
     - Method
     - Response status
     - Response body snippet (if present)
   - If available, collect Elements-side error/log excerpt for the same timestamp

5. Verify credentials path
   - Confirm which REST account email is configured
   - If not `deepblue@umich.edu`, note mismatch explicitly
   - Confirm password in use is current for the configured account

6. Verify permissions path
   - Confirm configured REST account has deposit rights to the configured target collection
   - If collection-level permissions are unclear, record that as a blocker

7. Controlled toggle test (Automated Metadata Updates)
   - Run one deposit with setting OFF
   - Run one deposit with setting ON
   - Record whether status transitions `403` <-> `401`
   - Revert to original state after test

8. Produce session summary for MITS
   - Most likely root-cause category:
     - credential mismatch
     - insufficient account permissions
     - endpoint/config mismatch
     - unknown (needs server logs)
   - Include exact evidence references (screenshots/log excerpts/timestamps)

## Evidence template (copy/paste)

```text
Session date/time (TZ):
Elements user:
Data source:
Automated Metadata Updates (start state):

Current config:
- DSpace version:
- API Base URL:
- OAI-PMH URL:
- REST account email:

Attempt A (baseline):
- Timestamp:
- Item ID/title:
- HTTP status:
- Failing endpoint:
- Response excerpt:

Attempt B (toggle state):
- Toggle state:
- Timestamp:
- HTTP status:
- Failing endpoint:
- Response excerpt:

Permission check:
- Target collection:
- Account has deposit permission? (yes/no/unknown)

Conclusion:
- Probable cause:
- Requested follow-up from MITS:
```

## Handoff checklist

- Send MITS one concise email with:
  - confirmed config values
  - two timestamped failing attempts
  - endpoint + status + response excerpts
  - permission check result
- Offer a 30-minute live follow-up if server-side logs are needed.

