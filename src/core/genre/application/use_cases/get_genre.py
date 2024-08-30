from uuid import UUID
from dataclasses import dataclass
from src.core.genre.domain.genre_repository import GenreRepository
from src.core.genre.application.use_cases.exceptions import GenreNotFound




class GetGenre:
    def __init__(self, repository: GenreRepository) -> None:
        self.repository = repository
    
    @dataclass
    class Input:
        id: UUID

    @dataclass
    class Output:
        id: UUID
        name: str
        is_active: bool 
        categories: set[UUID]

    def execute(self, input: Input) -> Output:

        genre = self.repository.get_by_id(id=input.id)

        if genre is None:
            raise GenreNotFound(f"Genre with {input.id} not found")

        return self.Output(
            id=genre.id,
            name=genre.name,
            is_active=genre.is_active,
            categories=genre.categories
            )
    