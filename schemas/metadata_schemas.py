from pydantic import BaseModel, Field, validator
from typing import Literal

class AssetMetadata(BaseModel):
    """Base model for all Intellify assets."""
    asset_type: str

class FileAsset(AssetMetadata):
    asset_id: str
    asset_type: Literal["document", "media", "code", "audio"] = "document"
    file_format: str
    category: str
    confidence_score: float = Field(ge=0.0, le=1.0)
    file_path: str

    @validator("confidence_score")
    def validate_confidence(cls, v):
        if v < 0.8:
            raise ValueError("confidence_score must be >= 0.8 for valid assets")
        return v

    @validator("file_format")
    def validate_format(cls, v):
        allowed_formats = {".pdf", ".doc", ".docx", ".txt", ".jpg", ".png", ".mp4", ".mp3", ".wav"}
        if v not in allowed_formats:
            raise ValueError(f"file_format must be one of {allowed_formats}")
        return v

class FolderAsset(AssetMetadata):
    folder_id: str
    asset_type: Literal["folder"] = "folder"
    asset_count: int
    primary_category: str
    folder_path: str

    @validator("asset_count")
    def validate_count(cls, v):
        if v < 5:
            raise ValueError("asset_count must be >= 5 for valid folders")
        return v
        
    @validator("primary_category")
    def validate_category(cls, v):
        allowed_cats = {"financial_reports", "internal_memo", "marketing_assets", "audio_samples"}
        if v not in allowed_cats:
            raise ValueError(f"primary_category must be one of {allowed_cats}")
        return v

class HardwareAsset(AssetMetadata):
    hardware_id: str
    asset_type: Literal["network_device", "compute_node", "audio_interface"] = "network_device"
    status: Literal["active", "offline"]
    lan_ip: str

    @validator("lan_ip")
    def validate_ip(cls, v):
        if not v.startswith("192.168.") and not v.startswith("10.") and not v.startswith("172."):
            raise ValueError("lan_ip must be within a private subnet range (e.g. 192.168.x.x)")
        return v
