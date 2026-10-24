#!/usr/bin/env python3
"""Derive review dispositions and the final decision from finding classifications."""

import argparse
import json
import sys
from pathlib import Path

SEVERITIES = {"blocker", "material", "cosmetic"}
CONFIDENCES = {"confirmed", "supported", "speculative"}
EXPOSURES = {"common", "plausible", "exceptional", "unreachable", "unknown"}


def classify(finding):
    severity = finding.get("severity")
    confidence = finding.get("confidence")
    exposure = finding.get("exposure")
    hard_gate = finding.get("hard_gate", False)

    if severity not in SEVERITIES:
        raise ValueError(f"invalid severity: {severity!r}")
    if confidence not in CONFIDENCES:
        raise ValueError(f"invalid confidence: {confidence!r}")
    if exposure not in EXPOSURES:
        raise ValueError(f"invalid exposure: {exposure!r}")
    if not isinstance(hard_gate, bool):
        raise ValueError(f"invalid hard_gate: {hard_gate!r}")

    if exposure == "unreachable":
        return "REJECT"
    if confidence == "speculative" or severity == "cosmetic":
        return "OMIT"
    if hard_gate or severity == "blocker":
        return "ACT_NOW"
    if exposure in {"common", "plausible"}:
        return "ACT_NOW"
    if exposure == "unknown":
        return "VERIFY_NOW"
    return "TRACK"


def decide(dispositions):
    if "ACT_NOW" in dispositions:
        return "REWORK"
    if "VERIFY_NOW" in dispositions:
        return "NEEDS_EVIDENCE"
    return "APPROVED"


def load_input(path):
    with path.open(encoding="utf-8") if path else sys.stdin as stream:
        payload = json.load(stream)
    findings = payload.get("findings") if isinstance(payload, dict) else payload
    if not isinstance(findings, list):
        raise ValueError("input must be a list or an object with a findings list")
    return findings


def self_test():
    cases = [
        ({"severity": "blocker", "confidence": "supported", "exposure": "exceptional"}, "ACT_NOW"),
        ({"severity": "material", "confidence": "confirmed", "exposure": "common"}, "ACT_NOW"),
        ({"severity": "material", "confidence": "supported", "exposure": "unknown"}, "VERIFY_NOW"),
        ({"severity": "material", "confidence": "confirmed", "exposure": "exceptional"}, "TRACK"),
        ({"severity": "material", "confidence": "speculative", "exposure": "common"}, "OMIT"),
        ({"severity": "cosmetic", "confidence": "confirmed", "exposure": "common"}, "OMIT"),
        ({"severity": "blocker", "confidence": "confirmed", "exposure": "unreachable"}, "REJECT"),
        ({"severity": "material", "confidence": "supported", "exposure": "exceptional", "hard_gate": True}, "ACT_NOW"),
    ]
    for finding, expected in cases:
        actual = classify(finding)
        assert actual == expected, (finding, actual, expected)
    assert decide(["TRACK"]) == "APPROVED"
    assert decide(["VERIFY_NOW", "TRACK"]) == "NEEDS_EVIDENCE"
    assert decide(["VERIFY_NOW", "ACT_NOW"]) == "REWORK"


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("input", nargs="?", type=Path, help="JSON file; defaults to stdin")
    parser.add_argument("--self-test", action="store_true")
    args = parser.parse_args()

    if args.self_test:
        self_test()
        print("ok")
        return 0

    findings = load_input(args.input)
    result = []
    for index, finding in enumerate(findings, 1):
        if not isinstance(finding, dict):
            raise ValueError(f"finding {index} must be an object")
        result.append({**finding, "disposition": classify(finding)})
    decision = decide([finding["disposition"] for finding in result])
    json.dump({"decision": decision, "findings": result}, sys.stdout, indent=2)
    print()
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except (OSError, ValueError, json.JSONDecodeError) as error:
        print(f"error: {error}", file=sys.stderr)
        raise SystemExit(2)
