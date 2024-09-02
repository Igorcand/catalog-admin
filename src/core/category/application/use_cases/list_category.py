from uuid import UUID
from dataclasses import dataclass
from src.core.category.domain.category import Category
from src.core.category.domain.category_repository import CategoryRepository
from src.core.category.application.use_cases.exceptions import CategoryNotFound

@dataclass
class ListCategoryRequest:
    order_by: str = "name"

@dataclass
class CategoryOutput:
    id: UUID
    name: str
    description: str 
    is_active: bool

@dataclass
class ListCategoryResponse:
    data: list[CategoryOutput]


class ListCategory:
    def __init__(self, repository: CategoryRepository) -> None:
        self.repository = repository

    def execute(self, request: ListCategoryRequest) ->ListCategoryResponse:
        categories = self.repository.list()
        data = [
                CategoryOutput(
                    id=category.id,
                    name=category.name,
                    description=category.description,
                    is_active=category.is_active,
                ) for category in categories
            ]
        if request.order_by:
            try:
                data = sorted(data, key=lambda category: getattr(category, request.order_by))
            except:
                pass 

        return ListCategoryResponse(data = data)
    