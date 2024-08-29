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
        print(f'response.data["data"] = {response.data["data"]}')

        assert response.status_code == HTTP_200_OK
        assert response.data["data"]

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




