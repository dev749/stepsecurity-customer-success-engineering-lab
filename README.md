# StepSecurity Customer Success Engineering Lab

A compact portfolio project by Dev Mehta demonstrating how I approach technical
onboarding, issue reproduction, structured triage, runbooks, and communication
for GitHub Actions customers.

## What is included

- `.github/workflows/secure-ci.yml`: GitHub Actions workflow with Harden-Runner
  as the first step, audit-mode egress monitoring, pinned action SHAs, and
  least-privilege repository permissions.
- `scripts/diagnose_log.py`: Small Python utility that classifies common support
  signals and produces a structured escalation checklist.
- `samples/workflow.log`: Sanitized sample log.
- `CUSTOMER_RUNBOOK.md`: Customer and Engineering troubleshooting playbook.

## Run locally

```bash
python scripts/diagnose_log.py samples/workflow.log
```

The command returns likely issue categories, matched signals, recommended next
steps, and an escalation checklist.

## Run on GitHub

1. Create a new public GitHub repository.
2. Upload all files while preserving the `.github/workflows` path.
3. Enable GitHub Actions if prompted.
4. Open the Actions tab and run **Secure CI Troubleshooting Lab**.
5. Review the job summary and Harden-Runner security insights.

## Design choices

- Harden-Runner is placed first so it can monitor the remaining job.
- Audit mode is used for observation before enforcement.
- `contents: read` demonstrates least-privilege `GITHUB_TOKEN` configuration.
- Third-party actions are pinned to commit SHAs to reduce tag-movement risk.
- The log utility is intentionally small and explainable; it supports triage,
  not automatic remediation.

## Scope and honesty

This is a self-directed learning and portfolio lab, not a production
StepSecurity deployment. It demonstrates my troubleshooting method and current
hands-on development in GitHub Actions, Python, CI/CD, and software supply chain
security.
