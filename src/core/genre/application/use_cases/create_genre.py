from uuid import UUID
from dataclasses import dataclass, field
from core.genre.application.use_cases.exceptions import RelatedCategoriesNotFound, InvalidGenre
from src.core.genre.domain.genre import Genre

class CreateGenre:
    def __init__(self, repository, category_repository) -> None:
        self.repository = repository
        self.category_repository = category_repository

    @dataclass
    class Input:
        name: str
        category_ids : set[UUID] = field(default_factory=set)
        is_active: bool = True

    @dataclass
    class Output:
        id: UUID


    def execute(self, input: Input):
        category_ids = {category.id for category in self.category_repository.list()}
        if not input.category_ids.issubset(category_ids):
            raise RelatedCategoriesNotFound(
                f"Categories not found: {input.category_ids - category_ids}"
            )

        try:
            genre = Genre(
                name=input.name,
                is_active=input.is_active,
                categories = input.category_ids
            )
        except ValueError as e:
            raise InvalidGenre(e)
        
        self.repository.save(genre)
        return self.Output(id=genre.id)