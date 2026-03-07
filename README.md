# Code Factory

Shared control-plane for risk-aware, agent-driven development.

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

- Sensitive policy details should live in repo-local `.code-factory/config.json` and `.code-factory/policy.json` overrides.
- Organization-level rulesets still need repository or organization admin permissions to manage.
