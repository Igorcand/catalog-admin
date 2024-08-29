from uuid import UUID
from dataclasses import dataclass, field
from core.genre.application.use_cases.exceptions import RelatedCategoriesNotFound, InvalidGenre
from src.core.genre.domain.genre import Genre
from src.core.genre.domain.genre_repository import GenreRepository

@dataclass
class GenreOutput:
    id: UUID
    name: str
    is_active: bool
    categories: set[UUID]

class ListGenre:
    def __init__(self, repository: GenreRepository) -> None:
        self.repository = repository

    @dataclass
    class Input:
        pass

    @dataclass
    class Output:
        data: list[GenreOutput]


    def execute(self, input: Input):
        genres = self.repository.list()
        mapped_genres = [
            GenreOutput(
                id=genre.id,
                name=genre.name,
                is_active=genre.is_active,
                categories=genre.categories,
            ) for genre in genres
        ]
        return self.Output(data=mapped_genres)