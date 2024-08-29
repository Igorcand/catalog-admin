import pytest 
from uuid import uuid4, UUID
from src.core.category.domain.category import Category
from src.core.genre.application.use_cases.update_genre import UpdateGenre
from src.core.genre.domain.genre_repository import GenreRepository
from src.core.category.domain.category_repository import CategoryRepository
from core.genre.application.use_cases.exceptions import RelatedCategoriesNotFound, InvalidGenre, GenreNotFound
from src.core.genre.domain.genre import Genre
from unittest.mock import create_autospec



@pytest.fixture
def mock_genre_repository() -> GenreRepository:
    return create_autospec(GenreRepository)

@pytest.fixture
def movie_category() -> Category:
    return Category(name="Movie")

@pytest.fixture
def documentary_category() -> Category:
    return Category(name="Documentary")

@pytest.fixture
def mock_category_repository_with_categories(movie_category, documentary_category) -> CategoryRepository:
    repository = create_autospec(CategoryRepository)
    repository.list.return_value = [movie_category, documentary_category]
    return repository

@pytest.fixture
def mock_empty_category_repository() -> CategoryRepository:
    repository = create_autospec(CategoryRepository)
    repository.list.return_value = []
    return repository

class TestUpdateGenre:

    def test_update_genre_does_not_exist_than_raise_exceptions(
            self,
            movie_category,
            documentary_category,
            mock_genre_repository,
            mock_category_repository_with_categories
            ):

        mock_genre_repository.get_by_id.return_value = None

        use_case = UpdateGenre(repository=mock_genre_repository, category_repository=mock_category_repository_with_categories)
        input = UpdateGenre.Input(
                    id=uuid4(),
                    name="Drama",
                    is_active=True,
                    categories={movie_category.id, documentary_category.id}
                )

        with pytest.raises(GenreNotFound) as exc_info:
            use_case.execute(input=input)

        assert str(exc_info.value) == f"Genre with {input.id} not found"
        mock_genre_repository.update.assert_not_called() 
    
    def test_update_genre_with_category_related_not_exists_than_raise_exceptions(
            self,
            movie_category,
            documentary_category,
            mock_genre_repository,
            mock_category_repository_with_categories
            ):

        genre = Genre(name='Drama', is_active=True, categories={movie_category.id, documentary_category.id})
        mock_genre_repository.get_by_id.return_value = genre

        use_case = UpdateGenre(repository=mock_genre_repository, category_repository=mock_category_repository_with_categories)
        input = UpdateGenre.Input(
                    id=uuid4(),
                    name="Drama",
                    is_active=True,
                    categories={movie_category.id, documentary_category.id, uuid4()}
                )

        with pytest.raises(RelatedCategoriesNotFound):
            use_case.execute(input=input)

        mock_genre_repository.update.assert_not_called() 
    
    def test_update_genre_invalid_genre_data_than_raise_exceptions(
            self,
            movie_category,
            documentary_category,
            mock_genre_repository,
            mock_category_repository_with_categories
            ):

        genre = Genre(name='Drama', is_active=True, categories={movie_category.id, documentary_category.id})
        mock_genre_repository.get_by_id.return_value = genre

        use_case = UpdateGenre(repository=mock_genre_repository, category_repository=mock_category_repository_with_categories)
        input = UpdateGenre.Input(
                    id=uuid4(),
                    name="",
                    is_active=True,
                    categories={movie_category.id, documentary_category.id}
                )

        with pytest.raises(InvalidGenre):
            use_case.execute(input=input)

        mock_genre_repository.update.assert_not_called() 
    
    def test_update_genre_with_valid_data_should_success(
            self,
            movie_category,
            documentary_category,
            mock_genre_repository,
            mock_category_repository_with_categories
            ):

        genre = Genre(name='Drama', is_active=True, categories={movie_category.id})
        mock_genre_repository.get_by_id.return_value = genre

        use_case = UpdateGenre(repository=mock_genre_repository, category_repository=mock_category_repository_with_categories)
        input = UpdateGenre.Input(
                    id=genre.id,
                    name="Romance",
                    is_active=False,
                    categories={movie_category.id, documentary_category.id}
                )

        use_case.execute(input=input)

        mock_genre_repository.update.assert_called_once_with(genre)
        
        assert genre.name == "Romance"
        assert genre.is_active is False 
        assert genre.categories == {movie_category.id, documentary_category.id}

