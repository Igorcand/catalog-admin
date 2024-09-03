from unittest.mock import create_autospec
from uuid import uuid4
from src.core.genre.application.use_cases.get_genre import GetGenre
from src.core.genre.application.use_cases.exceptions import GenreNotFound
from src.core.genre.domain.genre_repository import GenreRepository
from src.core.genre.domain.genre import Genre
import pytest

@pytest.mark.genre
class TestGetGenre:
    def test_return_found_genre(self):
        genre = Genre(
            name="Action", 
            is_active=True,
            categories=set()
        )
        mock_repository = create_autospec(GenreRepository)
        mock_repository.get_by_id.return_value = genre

        use_case = GetGenre(repository=mock_repository)
        input = GetGenre.Input(id=genre.id)
        response = use_case.execute(input=input)

        assert response == GetGenre.Output(
            id = genre.id, 
            name="Action", 
            is_active=True,
            categories=set()

        )
    
    def test_when_genre_not_found_then_raise_exception(self):
        mock_repository = create_autospec(GenreRepository)
        mock_repository.get_by_id.return_value = None

        use_case = GetGenre(repository=mock_repository)
        request = GetGenre.Input(id=uuid4())

        with pytest.raises(GenreNotFound):
            use_case.execute(request)


    