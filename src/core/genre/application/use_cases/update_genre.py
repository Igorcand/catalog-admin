from uuid import UUID
from dataclasses import dataclass
from src.core.genre.domain.genre_repository import GenreRepository
from src.core.category.domain.category_repository import CategoryRepository
from src.core.genre.application.use_cases.exceptions import GenreNotFound, InvalidGenre, RelatedCategoriesNotFound

class UpdateGenre:
    def __init__(self, repository: GenreRepository, category_repository: CategoryRepository) -> None:
        self.repository = repository
        self.category_repository = category_repository

    @dataclass
    class Input:
        id: UUID
        name :str
        is_active: bool
        categories: set[UUID]

    def execute(self, input: Input) -> None:
        genre = self.repository.get_by_id(id=input.id)
        if genre is None:
            raise GenreNotFound(f"Genre with {input.id} not found")
        
        categories = {category.id for category in self.category_repository.list()}
        if not input.categories.issubset(categories):
            raise RelatedCategoriesNotFound(
                f"Categories with provided IDs not found: {input.categories - categories}")

        try:
            if input.is_active is True:
                genre.activate()
            if input.is_active is False:
                genre.deactivate()
            genre.change_name(input.name)

            genre.update_categories(input.categories)
        except ValueError as error:
            raise InvalidGenre(error)

        self.repository.update(genre)
    