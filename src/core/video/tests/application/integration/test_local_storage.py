from src.core._shered.infrastructure.storage.local_storage import LocalStorage
import pytest

@pytest.mark.video
class TestLocalStorage:
    def test_init_local_storage(self):
        storage = LocalStorage()