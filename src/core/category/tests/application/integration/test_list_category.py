from src.core.category.application.use_cases.list_category import ListCategory, ListCategoryRequest, ListCategoryResponse, CategoryOutput
from src.core.category.domain.category import Category
from src.core.category.infra.in_memory_category_repository import InMemoryCategoryRepository

class TestListCategory:
    def test_then_return_empty_list(self):
        category = Category(
            name="Filme", 
            description="Desc", 
        )
        repository = InMemoryCategoryRepository()

        use_case = ListCategory(repository=repository)
        request = ListCategoryRequest()
        response = use_case.execute(request)

        assert response == ListCategoryResponse(data=[])
    
    def test__return_existing_categories(self):
        category = Category(
            name="Filme", 
            description="Desc", 
        )
        repository = InMemoryCategoryRepository(categories=[category])

        use_case = ListCategory(repository=repository)
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