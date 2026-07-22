# Plan: DEEPBLUE-466 password login toggle (concise)

## Scope

- Repository: `mlibrary/dspace-angular`
- Branch: `show-password-login`
- Goal: restore demo password login without changing production/workshop behavior.

## Implemented changes

- Add `showPasswordLogin?: boolean` to `AuthConfig`.
- Set default `showPasswordLogin: false` in app config.
- Inject `APP_CONFIG` into login component and compute `showPasswordLogin`.
- Change login template filter to an exclusive toggle condition.
- Update login component specs and document config in `config/config.example.yml`.

## Runtime behavior

| `showPasswordLogin` | Visible method |
|---------------------|----------------|
| `false`             | OIDC/non-password |
| `true`              | password only |

## Out-of-band follow-up

- In `mlibrary/deepblue-documents-kube` demo frontend configuration, set:
  `DSPACE_AUTH_SHOWPASSWORDLOGIN=true`
- Production/workshop should not set the variable.

## Verification checklist

- Login component specs pass in headless non-watch mode.
- Demo shows password form after config rollout.
- Production/workshop remain OIDC-only.
