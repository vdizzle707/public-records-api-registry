#!/usr/bin/env python3
"""
CHRONOS OS // GOOGLE DRIVE VAULT SYNCHRONIZATION ENGINE (PURE PYTHON REST API)
Automates uploading generated PDF dossiers, CSV lead exports, and SQLite audit vaults
to Google Drive using standard library urllib and OAuth Bearer tokens (zero compiled dependencies).
"""

import os
import sys
import json
import logging
import urllib.request
import urllib.error
from pathlib import Path

logging.basicConfig(
    level=logging.INFO,
    format="[%(asctime)s] [%(levelname)s] [GDRIVE-REST] %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S"
)
logger = logging.getLogger("GDriveRestSync")

DRIVE_FOLDER_NAME = "CHRONOS_AUDIT_VAULT_2026"

class GDriveRestSync:
    def __init__(self):
        self.access_token = os.getenv("GOOGLE_ACCESS_TOKEN", "")
        if not self.access_token or self.access_token == "your_oauth_access_token_here":
            logger.error("FATAL: GOOGLE_ACCESS_TOKEN environment variable is missing or invalid.")
            logger.error("       Provide a valid Google OAuth2 Bearer token in production_config.env.")
            raise RuntimeError("CREDENTIALS_MISSING: GOOGLE_ACCESS_TOKEN not configured.")

    def _apiRequest(self, url: str, method: str = "GET", headers: dict = None, data: bytes = None) -> dict:
        req_headers = {"Authorization": f"Bearer {self.access_token}"}
        if headers:
            req_headers.update(headers)

        req = urllib.request.Request(url, data=data, headers=req_headers, method=method)
        try:
            with urllib.request.urlopen(req) as response:
                body = response.read().decode("utf-8")
                return json.loads(body) if body else {}
        except urllib.error.HTTPError as e:
            err_body = e.read().decode("utf-8")
            logger.error(f"HTTPError {e.code}: {e.reason} - {err_body}")
            raise RuntimeError(f"DRIVE_API_HTTP_ERROR_{e.code}: {err_body}") from e
        except Exception as e:
            logger.error(f"API request failed: {e}")
            raise RuntimeError(f"DRIVE_API_EXCEPTION: {e}") from e

    def get_or_create_folder(self) -> str:
        escaped_name = DRIVE_FOLDER_NAME.replace("'", "\\'")
        query = urllib.parse.quote(f"name='{escaped_name}' and mimeType='application/vnd.google-apps.folder' and trashed=false")
        url = f"https://www.googleapis.com/drive/v3/files?q={query}"

        res = self._apiRequest(url, method="GET")
        files = res.get("files", [])
        if files:
            folder_id = files[0]["id"]
            logger.info(f"Found existing Google Drive folder '{DRIVE_FOLDER_NAME}' (ID: {folder_id})")
            return folder_id

        # Create folder
        create_url = "https://www.googleapis.com/drive/v3/files"
        payload = json.dumps({
            "name": DRIVE_FOLDER_NAME,
            "mimeType": "application/vnd.google-apps.folder"
        }).encode("utf-8")
        headers = {"Content-Type": "application/json"}

        res = self._apiRequest(create_url, method="POST", headers=headers, data=payload)
        folder_id = res.get("id")
        logger.info(f"Created new Google Drive folder '{DRIVE_FOLDER_NAME}' (ID: {folder_id})")
        return folder_id

    def upload_file(self, local_path: str, folder_id: str) -> dict:
        path = Path(local_path)
        if not path.exists():
            raise FileNotFoundError(f"LOCAL_FILE_MISSING: {local_path}")

        file_name = path.name
        logger.info(f"Uploading '{file_name}' to Google Drive...")

        # Multipart upload to Google Drive v3 upload endpoint
        upload_url = "https://www.googleapis.com/upload/drive/v3/files?uploadType=multipart"
        
        metadata = json.dumps({
            "name": file_name,
            "parents": [folder_id]
        }).encode("utf-8")

        file_data = path.read_bytes()
        boundary = "foo_bar_baz_chronos_boundary"
        
        body = (
            b"--" + boundary.encode() + b"\r\n"
            b"Content-Type: application/json; charset=UTF-8\r\n\r\n" +
            metadata + b"\r\n" +
            b"--" + boundary.encode() + b"\r\n"
            b"Content-Type: application/octet-stream\r\n\r\n" +
            file_data + b"\r\n" +
            b"--" + boundary.encode() + b"--\r\n"
        )

        headers = {
            "Content-Type": f"multipart/related; boundary={boundary}",
            "Content-Length": str(len(body))
        }

        res = self._apiRequest(upload_url, method="POST", headers=headers, data=body)
        file_id = res.get("id")
        logger.info(f"Successfully uploaded '{file_name}' | File ID: {file_id}")
        return {"success": True, "file_id": file_id, "name": file_name}

    def sync_all_dossiers_and_vaults(self):
        logger.info("Starting pure Python Google Drive synchronization...")
        folder_id = self.get_or_create_folder()

        patterns = ["*.pdf", "*.csv", "*.db", "vault_export_*.json"]
        uploaded_count = 0

        for pattern in patterns:
            for file_path in Path(".").glob(pattern):
                if file_path.is_file():
                    res = self.upload_file(str(file_path), folder_id)
                    if res.get("success"):
                        uploaded_count += 1

        logger.info(f"Google Drive synchronization complete. Total files synced: {uploaded_count}")
        return uploaded_count

if __name__ == "__main__":
    print("=" * 76)
    print("      CHRONOS OS // GOOGLE DRIVE VAULT SYNC (PURE PYTHON REST API)")
    print("=" * 76)
    try:
        sync_client = GDriveRestSync()
        sync_client.sync_all_dossiers_and_vaults()
    except Exception as e:
        logger.error(f"Execution halted: {e}")
        sys.exit(1)
    print("=" * 76)
