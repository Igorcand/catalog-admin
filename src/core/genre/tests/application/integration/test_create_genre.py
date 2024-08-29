import pytest 
from uuid import uuid4, UUID
from src.core.category.domain.category import Category
from src.core.genre.application.use_cases.create_genre import CreateGenre
from src.core.category.domain.category_repository import CategoryRepository
from src.core.category.infra.in_memory_category_repository import InMemoryCategoryRepository
from src.core.genre.infra.in_memory_genre_repository import InMemoryGenreRepository

from src.core.genre.application.use_cases.exceptions import RelatedCategoriesNotFound


@pytest.fixture
def movie_category() -> Category:
    return Category(name="Movie")

@pytest.fixture
def documentary_category() -> Category:
    return Category(name="Documentary")

@pytest.fixture
def category_repository(movie_category, documentary_category) -> CategoryRepository:
    return InMemoryCategoryRepository(categories=[movie_category, documentary_category])



class TestCreateGenre:
    def test_create_genre_with_associated_categories(
            self,
            movie_category, 
            documentary_category, 
            category_repository
    ):
        genre_repository = InMemoryGenreRepository()
        use_case = CreateGenre(
            repository=genre_repository,
            category_repository = category_repository
        )

        input = CreateGenre.Input(
            name="Action", 
            categories={movie_category.id, documentary_category.id}
            )
        output = use_case.execute(input)
        
        assert isinstance(output.id, UUID)
        saved_genre = genre_repository.get_by_id(output.id)
        assert saved_genre.name == "Action"

    def test_create_genre_with_inexistent_categories_raise_an_error(
            self,
            category_repository):
        
        genre_repository = InMemoryGenreRepository()
        use_case = CreateGenre(
            repository=genre_repository,
            category_repository = category_repository
        )

        category_id = uuid4()
        input = CreateGenre.Input(
            name="Action", 
            categories={category_id}
            )
        with pytest.raises(RelatedCategoriesNotFound) as exc_info:
            use_case.execute(input)
        
        assert str(category_id) in str(exc_info.value)

    def test_create_genre_without_categories(self):
        genre_repository = InMemoryGenreRepository()
        category_repository = InMemoryCategoryRepository()

        use_case = CreateGenre(
            repository=genre_repository,
            category_repository = category_repository
        )

        input = CreateGenre.Input(
            name="Action", 
            categories=set()
            )
        output = use_case.execute(input)
        
        assert isinstance(output.id, UUID)
        saved_genre = genre_repository.get_by_id(output.id)
        assert saved_genre.name == "Action" 
        assert saved_genre.categories == set()

