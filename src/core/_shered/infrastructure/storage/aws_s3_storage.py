import mimetypes
import os
import boto3
from dotenv import load_dotenv
from pathlib import Path
from src.core._shered.infrastructure.storage.abstract_storage_service import AbstractStorageService

load_dotenv()

class S3Storage(AbstractStorageService):
    def __init__(self) -> None:
        # Inicializando o cliente do S3
        self.s3_client = boto3.client(
            's3',
            aws_access_key_id=os.getenv('AWS_ACCESS_KEY_ID'),
            aws_secret_access_key=os.getenv('AWS_SECRET_ACCESS_KEY'),
            region_name=os.getenv('AWS_REGION')
        )
        self.bucket_name = os.getenv('AWS_S3_BUCKET_NAME')

    def store(self, file_path: Path, content: bytes, content_type: str = "") -> str:
        if not content_type:
            content_type, _ = mimetypes.guess_type(str(file_path))

        self.s3_client.put_object(
            Bucket=self.bucket_name,
            Key=str(file_path),
            Body=content,
            ContentType=content_type
        )

        # Construindo a URL pública para o objeto armazenado
        public_url = f"https://{self.bucket_name}.s3.{os.getenv('AWS_REGION')}.amazonaws.com/{file_path}"
        return public_url

    def retrieve(self, file_path: Path) -> bytes:
        response = self.s3_client.get_object(Bucket=self.bucket_name, Key=str(file_path))
        return response['Body'].read()
