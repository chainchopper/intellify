from metadata_schemas import FileAsset, FolderAsset, HardwareAsset
from pydantic import ValidationError

def test_file_asset():
    print("Testing Valid FileAsset...")
    valid_file = FileAsset(
        asset_id="file_001",
        asset_type="document",
        file_format=".pdf",
        category="financial_report",
        confidence_score=0.92,
        file_path="/Finance/report_2023.pdf"
    )
    print("SUCCESS: Valid FileAsset created.")

    print("Testing Invalid FileAsset (low confidence)...")
    try:
        invalid_file = FileAsset(
            asset_id="file_002",
            asset_type="document",
            file_format=".pdf",
            category="financial_report",
            confidence_score=0.75, # low confidence
            file_path="/Finance/report_draft.pdf"
        )
        print("FAIL: Should have raised ValidationError")
    except ValidationError as e:
        print(f"SUCCESS: Caught validation error -> {e.errors()[0]['msg']}")

    print("Testing Invalid FileAsset (bad format)...")
    try:
        bad_format = FileAsset(
            asset_id="file_003",
            asset_type="document",
            file_format=".exe",
            category="financial_report",
            confidence_score=0.95,
            file_path="/Finance/malware.exe"
        )
        print("FAIL: Should have raised ValidationError")
    except ValidationError as e:
        print(f"SUCCESS: Caught validation error -> {e.errors()[0]['msg']}")

def test_folder_asset():
    print("\nTesting Valid FolderAsset...")
    valid_folder = FolderAsset(
        folder_id="folder_001",
        asset_type="folder",
        asset_count=15,
        primary_category="financial_reports",
        folder_path="/Finance/"
    )
    print("SUCCESS: Valid FolderAsset created.")

def test_hardware_asset():
    print("\nTesting Valid HardwareAsset...")
    valid_hw = HardwareAsset(
        hardware_id="hw_001",
        asset_type="network_device",
        status="active",
        lan_ip="192.168.1.10"
    )
    print("SUCCESS: Valid HardwareAsset created.")

if __name__ == "__main__":
    test_file_asset()
    test_folder_asset()
    test_hardware_asset()
