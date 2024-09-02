from uuid import UUID
from dataclasses import dataclass
from src.core.category.domain.category import Category
from src.core.category.domain.category_repository import CategoryRepository
from src.core.category.application.use_cases.exceptions import CategoryNotFound
from enum import StrEnum

class CategoryFilterByType(StrEnum):
    NAME = "name"
    DESCRIPTION = "description"

@dataclass
class ListCategoryRequest:
    order_by: CategoryFilterByType = ""

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
            if request.order_by and request.order_by in CategoryFilterByType:
                data = sorted(data, key=lambda category: getattr(category, request.order_by))
            

        return ListCategoryResponse(data = data)
    