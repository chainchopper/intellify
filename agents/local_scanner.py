import os
import sys
import json
import uuid
from typing import List

# Add schemas to path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'schemas')))
from metadata_schemas import FileAsset, FolderAsset
from pydantic import ValidationError

def scan_directory(directory_path: str) -> dict:
    if not os.path.exists(directory_path):
        print(f"Error: Directory {directory_path} does not exist.")
        sys.exit(1)

    print(f"Scanning directory: {directory_path}")
    
    valid_assets = []
    invalid_count = 0

    allowed_exts = {".pdf", ".doc", ".docx", ".txt", ".jpg", ".png", ".mp4", ".mp3", ".wav"}
    
    file_count = 0
    primary_cats = {"financial_reports": 0, "internal_memo": 0, "marketing_assets": 0, "audio_samples": 0}

    for root, _, files in os.walk(directory_path):
        for file in files:
            ext = os.path.splitext(file)[1].lower()
            if ext not in allowed_exts:
                invalid_count += 1
                continue

            # extremely basic mock categorization based on extension/filename
            category = "marketing_assets"
            if ext in {".pdf", ".doc", ".docx"}:
                category = "financial_reports" if "finance" in root.lower() or "report" in file.lower() else "internal_memo"
            elif ext in {".mp3", ".wav"}:
                category = "audio_samples"
            
            primary_cats[category] += 1
            file_count += 1

            # Mock confidence score (usually would come from a local ML classifier)
            confidence = 0.95

            try:
                asset = FileAsset(
                    asset_id=f"file_{uuid.uuid4().hex[:8]}",
                    asset_type="document" if ext in {".pdf", ".doc", ".docx", ".txt"} else "media" if ext in {".jpg", ".png", ".mp4"} else "audio",
                    file_format=ext,
                    category=category,
                    confidence_score=confidence,
                    file_path=os.path.join(root, file).replace("\\", "/")
                )
                valid_assets.append(asset.dict())
            except ValidationError as e:
                print(f"Validation failed for {file}: {e}")
                invalid_count += 1

    # Determine primary category for folder
    primary_category = max(primary_cats, key=primary_cats.get) if file_count > 0 else "internal_memo"

    folder_metadata = None
    if file_count >= 5:
        try:
            folder_asset = FolderAsset(
                folder_id=f"folder_{uuid.uuid4().hex[:8]}",
                asset_type="folder",
                asset_count=file_count,
                primary_category=primary_category,
                folder_path=directory_path.replace("\\", "/")
            )
            folder_metadata = folder_asset.dict()
        except ValidationError as e:
            print(f"Folder validation failed: {e}")

    output_payload = {
        "folder": folder_metadata,
        "files": valid_assets,
        "summary": {
            "total_files": file_count + invalid_count,
            "valid_assets_count": len(valid_assets),
            "invalid_assets_count": invalid_count
        }
    }

    out_file = os.path.join(directory_path, "asset_metadata.json")
    with open(out_file, "w") as f:
        json.dump(output_payload, f, indent=4)
        
    print(f"Scan complete. Found {len(valid_assets)} valid files.")
    print(f"Metadata exported to {out_file}")
    
    return output_payload

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python local_scanner.py <path_to_scan>")
        sys.exit(1)
    
    target_dir = sys.argv[1]
    scan_directory(target_dir)
