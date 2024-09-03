from rest_framework.status import HTTP_200_OK, HTTP_400_BAD_REQUEST, HTTP_404_NOT_FOUND, HTTP_201_CREATED, HTTP_204_NO_CONTENT
from rest_framework.test import APIClient
from src.django_project.category_app.repository import DjangoORMCategoryRepository
from src.core.category.domain.category import Category
import pytest 
from uuid import uuid4, UUID

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
class TestListAPI():

    def test_list_categories(self,category_movie: Category,category_repository: DjangoORMCategoryRepository) -> None:
        category_repository.save(category_movie)
        url = "/api/categories/"
        response = APIClient().get(url)

        expected_data = {
            "data": [
                {
                    "id": str(category_movie.id),
                    "name": category_movie.name,
                    "description": category_movie.description,
                    "is_active": category_movie.is_active,
                }
            ],
            "meta": {
               "current_page": 1,
                "per_page": 2,
                "total": 1 
            }
        }
        assert response.status_code == HTTP_200_OK
        assert response.data == expected_data
        assert len(response.data['data']) == 1

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
            "data": {
                "id": str(category_movie.id),
                "name": category_movie.name,
                "description": category_movie.description,
                "is_active": category_movie.is_active,
            }
            
        }
        assert response.status_code == HTTP_200_OK
        assert response.data == expected_data

    def test_return_404_when_not_exists(self):
        url = f"/api/categories/{uuid4()}/"
        response = APIClient().get(url)

        assert response.status_code == HTTP_404_NOT_FOUND

@pytest.mark.django_db
class TestCreateAPI():
    def test_when_payload_is_invalid_then_return_400(self) -> None:
        url = f"/api/categories/"
        response = APIClient().post(
            url,
            data={
                "name": "",
                "description": "Movie description"
            }
            )

        assert response.status_code == HTTP_400_BAD_REQUEST

    def test_when_payload_is_valid_then_create_category_and_return_201(
            self,
            category_repository: DjangoORMCategoryRepository
            ) -> None:
        
        url = f"/api/categories/"
        response = APIClient().post(
            url,
            data={
                "name": "Movie",
                "description": "Movie description"
            }
            )
        created_category_id = UUID(response.data["id"])

        assert response.status_code == HTTP_201_CREATED
        assert category_repository.get_by_id(created_category_id) == Category(
            id = created_category_id,
            name= "Movie",
            description= "Movie description"
        )

@pytest.mark.django_db
class TestUpdateAPI():
    def test_when_payload_is_invalid_then_return_400(self) -> None:
        url = f"/api/categories/123523634/" #UUID invalid
        response = APIClient().put(
            url,
            data={
                "name": "", # Name must not be blank
                "description": "Movie description"
                # is_active is missing
            }
            )

        assert response.status_code == HTTP_400_BAD_REQUEST
        assert response.data == {
            "name": ["This field may not be blank."],
            "id": ["Must be a valid UUID."],
            "is_active": ["This field is required."]

            }

    def test_when_payload_is_valid_then_update_category_and_return_204(
            self,
            category_movie: Category,
            category_repository: DjangoORMCategoryRepository
            ) -> None:
        
        category_repository.save(category_movie)

        url = f"/api/categories/{category_movie.id}/"
        response = APIClient().put(
            url,
            data={
                "name": "Documentary",
                "description": "Documentary description",
                "is_active": True
            }
            )

        assert response.status_code == HTTP_204_NO_CONTENT
        updated_category = category_repository.get_by_id(category_movie.id)

        assert updated_category.name == "Documentary"
        assert updated_category.description == "Documentary description"
        assert updated_category.is_active is True

    def test_when_category_does_not_exist_then_return_404(self) -> None:
        url = f"/api/categories/{uuid4()}/"
        response = APIClient().put(
            url,
            data={
                "name": "Documentary",
                "description": "Documentary description",
                "is_active": True
            }
            )

        assert response.status_code == HTTP_404_NOT_FOUND

@pytest.mark.django_db
class TestPartialUpdateAPI():
    def test_when_id_is_invalid_then_return_400(self) -> None:
        url = f"/api/categories/123523634/" #UUID invalid
        response = APIClient().patch(
            url,
            data={
                "description": "Movie description"
            }, format="json"
            )

        assert response.status_code == HTTP_400_BAD_REQUEST

    def test_when_payload_is_valid_then_update_partial_category_and_return_204(
            self,
            category_movie: Category,
            category_repository: DjangoORMCategoryRepository
            ) -> None:
        
        category_repository.save(category_movie)

        url = f"/api/categories/{category_movie.id}/"
        response = APIClient().patch(
            url,
            data={
                "name": "Documentary",
            }
            )

        assert response.status_code == HTTP_204_NO_CONTENT
        updated_category = category_repository.get_by_id(category_movie.id)

        assert updated_category.name == "Documentary"
        assert updated_category.description == "Description"
        assert updated_category.is_active is True

    def test_when_category_does_not_exist_then_return_404(self) -> None:
        url = f"/api/categories/{uuid4()}/"
        response = APIClient().put(
            url,
            data={
                "name": "Documentary",
                "description": "Documentary description",
                "is_active": True
            }
            )

        assert response.status_code == HTTP_404_NOT_FOUND

@pytest.mark.django_db
class TestDeleteAPI():
    def test_when_id_is_invalid_then_return_400(self) -> None:
        url = f"/api/categories/123523634/" #UUID invalid
        response = APIClient().delete(url)

        assert response.status_code == HTTP_400_BAD_REQUEST
    
    def test_when_category_does_not_exists_then_return_400(self) -> None:
        url = f"/api/categories/{uuid4()}/"
        response = APIClient().delete(url)

        assert response.status_code == HTTP_404_NOT_FOUND

    def test_when_category_does_exists_then_delete_category_and_return_204(
            self,
            category_movie: Category,
            category_repository: DjangoORMCategoryRepository
            ) -> None:
        
        category_repository.save(category_movie)

        url = f"/api/categories/{category_movie.id}/"
        response = APIClient().delete(url)

        assert response.status_code == HTTP_204_NO_CONTENT
        assert  category_repository.get_by_id(category_movie.id) is None
        assert category_repository.list() == []


