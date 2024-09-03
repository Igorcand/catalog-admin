from unittest.mock import create_autospec
from uuid import uuid4
from src.core.category.application.use_cases.get_category import GetCategory, GetCategoryRequest, GetCategoryResponse
from src.core.category.application.use_cases.exceptions import CategoryNotFound
from src.core.category.domain.category_repository import CategoryRepository
from src.core.category.domain.category import Category
import pytest

@pytest.mark.category
class TestGetCateory:
    def test_return_found_category(self):
        category = Category(
            name="Filme", 
            description="Desc", 
            is_active=True
        )
        mock_repository = create_autospec(CategoryRepository)
        mock_repository.get_by_id.return_value = category

        use_case = GetCategory(repository=mock_repository)
        request = GetCategoryRequest(id=category.id)
        response = use_case.execute(request)

        assert response == GetCategoryResponse(
            id = category.id, 
            name="Filme", 
            description="Desc", 
            is_active=True

        )
    
    def test_when_category_not_found_then_raise_exception(self):
        mock_repository = create_autospec(CategoryRepository)
        mock_repository.get_by_id.return_value = None

        use_case = GetCategory(repository=mock_repository)
        request = GetCategoryRequest(id=uuid4())

        with pytest.raises(CategoryNotFound):
            use_case.execute(request)


    