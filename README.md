# Code Factory

Shared control-plane for risk-aware, agent-driven development across the `benchcutlogic` organization.

## What lives here

- Reusable GitHub Actions workflows
- Default risk and merge policy
- Lightweight helper scripts used by those workflows

## Expected repo layout

Each participating repository should include:

- `.github/workflows/code-factory-pr.yml`
- `.code-factory/config.json`
- optional `.code-factory/policy.json`

## Shared checks

- `risk-policy-gate`
- `CI Pipeline`
- `Browser Evidence`
- `Review Agent`

## Notes

- Org-wide rulesets still need a token with `admin:org`.
- Repository rollout can still proceed with repo admin access alone.
