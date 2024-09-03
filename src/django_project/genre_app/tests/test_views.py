from rest_framework.status import HTTP_200_OK, HTTP_400_BAD_REQUEST, HTTP_404_NOT_FOUND, HTTP_201_CREATED, HTTP_204_NO_CONTENT
from rest_framework.test import APIClient
from src.django_project.category_app.repository import DjangoORMCategoryRepository
from src.django_project.genre_app.repository import DjangoORMGenreRepository
from src.core.category.domain.category import Category
from src.core.genre.domain.genre import Genre

import pytest 
from uuid import uuid4, UUID

@pytest.fixture
def category_movie():
    return Category(
        name= "Movie",
        description="Description"
    )

@pytest.fixture
def category_documentary():
    return Category(
        name= "Documentary",
        description="Description"
    )

@pytest.fixture
def category_repository(category_documentary, category_movie) -> DjangoORMCategoryRepository:
    repository = DjangoORMCategoryRepository()
    repository.save(category_documentary)
    repository.save(category_movie)
    return repository

@pytest.fixture
def genre_repository() -> DjangoORMGenreRepository:
    return DjangoORMGenreRepository()

@pytest.fixture
def genre_romance(category_documentary, category_movie) -> Genre:
    return Genre(
        name="Romance",
        is_active=True,
        categories={category_documentary.id, category_movie.id}
    )

@pytest.fixture
def genre_drama() -> Genre:
    return Genre(
        name="Drama",
        is_active=True,
        categories=set()
    )

@pytest.mark.django_db
@pytest.mark.web_service
class TestListAPI:
    def test_list_genre_and_categories(
            self,
            category_movie: Category,
            category_documentary: Category,
            category_repository: DjangoORMCategoryRepository,
            genre_romance: Genre,
            genre_drama: Genre,
            genre_repository: DjangoORMGenreRepository,
    ):
        genre_repository.save(genre_romance) 
        genre_repository.save(genre_drama) 
        url = "/api/genres/"
        response = APIClient().get(url)

        assert response.status_code == HTTP_200_OK
        assert response.data["data"]
        assert response.data["meta"]

        assert response.data["data"][0]["id"] == str(genre_romance.id)
        assert response.data["data"][0]["name"] == "Romance"
        assert response.data["data"][0]["is_active"] is True
        assert set(response.data["data"][0]["categories"]) == {
            str(category_documentary.id),
            str(category_movie.id),
        }


        assert response.data["data"][1]["id"] == str(genre_drama.id)
        assert response.data["data"][1]["name"] == "Drama"
        assert response.data["data"][1]["is_active"] is True
        assert response.data["data"][1]["categories"] == []

@pytest.mark.django_db
@pytest.mark.web_service
class TestRetrieveAPI():
    def test_when_id_is_invalid_return_400(self) -> None:
        url = f"/api/genres/159761298546/"
        response = APIClient().get(url)

        assert response.status_code == HTTP_400_BAD_REQUEST

    def test_return_genre_when_exists(
            self, 
            category_movie: Category,
            category_documentary: Category,
            category_repository: DjangoORMCategoryRepository,
            genre_romance: Genre,
            genre_drama: Genre,
            genre_repository: DjangoORMGenreRepository,
            ):
        genre_repository.save(genre_romance) 
        genre_repository.save(genre_drama) 

        url = f"/api/categories/{genre_drama.id}/"
        response = APIClient().get(url)

        expected_data = {
            "data": {
                "id": str(genre_drama.id),
                "name": genre_drama.name,
                "is_active": genre_drama.is_active,
                "categories": genre_drama.categories
            }
            
        }
        #assert response.status_code == HTTP_200_OK
        #assert response.data == expected_data

    def test_return_404_when_not_exists(self):
        url = f"/api/genres/{uuid4()}/"
        response = APIClient().get(url)

        assert response.status_code == HTTP_404_NOT_FOUND

@pytest.mark.django_db
@pytest.mark.web_service
class TestCreateAPI:
    def test_when_request_data_is_valid_then_create_genre(
            self,
            genre_romance,
            genre_drama,
            genre_repository: DjangoORMGenreRepository,
            category_repository,
            category_documentary,
            category_movie
    ):

        url = "/api/genres/"
        data = {
            "name": "Romance",
            "is_active": True,
            "categories": [
                str(category_movie.id)

            ]
        }
        response = APIClient().post(url, data=data, format="json")

        assert response.status_code == HTTP_201_CREATED
        assert response.data["id"]

        saved_genre = genre_repository.get_by_id(response.data["id"])

        assert saved_genre == Genre(
            id=UUID(response.data["id"]),
            name="Romance",
            is_active=True,
            categories={category_movie.id},
        )

@pytest.mark.django_db
@pytest.mark.web_service
class TestUpdateAPI:
    def test_when_request_data_is_valid_then_update_genre(
        self,
        category_repository: DjangoORMCategoryRepository,
        category_movie: Category,
        category_documentary: Category,
        genre_repository: DjangoORMGenreRepository,
        genre_romance: Genre,
    ) -> None:
        genre_repository.save(genre_romance)

        url = f"/api/genres/{str(genre_romance.id)}/"
        data = {
            "name": "Drama",
            "is_active": True,
            "categories": [category_documentary.id],
        }
        response = APIClient().put(url, data=data)

        assert response.status_code == HTTP_204_NO_CONTENT
        updated_genre = genre_repository.get_by_id(genre_romance.id)
        assert updated_genre.name == "Drama"
        assert updated_genre.is_active is True
        assert updated_genre.categories == {category_documentary.id}

    def test_when_request_data_is_invalid_then_return_400(
        self,
        genre_drama: Genre,
    ) -> None:
        url = f"/api/genres/{str(genre_drama.id)}/"
        data = {
            "name": "",
            "is_active": True,
            "categories": [],
        }
        response = APIClient().put(url, data=data)

        assert response.status_code == HTTP_400_BAD_REQUEST
        assert response.data == {"name": ["This field may not be blank."]}

    def test_when_related_categories_do_not_exist_then_return_400(
        self,
        category_repository: DjangoORMCategoryRepository,
        category_movie: Category,
        category_documentary: Category,
        genre_repository: DjangoORMGenreRepository,
        genre_romance: Genre,
    ) -> None:
        genre_repository.save(genre_romance)

        url = f"/api/genres/{str(genre_romance.id)}/"
        data = {
            "name": "Romance",
            "is_active": True,
            "categories": [uuid4()],  # non-existent category
        }
        response = APIClient().put(url, data=data)

        assert response.status_code == HTTP_400_BAD_REQUEST
        assert "Categories with provided IDs not found" in response.data["error"]

    def test_when_genre_does_not_exist_then_return_404(self) -> None:
        url = f"/api/genres/{str(uuid4())}/"
        data = {
            "name": "Romance",
            "is_active": True,
            "categories": [],
        }
        response = APIClient().put(url, data=data)

        assert response.status_code == HTTP_404_NOT_FOUND

@pytest.mark.django_db
@pytest.mark.web_service
class TestDeleteAPI:
    def test_when_genre_does_not_exist_then_raise_404(self):
        url = f"/api/genres/{uuid4()}/"
        response = APIClient().delete(url)
        assert response.status_code == HTTP_404_NOT_FOUND
    
    def test_when_pk_is_invalid_then_raise_400(self):
        url = f"/api/genres/9348561054612806/"
        response = APIClient().delete(url)
        assert response.status_code == HTTP_400_BAD_REQUEST
    
    def test_delete_genre_from_repository(
            self,
            genre_repository: DjangoORMGenreRepository,
            genre_drama: Genre,):
        
        genre_repository.save(genre_drama)
        url = f"/api/genres/{genre_drama.id}/"
        response = APIClient().delete(url) 
        assert response.status_code == HTTP_204_NO_CONTENT
