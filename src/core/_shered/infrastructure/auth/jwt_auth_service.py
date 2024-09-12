from src.core._shered.infrastructure.auth.auth_service_interface import AuthServiceInterface
from dotenv import load_dotenv
import os
import jwt

load_dotenv()

class JwtAuthService(AuthServiceInterface):
    def __init__(self, token: str = "") -> None:
        raw_public_key = os.getenv('AUTH_PUBLIC_KEY')
        self.public_key = f"-----BEGIN PUBLIC KEY-----\n{raw_public_key}\n-----END PUBLIC KEY-----"
        self.token = token.replace("Bearer ", "", 1)
    
    def _decode_token(self):
        try:
            return jwt.decode(self.token, self.public_key, algorithms=["RS256"], audience="account")
        except:
            return {}

    def is_authenticated(self) -> bool:
        return bool(self._decode_token())
    
    def has_role(self, role: str) -> bool:
        decoded_token = self._decode_token()
        return role in decoded_token.get("realm_access", {}).get("roles", [])