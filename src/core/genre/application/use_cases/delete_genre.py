from uuid import UUID
from dataclasses import dataclass
from core.genre.domain.genre_repository import GenreRepository
from src.core.genre.application.exceptions import GenreNotFound



class DeleteGenre:
    def __init__(self, repository: GenreRepository) -> None:
        self.repository = repository

    @dataclass
    class Input:
        id: UUID

    def execute(self, input: Input) -> None:
        genre = self.repository.get_by_id(id=input.id)
        if genre is None:
            raise GenreNotFound(f"Genre with {input.id} not found")

        self.repository.delete(genre.id)
    