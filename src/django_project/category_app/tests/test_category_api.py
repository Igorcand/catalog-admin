from rest_framework.status import HTTP_200_OK, HTTP_400_BAD_REQUEST, HTTP_404_NOT_FOUND
from rest_framework.test import APIClient
from django_project.category_app.repository import DjangoORMCategoryRepository
from src.core.category.domain.category import Category
import pytest 
from uuid import uuid4

@pytest.fixture
def category_movie():
    return Category(
        name= "Movie",
        description="Description"
    )

@pytest.fixture
def category_repository() -> DjangoORMCategoryRepository:
    return DjangoORMCategoryRepository()


@pytest.mark.django_db
class TestCategoryAPI():

    def test_list_categories(self,category_movie: Category,category_repository: DjangoORMCategoryRepository) -> None:
        category_repository.save(category_movie)
        url = "/api/categories/"
        response = APIClient().get(url)

        expected_data = [
            {
                "id": str(category_movie.id),
                "name": category_movie.name,
                "description": category_movie.description,
                "is_active": category_movie.is_active,
            }
        ]
        assert response.status_code == HTTP_200_OK
        assert response.data == expected_data
        assert len(response.data) == 1

@pytest.mark.django_db
class TestRetrieveAPI():
    def test_when_id_is_invalid_return_400(self) -> None:
        url = f"/api/categories/159761298546/"
        response = APIClient().get(url)

        assert response.status_code == HTTP_400_BAD_REQUEST

    def test_return_category_when_exists(self, category_movie: Category, category_repository: DjangoORMCategoryRepository):
        category_repository.save(category_movie)
        url = f"/api/categories/{category_movie.id}/"
        response = APIClient().get(url)

        expected_data = {
                "id": str(category_movie.id),
                "name": category_movie.name,
                "description": category_movie.description,
                "is_active": category_movie.is_active,
            
        }
        assert response.status_code == HTTP_200_OK
        assert response.data == expected_data

    def test_return_404_when_not_exists(self):
        url = f"/api/categories/{uuid4()}/"
        response = APIClient().get(url)

        assert response.status_code == HTTP_404_NOT_FOUND
