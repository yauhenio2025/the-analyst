# Note: Close Read Public Host Topology Evidence

Date: 2026-04-13
Program: Dynamic Bespoke Apps Platformization
Related Scope:
- `communications/MEMO_2026-04-13_close_read_public_host_topology_and_admitted_family_umbrella_publication_scope.md`

## Purpose

Freeze the real public host topology and the repo-facing config truth used during the live Close Read public-surface tranche.

## Live Host Truth

The live public pair is:

- frontend: `https://the-critic-1.onrender.com`
- API: `https://the-critic.onrender.com`

This is the pair that served the public Close Read route matrix during the browser-proof run.

## Deployment Evidence

The public frontend bundle progressed through these live `asset-manifest.json` fingerprints during the tranche:

- `main.23779f37.js`
- `main.c1fb1a16.js`
- `main.1d26cf69.js`

Render deploy history nuance:

- `232c368` was part of the rollout sequence on `master`, but its frontend deploy attempt build-failed
- the later commits
  - `1d726db`
  - `5f0260f`
  - `10cec95`
  - `4a87971`
  - `938c09f`
  completed successfully, with `938c09f` serving the final verified public bundle

The final browser-proof run was taken against:

- `main.1d26cf69.js`

## Repo-Facing Config Truth

### Tracked env/config source

The tracked frontend env source already points at the real API host:

- `the-critic/webapp/.env`
- `REACT_APP_API_URL=https://the-critic.onrender.com/api`

### Documentary deployment config

The dirty local main-tree `the-critic/render.yaml` was still stale at the start of execution and advertised:

- `benanav-api`
- `benanav-web`
- `https://benanav-api.onrender.com`

The deployed-source-aligned worktree carried the corrected documentary version:

- service names:
  - `the-critic`
  - `the-critic-1`
- frontend API env value:
  - `https://the-critic.onrender.com/api`

That corrected documentary file was then synced back into the dirty main tree locally.

## Operational Interpretation

`render.yaml` should be read as documentary truth for repo readers, not as proof that the current live Render services are blueprint-managed.

The live services in this tranche were treated as dashboard-managed services with auto-deploy from `master`.

## Bottom Line

The public host-topology ambiguity is now closed enough for planning purposes:

- the real live pair is `the-critic-1` plus `the-critic`
- route-level `200` was not treated as sufficient proof
- the final public Close Read completion record is grounded in hydrated browser proof on that pair
