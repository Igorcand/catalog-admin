from uuid import uuid4
from src.core.genre.application.use_cases.get_genre import GetGenre
from src.core.genre.domain.genre import Genre
from src.core.genre.infra.in_memory_genre_repository import InMemoryGenreRepository
from src.core.genre.application.use_cases.exceptions import GenreNotFound
import pytest

@pytest.mark.genre
class TestGetGenre:
    def test_get_genre_by_id(self):
        genre = Genre(
            name="Action",
            is_active=True,
            categories=set()
        )
        repository = InMemoryGenreRepository(genres=[genre])
        use_case = GetGenre(repository=repository)

        input = GetGenre.Input(id=genre.id)

        response = use_case.execute(input)

        assert response == GetGenre.Output(
            id = genre.id,
            name="Action",
            is_active=True,
            categories=set()
        )
    
    def test_when_genre_does_not_exist_then_raise_exception(self):
        genre = Genre(
            name="Action",
            is_active=True,
            categories=set()
        )
        repository = InMemoryGenreRepository(genres=[genre])
        use_case = GetGenre(repository=repository)

        request = GetGenre.Input(id=uuid4())

        with pytest.raises(GenreNotFound) as exc:
            use_case.execute(request)
