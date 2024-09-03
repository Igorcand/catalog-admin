from unittest.mock import create_autospec
from src.core.category.application.use_cases.list_category import ListCategory, ListCategoryRequest, ListCategoryResponse, CategoryOutput
from src.core._shered.pagination import ListOutputMeta
from src.core.category.domain.category_repository import CategoryRepository
from src.core.category.domain.category import Category
import pytest

@pytest.mark.category
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

        assert response == ListCategoryResponse(
            data=[],
            meta = ListOutputMeta(current_page=1, per_page=2, total=0)
            )
    
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
                ),
            ],
            meta = ListOutputMeta(current_page=1, per_page=2, total=1)
        )
    
    def test_when_categories_in_repository_and_order_categories_by_name(self):
        category_movie = Category(name="Movie", description="Desc")
        category_action = Category(name="Action", description="Desc")

        mock_repository = create_autospec(CategoryRepository)

        use_case = ListCategory(repository=mock_repository)
        request = ListCategoryRequest(order_by="name")

        mock_repository.list.return_value = [category_action, category_movie]

        response = use_case.execute(request)

        assert response == ListCategoryResponse(
            data=[
                CategoryOutput(
                    id=category_action.id,
                    name=category_action.name,
                    description=category_action.description,
                    is_active=category_action.is_active,
                ),
                CategoryOutput(
                    id=category_movie.id,
                    name=category_movie.name,
                    description=category_movie.description,
                    is_active=category_movie.is_active,
                ),
            ],
            meta = ListOutputMeta(current_page=1, per_page=2, total=2)
        )
    
    def test_when_categories_in_repository_and_current_page_2(self):
        category_movie = Category(name="Movie", description="")
        category_action = Category(name="Action", description="")
        category_documentary = Category(name="Documentary", description="")


        mock_repository = create_autospec(CategoryRepository)

        use_case = ListCategory(repository=mock_repository)
        request = ListCategoryRequest(current_page=2)

        mock_repository.list.return_value = [category_action, category_movie, category_documentary]

        response = use_case.execute(request)

        assert response == ListCategoryResponse(
            data=[
                CategoryOutput(
                    id=category_documentary.id,
                    name=category_documentary.name,
                    description=category_documentary.description,
                    is_active=category_documentary.is_active,
                )
            ],
            meta = ListOutputMeta(current_page=2, per_page=2, total=3)
        )