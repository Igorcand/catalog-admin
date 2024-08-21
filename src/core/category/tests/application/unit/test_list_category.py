from unittest.mock import create_autospec
from src.core.category.application.use_cases.list_category import ListCategory, ListCategoryRequest, ListCategoryResponse, CategoryOutput
from src.core.category.application.category_repository import CategoryRepository
from src.core.category.domain.category import Category


class TestListCategory:
    def test_when_no_categories_in_repository_then_return_empty_list(self):
        category = Category(
            name="Filme", 
            description="Desc", 
        )
        mock_repository = create_autospec(CategoryRepository)
        mock_repository.list.return_value = []

        use_case = ListCategory(repository=mock_repository)
        request = ListCategoryRequest()
        response = use_case.execute(request)

        assert response == ListCategoryResponse(data=[])
    
    def test_when_categories_in_repository_then_return_list(self):
        category = Category(
            name="Filme", 
            description="Desc", 
        )
        mock_repository = create_autospec(CategoryRepository)
        mock_repository.list.return_value = [category]

        use_case = ListCategory(repository=mock_repository)
        request = ListCategoryRequest()
        response = use_case.execute(request)

        assert response == ListCategoryResponse(
            data=[
                CategoryOutput(
                    id=category.id,
                    name=category.name,
                    description=category.description,
                    is_active=category.is_active,
                )
            ]
        )