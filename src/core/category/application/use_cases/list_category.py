from uuid import UUID
from dataclasses import dataclass, field
from src.core.category.domain.category import Category
from src.core.category.domain.category_repository import CategoryRepository
from src.core.category.application.use_cases.exceptions import CategoryNotFound
from src.core._shered.domain.pagination import ListOutputMeta, ListOutput
from src import config
from enum import StrEnum

class CategoryFilterByType(StrEnum):
    NAME = "name"
    DESCRIPTION = "description"

@dataclass
class ListCategoryRequest:
    order_by: CategoryFilterByType = ""
    current_page: str = 1

@dataclass
class CategoryOutput:
    id: UUID
    name: str
    description: str 
    is_active: bool



@dataclass
class ListCategoryResponse(ListOutput[CategoryOutput]):
    pass


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
        
        
        page_offset = (request.current_page -1) * config.DEFAULT_PAGE_SIZE
        categories_page = data[page_offset:page_offset+config.DEFAULT_PAGE_SIZE]
        return ListCategoryResponse(
            data = categories_page,
            meta = ListOutputMeta(
                current_page = request.current_page,
                per_page = config.DEFAULT_PAGE_SIZE,
                total = len(data)
            )
            )
    