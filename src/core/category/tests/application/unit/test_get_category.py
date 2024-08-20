from unittest.mock import create_autospec, MagicMock
from uuid import UUID, uuid4
from src.core.category.application.use_cases.get_category import GetCategory, GetCategoryRequest, GetCategoryResponse
from src.core.category.application.use_cases.exceptions import CategoryNotFound
from src.core.category.application.category_repository import CategoryRepository
from src.core.category.domain.category import Category
import pytest

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
    
    def test_return_category_not_exists(self):

        mock_repository = create_autospec(CategoryRepository)
        mock_repository.get_by_id.side_effect = CategoryNotFound()

        use_case = GetCategory(repository=mock_repository)

        id = uuid4()
        with pytest.raises(CategoryNotFound) as exc_info:
            response = use_case.execute(GetCategoryRequest(id=id))

        assert exc_info.type is CategoryNotFound

    