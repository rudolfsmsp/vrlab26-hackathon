"""Resolve requested BlenderKit asset IDs into a repo manifest.

Run with Blender's Python:
  blender --background --python Tools/resolve_blenderkit_assets.py

The manifest intentionally stores metadata, not downloaded third-party model
files. BlenderKit royalty-free models may be used in the project, but raw
redistribution from a public GitHub repo is not allowed unless an asset is CC0.
"""

from __future__ import annotations

import json
import re
from datetime import datetime, timezone
from pathlib import Path

import bpy

from bl_ext.user_default.blenderkit import paths, search


ROOT = Path(__file__).resolve().parents[1]
OUT_DIR = ROOT / "Art" / "Blender" / "BlenderKitAssets"
MANIFEST_PATH = OUT_DIR / "blenderkit_assets_manifest.json"
README_PATH = OUT_DIR / "README.md"

ASSETS = [
    {"asset_base_id": "6302a2be-e623-48b8-a8d1-8dd2cb22fb40", "asset_type": "model"},
    {"asset_base_id": "e72444d5-b869-44b7-87ec-81d5dd4f7f08", "asset_type": "model"},
    {"asset_base_id": "6aae5842-dfe7-4e97-a421-4ce2db5c06dd", "asset_type": "model"},
    {"asset_base_id": "ea5c40f5-fc3b-4595-b476-630cfc8b0262", "asset_type": "model"},
    {"asset_base_id": "caebdd9c-6420-4768-a0af-da0393605fa1", "asset_type": "model"},
    {"asset_base_id": "a713a9d1-7ce5-4e8a-8a66-0cc34798f8a7", "asset_type": "model"},
    {"asset_base_id": "3285f787-bbef-404b-bdca-845c47192dea", "asset_type": "model"},
    {"asset_base_id": "32206625-26eb-49b0-8a0b-99ed1f9e1ae5", "asset_type": "model"},
    {"asset_base_id": "596d0928-4938-4a98-adcd-7605a586ba7a", "asset_type": "model"},
    {"asset_base_id": "b5a6b421-f809-4ac6-ae5f-da4a75c33ecc", "asset_type": "model"},
    {"asset_base_id": "0223c105-5312-4f73-aa16-361453eab6e6", "asset_type": "model"},
    {"asset_base_id": "afe8ec3b-ae8b-4a6c-8fe2-aaae94104a9a", "asset_type": "model"},
    {"asset_base_id": "accb3f43-21d9-4d3a-9805-8c0aae5f0827", "asset_type": "model"},
    {"asset_base_id": "d782d507-4a8d-4117-9d43-c6d2981284f3", "asset_type": "model"},
    {"asset_base_id": "830a85cd-f884-4282-aa97-8de873973600", "asset_type": "model"},
    {"asset_base_id": "4828e374-81ec-48f7-bc14-45b26c8ca14a", "asset_type": "model"},
    {"asset_base_id": "8c588279-c54c-467b-85ea-b79d3af88890", "asset_type": "model"},
    {"asset_base_id": "120f2f90-9104-48b3-b2ea-fece4d09e666", "asset_type": "model"},
    {"asset_base_id": "28c2f25a-c948-47a1-a72e-807a73bfa819", "asset_type": "model"},
    {"asset_base_id": "fdd9ddb8-9231-4cb8-9ebb-869b4053059b", "asset_type": "model"},
    {"asset_base_id": "2b90b3cb-e9bc-451b-a153-45567192fb45", "asset_type": "model"},
    {"asset_base_id": "44892441-ec35-484a-9951-06e97e99704e", "asset_type": "model"},
    {"asset_base_id": "3d560729-9179-49fa-b310-9ad2a9dbb7a5", "asset_type": "model"},
    {"asset_base_id": "98f8cae5-87d5-48c2-b458-7e82f3205512", "asset_type": "model"},
]


def slugify(value: str, fallback: str) -> str:
    value = re.sub(r"[^a-zA-Z0-9]+", "-", value).strip("-").lower()
    return value[:72] or fallback


def clean_author(author: dict) -> dict:
    return {
        "id": str(author.get("id", "")),
        "name": author.get("fullName")
        or " ".join(
            part
            for part in (author.get("firstName", ""), author.get("lastName", ""))
            if part
        ).strip(),
    }


def resolve_asset(asset_base_id: str, expected_type: str, api_key: str) -> dict:
    results = search.get_search_simple(
        {"asset_base_id": asset_base_id},
        page_size=1,
        max_results=1,
        api_key=api_key,
    )
    if not results:
        return {
            "asset_base_id": asset_base_id,
            "expected_asset_type": expected_type,
            "status": "missing",
            "error": "No BlenderKit search result returned for this asset_base_id.",
        }

    result = results[0]
    asset_id = result.get("id", "")
    display_name = result.get("displayName") or result.get("name") or asset_base_id
    license_name = result.get("license", "")
    return {
        "asset_base_id": result.get("assetBaseId", asset_base_id),
        "asset_id": asset_id,
        "expected_asset_type": expected_type,
        "asset_type": result.get("assetType", ""),
        "name": result.get("name", ""),
        "display_name": display_name,
        "slug": slugify(display_name, asset_base_id[:8]),
        "license": license_name,
        "can_download": bool(result.get("canDownload", False)),
        "is_free": bool(result.get("isFree", False)),
        "verification_status": result.get("verificationStatus", ""),
        "category": result.get("category", ""),
        "files_size_bytes": result.get("filesSize", 0),
        "author": clean_author(result.get("author", {})),
        "gallery_url": paths.get_asset_gallery_url(asset_id) if asset_id else "",
        "public_repo_raw_file_policy": (
            "raw_commit_allowed"
            if str(license_name).lower() == "cc_zero"
            else "metadata_only_for_public_repo"
        ),
        "status": "resolved",
    }


def write_readme(manifest: dict) -> None:
    assets = manifest["assets"]
    lines = [
        "# BlenderKit Assets",
        "",
        "This folder tracks the BlenderKit assets requested for the project by asset ID and license metadata.",
        "",
        "The GitHub repository is public, so raw BlenderKit model files are not committed here unless an individual asset is CC0. BlenderKit royalty-free assets may be used in a higher-level project build, but the raw asset files should not be redistributed from this public repo.",
        "",
        f"Resolved assets: {sum(1 for asset in assets if asset['status'] == 'resolved')} / {len(assets)}",
        "",
        "| Asset | License | Policy | Author | BlenderKit ID |",
        "| --- | --- | --- | --- | --- |",
    ]
    for asset in assets:
        name = asset.get("display_name") or asset["asset_base_id"]
        url = asset.get("gallery_url", "")
        linked_name = f"[{name}]({url})" if url else name
        author = asset.get("author", {}).get("name", "")
        lines.append(
            "| {name} | {license} | {policy} | {author} | `{asset_base_id}` |".format(
                name=linked_name,
                license=asset.get("license", ""),
                policy=asset.get("public_repo_raw_file_policy", ""),
                author=author,
                asset_base_id=asset["asset_base_id"],
            )
        )
    lines.append("")
    README_PATH.write_text("\n".join(lines), encoding="utf-8")


def main() -> None:
    prefs = bpy.context.preferences.addons["bl_ext.user_default.blenderkit"].preferences
    if not prefs.api_key:
        raise RuntimeError("BlenderKit API key is not configured in Blender preferences.")

    OUT_DIR.mkdir(parents=True, exist_ok=True)
    assets = [
        resolve_asset(asset["asset_base_id"], asset["asset_type"], prefs.api_key)
        for asset in ASSETS
    ]
    manifest = {
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "source": "BlenderKit",
        "repository_policy": "Public GitHub repo stores metadata for royalty-free BlenderKit assets; raw third-party asset files require CC0 or a private distribution channel.",
        "assets": assets,
    }
    MANIFEST_PATH.write_text(json.dumps(manifest, indent=2), encoding="utf-8")
    write_readme(manifest)
    print(f"Wrote {MANIFEST_PATH}")
    print(f"Wrote {README_PATH}")
    print(
        "Resolved {resolved}/{total}".format(
            resolved=sum(1 for asset in assets if asset["status"] == "resolved"),
            total=len(assets),
        )
    )


if __name__ == "__main__":
    main()
