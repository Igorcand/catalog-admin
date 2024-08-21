from uuid import uuid4
from src.core.category.application.use_cases.update_category import UpdateCategory, UpdateCategoryRequest
from src.core.category.domain.category import Category
from src.core.category.application.use_cases.exceptions import InvalidCategoryData
from src.core.category.infra.in_memory_category_repository import InMemoryCategoryRepository
from src.core.category.application.use_cases.exceptions import CategoryNotFound
import pytest

class TestUpdateCategory:
    def test_can_update_category_name_and_description(self):
        category = Category(
            name="Filme",
            description="Categoria para filmes",
            is_active=True
        )
        repository = InMemoryCategoryRepository(categories=[category])
        use_case = UpdateCategory(repository=repository)

        request = UpdateCategoryRequest(
            id=category.id,
            name= "Serie",
            description="Categoria para series"
            )

        response = use_case.execute(request)

        updated_category = repository.get_by_id(category.id)

        assert updated_category.name == "Serie"
        assert updated_category.description == "Categoria para series"
    
    def test_when_try_update_category_does_not_exist_then_raise_exception(self):
        category = Category(
            name="Filme",
            description="Categoria para filmes",
            is_active=True
        )
        repository = InMemoryCategoryRepository(categories=[category])
        use_case = UpdateCategory(repository=repository)

        request = UpdateCategoryRequest(
            id=uuid4(),
            name= "Serie",
            description="Categoria para series"
            )

        with pytest.raises(CategoryNotFound) as exc:
            use_case.execute(request)
        
        assert category.name == "Filme"
        assert category.description == "Categoria para filmes"
    
    def test_when_try_update_category_with_invalid_then_raise_exception(self):
        category = Category(
            name="Filme",
            description="Categoria para filmes",
            is_active=True
        )
        repository = InMemoryCategoryRepository(categories=[category])
        
        with pytest.raises(InvalidCategoryData) as exc:
            use_case = UpdateCategory(repository=repository)
            request = UpdateCategoryRequest(category.id, name= "")
            use_case.execute(request)
        