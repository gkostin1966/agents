# DEEPBLUE-466 PR draft (concise)

## Summary

- Restore demo password login without changing production/workshop behavior.
- Introduce `auth.showPasswordLogin` as an exclusive toggle.

## Code Changes

- Add `showPasswordLogin?: boolean` to `AuthConfig`.
- Default `showPasswordLogin` to `false`.
- Inject `APP_CONFIG` in login component and derive `showPasswordLogin`.
- Replace hard-coded password filter with exclusive toggle in login template.
- Update login spec and add config documentation in `config.example.yml`.

## Operational Follow-up

- In `mlibrary/deepblue-documents-kube` demo frontend config, set:
  `DSPACE_AUTH_SHOWPASSWORDLOGIN=true`

## Testing

- Login component specs pass with non-interactive `ng test` flags.

