#!/usr/bin/env python3
"""Classify common CI/CD support signals from a workflow log.

This deliberately small utility demonstrates reproducible triage, structured
output, and clear escalation notes. It is not a replacement for platform logs
or StepSecurity runtime insights.
"""
from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Dict, List

RULES = {
    "permissions": [
        "resource not accessible by integration",
        "permission denied",
        "403",
        "github_token",
        "insufficient permission",
    ],
    "network_egress": [
        "connection refused",
        "could not resolve host",
        "network is unreachable",
        "timed out",
        "unexpected outbound",
        "egress",
    ],
    "authentication_or_secrets": [
        "bad credentials",
        "unauthorized",
        "401",
        "secret",
        "token not found",
        "authentication failed",
    ],
    "dependency_or_action": [
        "unable to resolve action",
        "module not found",
        "package not found",
        "version conflict",
        "dependency",
    ],
    "runner_environment": [
        "no space left on device",
        "command not found",
        "unsupported runner",
        "permission denied:",
        "exec format error",
    ],
}

RECOMMENDATIONS = {
    "permissions": "Compare workflow permissions with the action/API operation. Add only the minimum required scope.",
    "network_egress": "Identify the exact step, destination, protocol, and timing. Review Harden-Runner network insights before allowlisting.",
    "authentication_or_secrets": "Confirm secret name, scope, event type, environment protection, and whether forked PR rules apply.",
    "dependency_or_action": "Verify the action reference/SHA, package version, registry availability, and runtime compatibility.",
    "runner_environment": "Capture runner OS/image, shell, tool versions, disk state, and the failing command with exit code.",
}


def classify(text: str) -> Dict[str, object]:
    lowered = text.lower()
    matches: Dict[str, List[str]] = {}
    for category, patterns in RULES.items():
        found = [pattern for pattern in patterns if pattern in lowered]
        if found:
            matches[category] = found

    likely = sorted(matches, key=lambda key: len(matches[key]), reverse=True)
    return {
        "likely_categories": likely,
        "matched_signals": matches,
        "recommended_next_steps": [RECOMMENDATIONS[item] for item in likely],
        "escalation_checklist": [
            "Repository and workflow name",
            "Workflow run URL and timestamp",
            "Runner type and operating system",
            "Exact failing step and exit code",
            "Relevant redacted logs",
            "Expected versus actual behaviour",
            "Minimal reproduction or last known working commit",
            "Changes already tested and their results",
        ],
    }


def main() -> int:
    parser = argparse.ArgumentParser(description="Triage a GitHub Actions workflow log.")
    parser.add_argument("log_file", type=Path)
    args = parser.parse_args()

    if not args.log_file.exists():
        parser.error(f"File not found: {args.log_file}")

    result = classify(args.log_file.read_text(encoding="utf-8", errors="replace"))
    print(json.dumps(result, indent=2))

    return 0 if result["likely_categories"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
