# Code Factory Rollout Status

Last updated: 2026-03-07

## Certification Bar

A repo is considered certified when all of the following are true:

- `code-factory-pr.yml` is present on `main`
- a post-rollout pull request emits `risk-policy-gate`, `CI Pipeline`, and `Review Agent`
- the checks run on the pull request head, not only on `push`
- at least one recent merge completed with the current Code Factory workflow active
- repo-native required checks remain understood and intentionally enforced

## Current Status

| Repo | Rollout on `main` | Recent PR emits Code Factory checks | Current state | Notes |
| --- | --- | --- | --- | --- |
| `ironprose-cli` | Yes | Yes | Certified | Recent PRs `#48`, `#49`, and repin `#53` emit all three checks on `pull_request`. |
| `ironprose` | Yes | Yes after refresh | Pending merge of repin | Repin `#201` refreshes workflow registration and restores PR-head checks. |
| `local-weather` | Yes | Yes on repin | Pending merge of repin | Older PR `#92` predates rollout and is not governed without a new push. |
| `bench` | Yes | Yes on repin | Pending merge of repin | Rollout is active; repin `#4` aligns it to `v1.0.0`. |
| `benchcut-logic` | Yes | Yes | Partial | Code Factory works, but native `visual-regression` still needs explicit governance. |
| `mcp-proxy` | Yes | Yes on repin | Pending merge of repin | Repin `#3` removes stale Browser Evidence wiring. |
| `stimulus` | Yes | Yes on repin | Pending repo-native CI cleanup | Repin `#120` aligns workflow shape and disables stale Browser Evidence config. |
| `tracios` | No | No | Rollout PR still open | Needs rollout PR `#536` merged before certification. |
| `factory` | No | No | Rollout PR still open | Repo-native CI still failing on rollout PR `#7`. |

## Org Enforcement

- `code-factory-baseline` is active.
- `code-factory-required-checks` remains in `evaluate`.
- The required-check ruleset should stay in `evaluate` until at least the certified repos above are merged on the current shared release and observed on normal pull requests.
