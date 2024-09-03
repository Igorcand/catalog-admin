from unittest.mock import create_autospec
from uuid import uuid4
from src.core.category.application.use_cases.update_category import UpdateCategory, UpdateCategoryRequest
from src.core.category.application.use_cases.exceptions import CategoryNotFound
from src.core.category.domain.category_repository import CategoryRepository
from src.core.category.domain.category import Category
import pytest

@pytest.mark.category
class TestUpdateCategory:
    def test_update_category_name(self):
        category = Category(
            id=uuid4(),
            name="Filme", 
            description="Desc", 
            is_active=True
        )
        mock_repository = create_autospec(CategoryRepository)
        mock_repository.get_by_id.return_value = category

        use_case = UpdateCategory(repository=mock_repository)
        request = UpdateCategoryRequest(
            id=category.id,
            name="Serie"
            )
        
        use_case.execute(request)

        assert category.name == "Serie"
        assert category.description == "Desc"
        mock_repository.update.assert_called_once_with(category)

    def test_update_description_name(self):
        category = Category(
            id=uuid4(),
            name="Filme", 
            description="Desc", 
            is_active=True
        )
        mock_repository = create_autospec(CategoryRepository)
        mock_repository.get_by_id.return_value = category

        use_case = UpdateCategory(repository=mock_repository)
        request = UpdateCategoryRequest(
            id=category.id,
            description="Description"
            )
        
        use_case.execute(request)

        assert category.name == "Filme"
        assert category.description == "Description"
        mock_repository.update.assert_called_once_with(category) 

    def test_can_deactivate_category(self):
        category = Category(
            id=uuid4(),
            name="Filme", 
            description="Desc", 
            is_active=True
        )
        mock_repository = create_autospec(CategoryRepository)
        mock_repository.get_by_id.return_value = category

        use_case = UpdateCategory(repository=mock_repository)
        request = UpdateCategoryRequest(
            id=category.id,
            is_active=False
            )
        
        use_case.execute(request)

        assert category.is_active == False
        assert category.name == "Filme"
        assert category.description == "Desc"
        mock_repository.update.assert_called_once_with(category)  

    def test_can_activate_category(self):
        category = Category(
            id=uuid4(),
            name="Filme", 
            description="Desc", 
            is_active=False
        )
        mock_repository = create_autospec(CategoryRepository)
        mock_repository.get_by_id.return_value = category

        use_case = UpdateCategory(repository=mock_repository)
        request = UpdateCategoryRequest(
            id=category.id,
            is_active=True
            )
        
        use_case.execute(request)

        assert category.is_active == True
        assert category.name == "Filme"
        assert category.description == "Desc"
        mock_repository.update.assert_called_once_with(category)   