#!/usr/bin/env python3
"""Structure-only license detection for two projects (mode D borrowing plan).

Reads both project directories and reports, per project, where a license
declaration exists and whether declarations contradict each other. It never
runs target code, never accesses the network, and never issues a legal verdict
-- compatibility judgment belongs to the model + user (see references/
borrow-plan.md D7). The script only answers: "is there a declaration, what
SPDX-like ids can be extracted, do the sources disagree, is anything missing".

Exit code is structural: 0 = both projects have consistent declarations;
2 = missing declaration or contradiction on either side (stop and ask the user).
Standard library only.
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path

LICENSE_FILENAMES = (
    "LICENSE", "LICENSE.md", "LICENSE.txt", "LICENCE", "LICENCE.md", "LICENCE.txt",
    "COPYING", "COPYING.md", "COPYING.txt", "NOTICE", "NOTICE.md", "NOTICE.txt",
)
SPDX_PATTERNS = [
    (r"\bMIT\s+License\b|\(MIT\)|\bMIT\b", "MIT"),
    (r"Apache\s+License[,\s]+Version\s+2\.0|Apache-2\.0|APACHE2", "Apache-2.0"),
    (r"BSD\s+3[-\s]Clause|BSD-3-Clause|Redistribution and use in source and binary forms", "BSD-3-Clause"),
    (r"BSD\s+2[-\s]Clause|Simplified BSD|FreeBSD", "BSD-2-Clause"),
    (r"GNU\s+AFFERO\s+GENERAL PUBLIC LICENSE|AGPL", "AGPL-3.0"),
    (r"GNU\s+LESSER\s+GENERAL PUBLIC LICENSE|LGPL", "LGPL"),
    (r"GNU\s+GENERAL PUBLIC LICENSE", "GPL"),
    (r"GPL[-\s]?v?3(?:\.0)?|GPL-3\.0|GPLv3", "GPL-3.0"),
    (r"GPL[-\s]?v?2(?:\.0)?|GPL-2\.0|GPLv2", "GPL-2.0"),
    (r"Mozilla\s+Public\s+License|MPL-?2\.0", "MPL-2.0"),
    (r"ISC\s+License|Permission to use, copy, modify", "ISC"),
    (r"Unlicense|This is free and unencumbered software", "Unlicense"),
    (r"CC0[- ]?1\.0|Creative Commons CC0", "CC0-1.0"),
    (r"CC BY|Creative Commons Attribution", "CC-BY"),
    (r"proprietary|All rights reserved", "proprietary"),
]
METADATA_FILES = {
    "package.json": r'"license"\s*:\s*"([^"]+)"',
    "pyproject.toml": r'license\s*=\s*(?:"([^"]+)"|\{?\s*text\s*=\s*"([^"]+)"\s*\}?)',
    "setup.py": r"license\s*=\s*['\"]([^'\"]+)['\"]",
    "Cargo.toml": r'license\s*=\s*"([^"]+)"',
    "composer.json": r'"license"\s*:\s*"([^"]+)"',
}
README_FILENAMES = ("README.md", "README.rst", "README", "readme.md")


def extract_spdx(text: str) -> list[str]:
    hits: list[str] = []
    for pattern, name in SPDX_PATTERNS:
        if re.search(pattern, text, re.IGNORECASE):
            if name not in hits:
                hits.append(name)
    return hits


def read_small(path: Path) -> str:
    try:
        return path.read_text(encoding="utf-8", errors="replace")
    except OSError:
        return ""


def scan_project(root: Path) -> dict:
    root = Path(root)
    license_files: list[str] = []
    spdx_from_files: list[str] = []
    for name in LICENSE_FILENAMES:
        path = root / name
        if path.is_file():
            license_files.append(str(path.relative_to(root)))
            spdx_from_files.extend(extract_spdx(read_small(path)))

    manifest_license: list[str] = []
    for filename, pattern in METADATA_FILES.items():
        path = root / filename
        if path.is_file():
            for match in re.finditer(pattern, read_small(path), re.IGNORECASE):
                value = next((g for g in match.groups() if g), "")
                if value.strip():
                    manifest_license.append(f"{filename}: {value.strip()}")

    readme_mention: str | None = None
    for name in README_FILENAMES:
        path = root / name
        if path.is_file():
            for hit in extract_spdx(read_small(path)[:8000]):
                readme_mention = f"{name} mentions {hit}"
                break
            if readme_mention:
                break

    declared = bool(license_files or manifest_license)
    unique_spdx = sorted(dict.fromkeys(spdx_from_files))
    contradictory = None
    if license_files and manifest_license and unique_spdx:
        metadata_flat = " ".join(manifest_license)
        metadata_spdx = extract_spdx(metadata_flat)
        overlap = set(unique_spdx) & set(metadata_spdx)
        if unique_spdx and metadata_spdx and not overlap:
            contradictory = f"LICENSE file ids {unique_spdx} vs metadata {sorted(set(metadata_spdx))}"
        if contradictory is None and "proprietary" in unique_spdx and metadata_spdx and set(metadata_spdx) != {"proprietary"}:
            contradictory = "LICENSE says proprietary but metadata declares FOSS id"

    return {
        "path": str(root),
        "license_files": license_files,
        "spdx_from_license_files": unique_spdx,
        "manifest_license_declarations": manifest_license,
        "readme_declaration_mention": readme_mention,
        "has_declaration": declared,
        "contradiction": contradictory,
    }


def main() -> int:
    parser = argparse.ArgumentParser(description="Structure-only license detection for two projects (mode D).")
    parser.add_argument("user_project", help="User's own project directory (license declarations checked read-only).")
    parser.add_argument("reference_project", help="Reference/borrowed project directory (license declarations checked read-only).")
    args = parser.parse_args()

    user = scan_project(Path(args.user_project))
    ref = scan_project(Path(args.reference_project))

    issues: list[str] = []
    for label, result in (("user_project", user), ("reference_project", ref)):
        if not result["has_declaration"]:
            issues.append(f"{label}: no license declaration found (missing evidence)")
        if result["contradiction"]:
            issues.append(f"{label}: {result['contradiction']}")

    output = {
        "ok": not issues,
        "scope": "structure-only; declare/missing/contradiction detection, NOT a legal verdict. Model+user decide compatibility (see references/borrow-plan.md D7).",
        "user_project": user,
        "reference_project": ref,
        "issues": issues,
    }
    print(json.dumps(output, ensure_ascii=False, indent=2))
    return 0 if not issues else 2


if __name__ == "__main__":
    sys.exit(main())