from uuid import UUID
from dataclasses import dataclass
from src.core.genre.domain.genre_repository import GenreRepository
from enum import StrEnum

class GenreFilterByType(StrEnum):
    NAME = "name"

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
        order_by: GenreFilterByType = ""

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
        if input.order_by:
            if input.order_by and input.order_by in GenreFilterByType:
                mapped_genres = sorted(mapped_genres, key=lambda genre: getattr(genre, input.order_by))

        return self.Output(data=mapped_genres)