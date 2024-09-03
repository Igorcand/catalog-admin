import pytest 
from uuid import uuid4
from src.core.genre.domain.genre import Genre
from src.django_project.genre_app.repository import DjangoORMGenreRepository
from src.django_project.category_app.repository import DjangoORMCategoryRepository
from src.core.category.domain.category import Category

from src.django_project.genre_app.models import Genre as GenreORM


@pytest.mark.django_db
@pytest.mark.web_service
class TestSaveGenre:
    def test_saves_genre_in_database(self):
        genre = Genre(name="Action")
        genre_repository = DjangoORMGenreRepository() 

        assert GenreORM.objects.count() == 0
        genre_repository.save(genre)

        assert GenreORM.objects.count() == 1
        genre_model = GenreORM.objects.first()
        assert genre_model.id == genre.id
        assert genre_model.name == genre.name
        assert genre_model.is_active == genre.is_active

    def test_saves_genre_with_categories(self):
        repository = DjangoORMGenreRepository()
        category_repository = DjangoORMCategoryRepository()

        category = Category(name="Movie")
        category_repository.save(category)

        genre = Genre(name="Action")
        genre.add_category(category.id)
        
        assert GenreORM.objects.count() == 0
        repository.save(genre)
        assert GenreORM.objects.count() == 1

        genre_model = GenreORM.objects.get(id=genre.id)
        related_category = genre_model.categories.get()

        assert genre_model.id == genre.id
        assert genre_model.name == genre.name
        assert genre_model.is_active == genre.is_active
        assert related_category.id == category.id

@pytest.mark.django_db
@pytest.mark.web_service
class TestGetGenre:
    def test_get_genre_does_not_exists_should_return_none(self):
        genre_repository = DjangoORMGenreRepository() 

        assert GenreORM.objects.count() == 0

        genre = genre_repository.get_by_id(id=uuid4())
        assert genre is None
        assert GenreORM.objects.count() == 0
    
    def test_get_genre_existing_should_return_success(self):
        genre = Genre(name="Action")
        genre_repository = DjangoORMGenreRepository() 

        assert GenreORM.objects.count() == 0
        genre_repository.save(genre)
        assert GenreORM.objects.count() == 1

        genre_model = genre_repository.get_by_id(id=genre.id)
        assert genre_model.id == genre.id
        assert genre_model.name == genre.name
        assert genre_model.is_active == genre.is_active
 

@pytest.mark.django_db
@pytest.mark.web_service
class TestDeleteGenre:
    def test_delete_genre_does_not_exists_should_return_none(self):
        genre_repository = DjangoORMGenreRepository() 

        assert GenreORM.objects.count() == 0

        genre_repository.delete(id=uuid4())

        assert GenreORM.objects.count() == 0
    
    def test_delete_genre_existing_should_return_success(self):
        genre = Genre(name="Action")
        genre_repository = DjangoORMGenreRepository() 

        assert GenreORM.objects.count() == 0
        genre_repository.save(genre)
        assert GenreORM.objects.count() == 1

        genre_repository.delete(id=genre.id)
        assert GenreORM.objects.count() == 0

@pytest.mark.django_db
@pytest.mark.web_service
class TestUpdateGenre:    
    def test_update_genre_existing_should_return_success(self):
        genre = Genre(name="Action")
        genre_repository = DjangoORMGenreRepository() 

        assert GenreORM.objects.count() == 0
        genre_repository.save(genre)
        assert GenreORM.objects.count() == 1

        genre_model = genre_repository.get_by_id(id=genre.id)
        assert genre_model.id == genre.id
        assert genre_model.name == genre.name
        assert genre_model.is_active == genre.is_active

        update_genre = Genre(id=genre.id, name="Romance", is_active=False)
        genre_repository.update(update_genre)

        genre_model_uptaded = genre_repository.get_by_id(id=genre.id)
        assert genre_model_uptaded.id == update_genre.id
        assert genre_model_uptaded.name == update_genre.name
        assert genre_model_uptaded.is_active == update_genre.is_active

@pytest.mark.django_db
@pytest.mark.web_service
class TestGetGenre:    
    def test_get_genre_existing_should_return_success(self):
        genre = Genre(name="Action")
        genre_repository = DjangoORMGenreRepository() 

        assert GenreORM.objects.count() == 0
        genre_repository.save(genre)
        assert GenreORM.objects.count() == 1

        genre_model = genre_repository.get_by_id(id=genre.id)
        assert genre_model.id == genre.id
        assert genre_model.name == genre.name
        assert genre_model.is_active == genre.is_active

