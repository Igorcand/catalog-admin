from uuid import UUID
from django.db import transaction
from src.core.genre.domain.genre_repository import GenreRepository
from src.core.genre.domain.genre import Genre
from src.django_project.genre_app.models import Genre as GenreORM

class DjangoORMGenreRepository(GenreRepository):
    def save(self, genre: Genre):
        with transaction.atomic():
            GenreModelMapper.to_model(genre)

    def get_by_id(self, id: UUID) -> Genre | None:
        try:
            genre_model = GenreORM.objects.get(id=id)
            return GenreModelMapper.to_entity(genre_model)
        except GenreORM.DoesNotExist:
            return None


    def delete(self, id: UUID) -> None:
        GenreORM.objects.filter(id=id).delete()

    def update(self, genre: Genre) -> None:
        try:
            genre_model = GenreORM.objects.get(id=genre.id)
        except GenreORM.DoesNotExist:
            return None
        
        with transaction.atomic():
            GenreORM.objects.filter(id=genre.id).update(
                name=genre.name,
                is_active=genre.is_active
            )

            genre_model.categories.set(genre.categories)
    
    def list(self) -> list[Genre]:
        return [
            GenreModelMapper.to_entity(genre_model)
         for genre_model in GenreORM.objects.all()]

class GenreModelMapper:
    @staticmethod
    def to_model(genre: Genre) -> GenreORM:
        genre_model = GenreORM.objects.create(
            id=genre.id,
            name=genre.name,
            is_active=genre.is_active
        )

        genre_model.categories.set(genre.categories)
        
        return genre_model
    
    def to_entity(genre: GenreORM) -> Genre:
        return Genre(
            id=genre.id,
            name=genre.name,
            is_active=genre.is_active,
            categories={category.id for category in genre.categories.all()}

        )