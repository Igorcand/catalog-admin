from uuid import uuid4
from src.core.genre.application.use_cases.list_genre import ListGenre, GenreOutput
from src.core.genre.domain.genre_repository import GenreRepository
from src.core.genre.domain.genre import Genre
from unittest.mock import create_autospec
from src.core._shered.domain.pagination import ListOutputMeta
import pytest

@pytest.mark.genre
class TestListGenre:
    def test_list_genres_with_associated_categories(self):
        
        genre_repository = create_autospec(GenreRepository)
        cat_1_id = uuid4()
        cat_2_id = uuid4()

        genre_drama = Genre(name="Drama", categories={cat_1_id, cat_2_id})
        genre_romance = Genre(name="Romance", categories=set())

        genre_repository.list.return_value = [genre_drama, genre_romance]


        use_case = ListGenre(repository=genre_repository)
        output = use_case.execute(ListGenre.Input())

        assert output == ListGenre.Output(
            data=[
                GenreOutput(
                    id=genre_drama.id,
                    name="Drama",
                    categories={cat_1_id, cat_2_id},
                    is_active=True,
                ),
                GenreOutput(
                    id=genre_romance.id,
                    name="Romance",
                    categories=set(),
                    is_active=True,
                ),
            ],
            meta = ListOutputMeta(current_page=1, per_page=2, total=2)
        )

    def test_when_no_genres_exist_then_return_empty_data(self):
        genre_repository = create_autospec(GenreRepository)
        genre_repository.list.return_value = []

        use_case = ListGenre(repository=genre_repository)
        output = use_case.execute(ListGenre.Input())

        assert output == ListGenre.Output(
            data=[],
            meta = ListOutputMeta(current_page=1, per_page=2, total=0)
            )