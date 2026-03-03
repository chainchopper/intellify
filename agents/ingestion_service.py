"""
Intellify Ingestion Service
===========================
Parses enterprise file assets (PDF, DOCX, images, audio) and submits
validated metadata records to the Intellify MCP Hub.

Covers Phase 1 backlog item:
  "Scaffold intellify-ingestion-service logic (Docling/LiteRAG inspired parsing)"

Run:
    python ingestion_service.py <path_to_directory>
    python ingestion_service.py ./test_data
"""

import os
import sys
import json
import uuid
import hashlib
import logging
import argparse
from typing import Optional
from pathlib import Path

# ---------------------------------------------------------------------------
# Optional parser imports — degrade gracefully when not installed
# ---------------------------------------------------------------------------
try:
    from pdfminer.high_level import extract_text as pdf_extract_text
    HAS_PDF = True
except ImportError:
    HAS_PDF = False

try:
    from docx import Document as DocxDocument
    HAS_DOCX = True
except ImportError:
    HAS_DOCX = False

try:
    from PIL import Image
    HAS_PIL = True
except ImportError:
    HAS_PIL = False

import requests
from dotenv import load_dotenv

# ---------------------------------------------------------------------------
# Config
# ---------------------------------------------------------------------------

# Walk up to project root to find .env
_ROOT = Path(__file__).resolve().parent.parent
load_dotenv(dotenv_path=_ROOT / ".env")

MCP_HUB_URL    = os.getenv("NPU_STACK_API_URL", "http://127.0.0.1:8000")
# The MCP hub runs on its own port separate from NPU-STACK
MCP_HUB_URL    = f"http://127.0.0.1:{os.getenv('MCP_HUB_PORT', '8080')}"
MIN_CONFIDENCE = float(os.getenv("INGESTION_MIN_CONFIDENCE", "0.80"))
OUTPUT_DIR     = Path(os.getenv("INGESTION_OUTPUT_DIR", str(_ROOT / "data" / "ingested")))
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    datefmt="%H:%M:%S",
)
log = logging.getLogger("ingestion")

# ---------------------------------------------------------------------------
# File type registry
# ---------------------------------------------------------------------------

SUPPORTED_EXTENSIONS = {
    # Documents
    ".pdf":  "document",
    ".doc":  "document",
    ".docx": "document",
    ".txt":  "document",
    ".md":   "document",
    ".rtf":  "document",
    ".csv":  "document",
    ".xlsx": "document",
    ".xls":  "document",
    # Images
    ".jpg":  "image",
    ".jpeg": "image",
    ".png":  "image",
    ".gif":  "image",
    ".webp": "image",
    ".bmp":  "image",
    ".tiff": "image",
    # Audio
    ".mp3":  "audio",
    ".wav":  "audio",
    ".flac": "audio",
    ".ogg":  "audio",
    ".aac":  "audio",
    # Video
    ".mp4":  "video",
    ".mov":  "video",
    ".avi":  "video",
    ".mkv":  "video",
    ".webm": "video",
}

# ---------------------------------------------------------------------------
# Category inference (keyword + path heuristics — no ML required locally)
# ---------------------------------------------------------------------------

_CATEGORY_RULES = [
    # (keywords_in_path_or_name,          category)
    ({"finance", "financial", "report", "budget", "invoice", "revenue", "profit"}, "financial_reports"),
    ({"hr", "human_resource", "employee", "memo", "onboard", "policy"},            "internal_memo"),
    ({"market", "campaign", "brand", "promo", "ad", "advertisement"},              "marketing_assets"),
    ({"audio", "podcast", "voice", "speech", "music"},                             "audio_samples"),
    ({"video", "recording", "footage", "clip"},                                    "video_media"),
    ({"data", "dataset", "train", "validation", "label"},                          "training_data"),
    ({"image", "photo", "picture", "scan", "diagram"},                             "images"),
]

def infer_category(file_path: str, asset_type: str) -> tuple[str, float]:
    """Return (category, confidence_score) based on path heuristics."""
    tokens = set(file_path.lower().replace("\\", "/").replace("-", "_").replace(".", "_").split("/"))
    tokens |= set(Path(file_path).stem.lower().replace("-", "_").split("_"))

    best_cat   = None
    best_score = 0.0

    for keywords, category in _CATEGORY_RULES:
        overlap = len(keywords & tokens)
        if overlap > 0:
            score = min(0.95, 0.75 + 0.05 * overlap)
            if score > best_score:
                best_score = score
                best_cat   = category

    if best_cat is None:
        # Fallback by asset type
        defaults = {
            "document": ("internal_memo",    0.80),
            "image":    ("images",           0.80),
            "audio":    ("audio_samples",    0.80),
            "video":    ("video_media",      0.80),
        }
        best_cat, best_score = defaults.get(asset_type, ("general", 0.80))

    return best_cat, round(best_score, 4)

# ---------------------------------------------------------------------------
# Content extraction (lightweight, no LLM)
# ---------------------------------------------------------------------------

def _sha256(path: str) -> str:
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(65536), b""):
            h.update(chunk)
    return h.hexdigest()


def extract_content_snippet(file_path: str, ext: str, max_chars: int = 500) -> Optional[str]:
    """Extract a short text snippet from the file for metadata enrichment."""
    try:
        if ext == ".pdf" and HAS_PDF:
            text = pdf_extract_text(file_path) or ""
            return text[:max_chars].strip() or None

        if ext in (".doc", ".docx") and HAS_DOCX:
            doc  = DocxDocument(file_path)
            text = " ".join(p.text for p in doc.paragraphs if p.text.strip())
            return text[:max_chars].strip() or None

        if ext == ".txt" or ext == ".md":
            with open(file_path, "r", errors="ignore") as f:
                return f.read(max_chars).strip() or None

        if ext in (".jpg", ".jpeg", ".png", ".bmp", ".tiff", ".webp") and HAS_PIL:
            img  = Image.open(file_path)
            info = f"{img.format} {img.size[0]}x{img.size[1]} {img.mode}"
            return info

    except Exception as exc:
        log.debug(f"  Could not extract snippet from {file_path}: {exc}")

    return None


# ---------------------------------------------------------------------------
# Core scanner
# ---------------------------------------------------------------------------

def scan_directory(directory_path: str) -> dict:
    directory_path = os.path.abspath(directory_path)
    if not os.path.exists(directory_path):
        log.error(f"Directory does not exist: {directory_path}")
        sys.exit(1)

    log.info(f"Starting ingestion scan: {directory_path}")

    valid_assets: list[dict] = []
    skipped    = 0
    errors     = 0

    for root, _, files in os.walk(directory_path):
        for filename in files:
            ext = Path(filename).suffix.lower()

            if ext not in SUPPORTED_EXTENSIONS:
                skipped += 1
                continue

            full_path  = os.path.join(root, filename)
            asset_type = SUPPORTED_EXTENSIONS[ext]
            category, confidence = infer_category(full_path, asset_type)

            if confidence < MIN_CONFIDENCE:
                log.debug(f"  Skipping {filename} (confidence {confidence} < {MIN_CONFIDENCE})")
                skipped += 1
                continue

            try:
                size_bytes = os.path.getsize(full_path)
                sha256     = _sha256(full_path)
                snippet    = extract_content_snippet(full_path, ext)

                asset = {
                    "asset_id":         f"asset_{uuid.uuid4().hex[:12]}",
                    "asset_type":       asset_type,
                    "file_format":      ext,
                    "category":         category,
                    "confidence_score": confidence,
                    "file_path":        full_path.replace("\\", "/"),
                    "filename":         filename,
                    "size_bytes":       size_bytes,
                    "sha256":           sha256,
                    "content_snippet":  snippet,
                }
                valid_assets.append(asset)
                log.info(f"  ✓ {filename} [{category}] conf={confidence}")

            except Exception as exc:
                log.warning(f"  ✗ Failed to process {filename}: {exc}")
                errors += 1

    # Build folder summary
    cat_counts: dict[str, int] = {}
    for asset in valid_assets:
        cat_counts[asset["category"]] = cat_counts.get(asset["category"], 0) + 1

    primary_category = max(cat_counts, key=cat_counts.get) if cat_counts else "general"

    output = {
        "scan_root":        directory_path.replace("\\", "/"),
        "primary_category": primary_category,
        "category_counts":  cat_counts,
        "assets":           valid_assets,
        "summary": {
            "total_valid":   len(valid_assets),
            "total_skipped": skipped,
            "total_errors":  errors,
        },
    }

    # Write to output dir
    out_file = OUTPUT_DIR / f"scan_{uuid.uuid4().hex[:8]}.json"
    with open(out_file, "w") as f:
        json.dump(output, f, indent=2)
    log.info(f"Ingestion report written to: {out_file}")

    return output


# ---------------------------------------------------------------------------
# MCP Hub relay — submit scan results as a recommendation request
# ---------------------------------------------------------------------------

def relay_to_mcp_hub(scan_result: dict) -> dict:
    """
    Post the scan summary to the MCP Hub /api/recommendations endpoint
    so the recommendation engine can suggest Docker pipelines.
    """
    if not scan_result["assets"]:
        log.warning("No valid assets found; skipping MCP Hub relay.")
        return {"status": "skipped", "reason": "no_assets"}

    largest_category = scan_result["primary_category"]
    file_format_counts: dict[str, int] = {}
    for asset in scan_result["assets"]:
        fmt = asset["file_format"]
        file_format_counts[fmt] = file_format_counts.get(fmt, 0) + 1
    dominant_format = max(file_format_counts, key=file_format_counts.get) if file_format_counts else ".pdf"

    payload = {
        "category":    largest_category,
        "file_format": dominant_format,
        "asset_count": scan_result["summary"]["total_valid"],
    }

    log.info(f"Relaying to MCP Hub ({MCP_HUB_URL}/api/recommendations): {payload}")
    try:
        resp = requests.post(f"{MCP_HUB_URL}/api/recommendations", json=payload, timeout=10)
        resp.raise_for_status()
        result = resp.json()
        log.info(f"MCP Hub response: {result}")
        return result
    except Exception as exc:
        log.warning(f"MCP Hub unreachable (will retry when hub is running): {exc}")
        return {"status": "hub_offline", "payload": payload}


# ---------------------------------------------------------------------------
# Entry point
# ---------------------------------------------------------------------------

if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Intellify Ingestion Service — Scan a directory and send metadata to MCP Hub."
    )
    parser.add_argument("path", nargs="?", default=os.getenv("INGESTION_SCAN_ROOT", "./test_data"),
                        help="Directory to scan (default: $INGESTION_SCAN_ROOT or ./test_data)")
    parser.add_argument("--no-relay", action="store_true",
                        help="Skip posting results to the MCP Hub")
    args = parser.parse_args()

    result = scan_directory(args.path)

    log.info(f"\n{'='*50}")
    log.info(f"  Valid assets : {result['summary']['total_valid']}")
    log.info(f"  Skipped      : {result['summary']['total_skipped']}")
    log.info(f"  Errors       : {result['summary']['total_errors']}")
    log.info(f"  Primary cat  : {result['primary_category']}")
    log.info(f"{'='*50}")

    if not args.no_relay:
        hub_response = relay_to_mcp_hub(result)
        log.info(f"Hub relay status: {hub_response.get('status', hub_response)}")
