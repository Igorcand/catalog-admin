from uuid import UUID, uuid4
from src.core.category.application.use_cases.get_category import GetCategory, GetCategoryRequest, GetCategoryResponse
from src.core.category.domain.category import Category

from src.core.category.application.use_cases.exceptions import InvalidCategoryData
from src.core.category.infra.in_memory_category_repository import InMemoryCategoryRepository
from src.core.category.application.use_cases.exceptions import CategoryNotFound
import pytest

class TestGetCategory:
    def test_get_category_by_id(self):
        category = Category(
            name="Filme",
            description="Categoria para filmes",
            is_active=True
        )
        repository = InMemoryCategoryRepository(categories=[category])
        use_case = GetCategory(repository=repository)

        request = GetCategoryRequest(
            id=category.id)

        response = use_case.execute(request)

        assert response == GetCategoryResponse(
            id = category.id,
            name="Filme",
            description="Categoria para filmes",
            is_active=True
        )
    
    def test_when_category_does_not_exist_then_raise_exception(self):
        category = Category(
            name="Filme",
            description="Categoria para filmes",
            is_active=True
        )
        repository = InMemoryCategoryRepository(categories=[category])
        use_case = GetCategory(repository=repository)

        not_found_id = uuid4()
        request = GetCategoryRequest(id=not_found_id)

        with pytest.raises(CategoryNotFound) as exc:
            use_case.execute(request)

        


