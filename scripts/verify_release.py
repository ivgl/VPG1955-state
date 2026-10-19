#!/usr/bin/env python3
"""Read-only validation of the imported official VPI1955 1955 baseline."""
import hashlib
import json
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parent.parent

def sha256(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()

def main():
    errors = []
    try:
        head = json.loads((ROOT / "HEAD.json").read_text(encoding="utf-8"))
        manifest = json.loads((ROOT / "manifest_1955.json").read_text(encoding="utf-8"))
    except Exception as exc:
        print("Cannot read HEAD/manifest:", exc)
        return 1

    if head.get("manifest_sha256") != sha256(ROOT / "manifest_1955.json"):
        errors.append("HEAD manifest SHA-256 does not match")
    if head.get("campaign_id") != manifest.get("campaign_id"):
        errors.append("Campaign ID differs")
    if head.get("release_id") != manifest.get("release_id"):
        errors.append("Release ID differs")
    if head.get("year") != 1955 or manifest.get("year") != 1955:
        errors.append("Unexpected release year")

    files = manifest.get("files", [])
    paths = [item.get("path") for item in files]
    if len(files) != 30 or sum(str(p).startswith("countries/") for p in paths) != 12 or sum(str(p).startswith("modules/") for p in paths) != 12:
        errors.append("Expected 30 records (12 country states and 12 modules)")

    for item in files:
        rel = item["path"]
        path = ROOT / rel
        if not path.is_file():
            errors.append(f"Missing: {rel}")
            continue
        if sha256(path) != item["sha256"]:
            errors.append(f"SHA-256 mismatch: {rel}")
        if path.stat().st_size != item["bytes"]:
            errors.append(f"Size mismatch: {rel}")
        try:
            json.loads(path.read_text(encoding="utf-8"))
        except (UnicodeDecodeError, ValueError) as exc:
            errors.append(f"Invalid JSON: {rel}: {exc}")

    if errors:
        for error in errors:
            print("ERROR:", error)
        return 1
    print(f"PASS: {len(files)}/30 verified, 12 countries, 12 mechanics; manifest matches HEAD")
    return 0

if __name__ == "__main__":
    sys.exit(main())
