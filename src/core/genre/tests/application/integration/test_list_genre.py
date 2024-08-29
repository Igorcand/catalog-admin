from src.core.category.domain.category import Category
from src.core.category.infra.in_memory_category_repository import InMemoryCategoryRepository
from src.core.genre.infra.in_memory_genre_repository import InMemoryGenreRepository
from src.core.genre.domain.genre import Genre
from src.core.genre.application.use_cases.list_genre import ListGenre, GenreOutput


class TestListGenre:
    def test_list_genres_with_associated_categories(self):
        category_repository = InMemoryCategoryRepository()
        movie_category = Category(name="Movie")
        documentary_category = Category(name="Documentary")

        category_repository.save(movie_category)
        category_repository.save(documentary_category)

        genre_repository = InMemoryGenreRepository()
        genre = Genre(name="Drama", categories={movie_category.id,documentary_category.id})
        genre_repository.save(genre)

        use_case = ListGenre(repository=genre_repository)
        output = use_case.execute(input=ListGenre.Input())

        assert len(output.data) == 1
        assert output == ListGenre.Output(
            data = [GenreOutput(
                    id = genre.id,
                    name=genre.name,
                    is_active=True,
                    categories={movie_category.id, documentary_category.id}
                )
            ]
        )
    
    def test_list_genres_without_associated_categories(self):
        genre_repository = InMemoryGenreRepository()
        genre = Genre(name="Drama", categories=set())
        genre_repository.save(genre)

        use_case = ListGenre(repository=genre_repository)
        output = use_case.execute(input=ListGenre.Input())

        assert len(output.data) == 1
        assert output == ListGenre.Output(
            data = [GenreOutput(
                    id = genre.id,
                    name=genre.name,
                    is_active=True,
                    categories=set()
                )
            ]
        )