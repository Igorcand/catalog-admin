from uuid import UUID
from dataclasses import dataclass
from src.core.genre.domain.genre_repository import GenreRepository
from enum import StrEnum
from src.core._shered.domain.pagination import ListOutputMeta, ListOutput
from src import config

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
        current_page: str = 1

    @dataclass
    class Output(ListOutput[GenreOutput]):
        pass


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
        
        page_offset = (input.current_page -1) * config.DEFAULT_PAGE_SIZE
        genres_page = mapped_genres[page_offset:page_offset+config.DEFAULT_PAGE_SIZE]

        return self.Output(
            data=genres_page,
            meta = ListOutputMeta(
                current_page = input.current_page,
                per_page = config.DEFAULT_PAGE_SIZE,
                total = len(mapped_genres)
            )
            )