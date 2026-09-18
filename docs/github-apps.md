# Creating the `lwp-claude` and `lwp-codex` GitHub Apps

This is an owner-only, web-UI action. It is not scriptable: GitHub does not
offer an API to create an App's registration itself (only to manage an
already-created App), so this procedure is manual, step by step, done twice
(once per app). Do it once for `lwp-claude`, then repeat every step for
`lwp-codex`.

The two App definitions already checked into this repo —
`.github/apps/lwp-claude.json` and `.github/apps/lwp-codex.json` — are the
source of truth for every value below. If this document and those files
ever disagree, the JSON files win; re-derive this document from them.

## Where to create them

Both apps are **org-owned**, not personal. Create each one at:

```
https://github.com/organizations/LEAPWare-Software/settings/apps/new
```

(Settings → Developer settings → GitHub Apps → New GitHub App, from the
`LEAPWare-Software` organization's settings, not a personal account's.)

## Values to enter, per app

### `lwp-claude`

| Field | Value |
|---|---|
| GitHub App name | `lwp-claude` |
| Homepage URL | `https://github.com/LEAPWare-Software/LEAPWare-Pulse` |
| Description | `LEAPWare Pulse CI/merge identity for Claude Code sessions working in this repo. Least-privilege: no org permissions, webhook inactive.` |
| Callback / redirect URL | `https://github.com/LEAPWare-Software/LEAPWare-Pulse` |
| Webhook — Active | **Unchecked (inactive).** |
| Webhook URL | `https://example.invalid/not-configured` (placeholder only, since the webhook is inactive; do not point it at a real endpoint) |
| Where can this GitHub App be installed? | **Only on this account** (the app is not public — leave "Any account" unchecked) |

Repository permissions (set exactly these levels; leave every other
repository permission at "No access"):

| Permission | Level |
|---|---|
| Contents | Read and write |
| Pull requests | Read and write |
| Checks | Read-only |
| Metadata | Read-only (this one is mandatory and GitHub sets it automatically) |

Organization permissions: **none.** Leave every organization permission
at "No access."

Subscribe to events: **none.** Leave every event checkbox unchecked (the
webhook is inactive, so subscribed events would not be delivered anywhere
useful).

### `lwp-codex`

Identical to `lwp-claude` above, except:

| Field | Value |
|---|---|
| GitHub App name | `lwp-codex` |
| Description | `LEAPWare Pulse CI/merge identity for Codex sessions working in this repo. Least-privilege: no org permissions, webhook inactive.` |

Every other field (Homepage URL, callback URL, webhook inactive, placeholder
webhook URL, installable only on this account, repository permissions,
organization permissions, subscribed events) is the same as `lwp-claude`.

## After creation: the private key and App ID

Each app's settings page shows an **App ID** at the top, and has a
"Generate a private key" button that downloads a `.pem` file.

**What to do with them:** as of this writing, nothing in this repository
consumes an App ID or a private key. `.github/workflows/*.yml` (`ci.yml`,
`handoff.yml`, `release.yml`) reference no secret name for either app, and
no script under `scripts/` reads one. Do not invent a secret name or wire
one in speculatively — that wiring is D1+ work, not part of this
procedure. For now:

- Save the downloaded `.pem` file and the App ID somewhere secure (a
  password manager or the org's secret store), outside this repository.
- Do not commit the `.pem` file anywhere, and do not paste its contents
  into an issue, PR, or commit message.
- When a later phase actually needs the App ID or key (for example, to run
  CI or merges under the app's identity instead of a personal token), that
  phase's plan entry should say which GitHub Actions secret name to store
  them under, and this document should be updated to point at that secret
  name once it exists.

## After creation: install the app on the repository

Creating an App only registers it; it must then be **installed** on
`LEAPWare-Software/LEAPWare-Pulse` before it can act on the repo.

1. From the app's settings page, use "Install App" (or, from the org's
   installed-apps list, install it and select the `LEAPWare-Pulse`
   repository specifically rather than "All repositories").
2. Repeat for the other app.

## Verifying afterwards

Run both of these and confirm each app appears with access to this
repository:

```
gh api orgs/LEAPWare-Software/installations --jq '.installations[].app_slug'
```

should list `lwp-claude` and `lwp-codex`.

```
gh api repos/LEAPWare-Software/LEAPWare-Pulse/installation --jq '{app_slug: .app_slug, id: .id}'
```

confirms a specific app's installation is scoped to this repository (this
endpoint returns the installation for the credential you're authenticated
as; check it once while authenticated as each app's installation, or use
the org-level `installations` list above plus the app's own "Advanced" →
"Recent Deliveries" / "Configure" page, which shows exactly which
repositories it's installed on).

Also confirm, on each app's settings page directly:

- Webhook shows **Inactive**.
- Permissions match the table above exactly (Contents: write, Pull
  requests: write, Checks: read, Metadata: read; nothing else).
- No organization permissions are granted.
- No events are subscribed.
- "Public" is off (the app page should say it's only installable on the
  `LEAPWare-Software` account, not listed publicly).

G-PUB's Apps sub-item is done only once both apps exist, are installed on
`LEAPWare-Pulse`, and pass every check above.
