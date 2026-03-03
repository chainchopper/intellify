import os
import sys
import json
import uuid
from typing import List
from pathlib import Path

# Add schemas to path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'schemas')))
from metadata_schemas import FileAsset, FolderAsset
from pydantic import ValidationError

# ---------------------------------------------------------------------------
# Category rules shared with ingestion_service.py
# ---------------------------------------------------------------------------

_CATEGORY_RULES = [
    ({"finance", "financial", "report", "budget", "invoice", "revenue", "profit"}, "financial_reports"),
    ({"hr", "human_resource", "employee", "memo", "onboard", "policy"},            "internal_memo"),
    ({"market", "campaign", "brand", "promo", "ad", "advertisement"},              "marketing_assets"),
    ({"audio", "podcast", "voice", "speech", "music"},                             "audio_samples"),
    ({"video", "recording", "footage", "clip"},                                    "video_media"),
    ({"data", "dataset", "train", "validation", "label"},                          "training_data"),
    ({"image", "photo", "picture", "scan", "diagram"},                             "images"),
]

_TYPE_DEFAULTS = {
    "document": "internal_memo",
    "media":    "images",
    "audio":    "audio_samples",
    "video":    "video_media",
}

ALLOWED_EXTS = {
    ".pdf": "document", ".doc": "document", ".docx": "document",
    ".txt": "document", ".md":  "document", ".csv":  "document",
    ".jpg": "media",    ".jpeg": "media",   ".png": "media",
    ".mp4": "video",    ".mov": "video",
    ".mp3": "audio",    ".wav": "audio",    ".flac": "audio",
}


def _infer_category(file_path: str, asset_type: str) -> tuple:
    """Return (category, confidence_score) using path + filename heuristics."""
    tokens = set(
        file_path.lower()
        .replace("\\", "/").replace("-", "_").replace(".", "_")
        .split("/")
    )
    tokens |= set(Path(file_path).stem.lower().replace("-", "_").split("_"))

    best_cat, best_score = None, 0.0
    for keywords, category in _CATEGORY_RULES:
        overlap = len(keywords & tokens)
        if overlap > 0:
            score = min(0.95, 0.75 + 0.05 * overlap)
            if score > best_score:
                best_score, best_cat = score, category

    if best_cat is None:
        best_cat   = _TYPE_DEFAULTS.get(asset_type, "internal_memo")
        best_score = 0.80

    return best_cat, round(best_score, 4)


def scan_directory(directory_path: str) -> dict:
    if not os.path.exists(directory_path):
        print(f"Error: Directory {directory_path} does not exist.")
        sys.exit(1)

    print(f"Scanning directory: {directory_path}")

    valid_assets: List[dict] = []
    invalid_count = 0
    category_counts: dict = {}

    for root, _, files in os.walk(directory_path):
        for file in files:
            ext = os.path.splitext(file)[1].lower()
            if ext not in ALLOWED_EXTS:
                invalid_count += 1
                continue

            full_path  = os.path.join(root, file)
            asset_type = ALLOWED_EXTS[ext]
            category, confidence = _infer_category(full_path, asset_type)

            category_counts[category] = category_counts.get(category, 0) + 1

            try:
                asset = FileAsset(
                    asset_id=f"file_{uuid.uuid4().hex[:8]}",
                    asset_type=asset_type,
                    file_format=ext,
                    category=category,
                    confidence_score=confidence,
                    file_path=full_path.replace("\\", "/"),
                )
                valid_assets.append(asset.model_dump())
            except ValidationError as e:
                print(f"Validation failed for {file}: {e}")
                invalid_count += 1

    primary_category = (
        max(category_counts, key=category_counts.get) if category_counts else "internal_memo"
    )

    folder_metadata = None
    if len(valid_assets) >= 5:
        try:
            folder_asset = FolderAsset(
                folder_id=f"folder_{uuid.uuid4().hex[:8]}",
                asset_type="folder",
                asset_count=len(valid_assets),
                primary_category=primary_category,
                folder_path=directory_path.replace("\\", "/"),
            )
            folder_metadata = folder_asset.model_dump()
        except ValidationError as e:
            print(f"Folder validation failed: {e}")

    output_payload = {
        "folder":          folder_metadata,
        "files":           valid_assets,
        "category_counts": category_counts,
        "summary": {
            "total_files":         len(valid_assets) + invalid_count,
            "valid_assets_count":  len(valid_assets),
            "invalid_assets_count": invalid_count,
        },
    }

    out_file = os.path.join(directory_path, "asset_metadata.json")
    with open(out_file, "w") as f:
        json.dump(output_payload, f, indent=4)

    print(f"Scan complete. {len(valid_assets)} valid assets. Metadata → {out_file}")
    return output_payload


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python local_scanner.py <path_to_scan>")
        sys.exit(1)
    scan_directory(sys.argv[1])
