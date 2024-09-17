import mimetypes
from django.conf import settings

from google.cloud import storage
from pathlib import Path
import os
from dotenv import load_dotenv
from src.core._shered.infrastructure.storage.abstract_storage_service import AbstractStorageService

load_dotenv()

class GCSStorage(AbstractStorageService):
    def __init__(self) -> None:
        # Client vai procurar por env var GOOGLE_APPLICATION_CREDENTIALS
        # https://cloud.google.com/docs/authentication/provide-credentials-adc#how-to
        self.client = storage.Client()
        self.bucket = self.client.bucket(os.getenv('CLOUD_STORAGE_BUCKET_NAME'))

    def store(self, file_path: Path, content: bytes, content_type: str = "") -> str:
        blob = self.bucket.blob(str(file_path))

        if not content_type:
            content_type, _ = mimetypes.guess_type(str(file_path))

        blob.upload_from_string(content, content_type=content_type)
        return blob.public_url

    def retrieve(self, file_path: Path) -> bytes:
        blob = self.bucket.blob(str(file_path))
        return blob.download_as_bytes()