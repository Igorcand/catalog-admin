import pytest 
from src.core.category.domain.category import Category
from src.core.genre.application.use_cases.update_genre import UpdateGenre
from src.core.genre.domain.genre import Genre
from src.core.category.infra.in_memory_category_repository import InMemoryCategoryRepository
from src.core.genre.infra.in_memory_genre_repository import InMemoryGenreRepository



@pytest.fixture
def movie_category() -> Category:
    return Category(name="Movie")

@pytest.fixture
def documentary_category() -> Category:
    return Category(name="Documentary")


class TestUpdateGenre: 
    def test_update_genre_with_valid_data_should_success(
            self,
            movie_category,
            documentary_category,
            ):

        category_repository = InMemoryCategoryRepository(categories=[movie_category, documentary_category])
        
        genre_repository = InMemoryGenreRepository()
        genre = Genre(name='Drama', is_active=True, categories={movie_category.id})
        genre_repository.save(genre)

        use_case = UpdateGenre(repository=genre_repository, category_repository=category_repository)
        input = UpdateGenre.Input(
                    id=genre.id,
                    name="Romance",
                    is_active=False,
                    categories={movie_category.id, documentary_category.id}
                )

        use_case.execute(input=input)

        updated_genre = genre_repository.get_by_id(genre.id)
        
        assert updated_genre.name == "Romance"
        assert updated_genre.is_active is False 
        assert updated_genre
        .categories == {movie_category.id, documentary_category.id}

