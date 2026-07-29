# Customer Troubleshooting Runbook

## Goal

Resolve technical onboarding and production issues with enough evidence that the
customer receives a clear next step and Engineering receives a reproducible case.

## 1. Establish impact

- Which repositories, workflows, branches, and users are affected?
- Is the issue blocking onboarding, all workflow runs, or one job/step?
- When did it start, and what was the last known successful run?
- Did any workflow, runner, action, permission, network, or secret configuration change?

## 2. Collect evidence

Capture the workflow run URL, timestamp, runner type/OS, exact failing step,
exit code, redacted logs, expected behaviour, actual behaviour, and recent changes.

Never request secrets or unredacted credentials in Slack, tickets, or screenshots.

## 3. Reproduce safely

1. Start from the smallest affected workflow/job.
2. Confirm that Harden-Runner is the first step.
3. Re-run in `egress-policy: audit` while collecting runtime insights.
4. Compare a failing run with the last successful run.
5. Change one variable at a time.
6. Record every test and result.

## 4. Common issue paths

### Permission failure

Typical signals: HTTP 403, "Resource not accessible by integration", or an API
operation that requires a missing `GITHUB_TOKEN` scope.

Check workflow-level and job-level permissions. Add only the minimum required
permission and explain why it is needed.

### Unexpected or blocked network call

Identify the exact step, process, destination, protocol, and whether the call is
expected. Review audit-mode evidence before changing an allowlist or moving to
block mode.

### Secret or authentication failure

Confirm the secret name and scope, event type, environment protection rules,
forked pull-request behaviour, and whether the credential is expired or rotated.

### Action or dependency failure

Verify the pinned action reference/SHA, package/version, registry availability,
runtime compatibility, and any upstream release or compromise notice.

### Runner-specific failure

Capture runner image, architecture, shell, disk state, installed tools, network
configuration, and differences between hosted and self-hosted runners.

## 5. Escalate with quality

A good Engineering escalation includes:

- Customer impact and urgency
- Exact reproduction steps
- Workflow/run links and timestamps
- Redacted logs and screenshots
- Expected versus actual result
- Scope: one repo, multiple repos, hosted/self-hosted
- Suspected component and evidence
- Tests already performed
- Workaround status
- Clear question for Engineering

## Example customer update

"We reproduced the failure in the publish step and isolated it to the workflow's
token permissions rather than the runner installation. The API request is
returning 403 because the job currently has read-only repository access. We are
testing the smallest required permission change and will share the exact YAML
diff. No secret values are needed from your team."
