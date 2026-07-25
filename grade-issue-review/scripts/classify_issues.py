#!/usr/bin/env python3
"""Derive retention dispositions for reviewed issues."""

import argparse
import json
import sys
from collections import Counter
from pathlib import Path

SEVERITIES = {"blocker", "material", "cosmetic"}
CONFIDENCES = {"confirmed", "supported", "speculative"}
EXPOSURES = {"common", "plausible", "exceptional", "unreachable", "unknown"}
FILTERED = {
    "FILTER_DUPLICATE",
    "FILTER_RESOLVED",
    "FILTER_UNREACHABLE",
    "FILTER_UNSUBSTANTIATED",
}


def classify(issue):
    severity = issue.get("severity")
    confidence = issue.get("confidence")
    exposure = issue.get("exposure")
    current = issue.get("current")
    duplicate_of = issue.get("duplicate_of")
    hard_gate = issue.get("hard_gate", False)

    if severity not in SEVERITIES:
        raise ValueError(f"invalid severity: {severity!r}")
    if confidence not in CONFIDENCES:
        raise ValueError(f"invalid confidence: {confidence!r}")
    if exposure not in EXPOSURES:
        raise ValueError(f"invalid exposure: {exposure!r}")
    if not isinstance(current, bool):
        raise ValueError(f"invalid current: {current!r}")
    if duplicate_of is not None and (
        not isinstance(duplicate_of, str) or not duplicate_of.strip()
    ):
        raise ValueError(f"invalid duplicate_of: {duplicate_of!r}")
    if not isinstance(hard_gate, bool):
        raise ValueError(f"invalid hard_gate: {hard_gate!r}")

    if duplicate_of is not None:
        return "FILTER_DUPLICATE"
    if not current:
        return "FILTER_RESOLVED"
    if exposure == "unreachable":
        return "FILTER_UNREACHABLE"
    if confidence == "speculative" or severity == "cosmetic":
        return "FILTER_UNSUBSTANTIATED"
    if hard_gate or severity == "blocker":
        return "KEEP_ACTIONABLE"
    if exposure in {"common", "plausible"}:
        return "KEEP_ACTIONABLE"
    if exposure == "unknown":
        return "VERIFY"
    return "KEEP_TRACKED"


def summarize(dispositions):
    counts = Counter(dispositions)
    return {
        "keep": counts["KEEP_ACTIONABLE"] + counts["KEEP_TRACKED"],
        "verify": counts["VERIFY"],
        "filter": sum(counts[name] for name in FILTERED),
        "by_disposition": dict(sorted(counts.items())),
    }


def load_input(path):
    with path.open(encoding="utf-8") if path else sys.stdin as stream:
        payload = json.load(stream)
    issues = payload.get("issues") if isinstance(payload, dict) else payload
    if not isinstance(issues, list):
        raise ValueError("input must be a list or an object with an issues list")
    return issues


def self_test():
    base = {
        "severity": "material",
        "confidence": "supported",
        "exposure": "plausible",
        "current": True,
        "duplicate_of": None,
    }
    cases = [
        ({**base, "duplicate_of": "#12"}, "FILTER_DUPLICATE"),
        ({**base, "current": False}, "FILTER_RESOLVED"),
        ({**base, "exposure": "unreachable"}, "FILTER_UNREACHABLE"),
        ({**base, "confidence": "speculative"}, "FILTER_UNSUBSTANTIATED"),
        ({**base, "severity": "cosmetic"}, "FILTER_UNSUBSTANTIATED"),
        ({**base, "severity": "blocker", "exposure": "exceptional"}, "KEEP_ACTIONABLE"),
        ({**base, "exposure": "common"}, "KEEP_ACTIONABLE"),
        ({**base, "exposure": "unknown"}, "VERIFY"),
        ({**base, "exposure": "exceptional"}, "KEEP_TRACKED"),
        ({**base, "exposure": "exceptional", "hard_gate": True}, "KEEP_ACTIONABLE"),
    ]
    dispositions = []
    for issue, expected in cases:
        actual = classify(issue)
        assert actual == expected, (issue, actual, expected)
        dispositions.append(actual)
    assert summarize(dispositions) == {
        "keep": 4,
        "verify": 1,
        "filter": 5,
        "by_disposition": {
            "FILTER_DUPLICATE": 1,
            "FILTER_RESOLVED": 1,
            "FILTER_UNREACHABLE": 1,
            "FILTER_UNSUBSTANTIATED": 2,
            "KEEP_ACTIONABLE": 3,
            "KEEP_TRACKED": 1,
            "VERIFY": 1,
        },
    }


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("input", nargs="?", type=Path, help="JSON file; defaults to stdin")
    parser.add_argument("--self-test", action="store_true")
    args = parser.parse_args()

    if args.self_test:
        self_test()
        print("ok")
        return 0

    issues = load_input(args.input)
    result = []
    for index, issue in enumerate(issues, 1):
        if not isinstance(issue, dict):
            raise ValueError(f"issue {index} must be an object")
        result.append({**issue, "disposition": classify(issue)})
    summary = summarize(issue["disposition"] for issue in result)
    json.dump({"summary": summary, "issues": result}, sys.stdout, indent=2)
    print()
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except (OSError, ValueError, json.JSONDecodeError) as error:
        print(f"error: {error}", file=sys.stderr)
        raise SystemExit(2)
