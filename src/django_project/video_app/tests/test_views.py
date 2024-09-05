import pytest 
from uuid import uuid4, UUID
from decimal import Decimal
from django.core.files.uploadedfile import SimpleUploadedFile
from src.django_project.video_app.repository import DjangoORMVideoRepository
from src.core.video.domain.video import Video
from src.core.video.domain.value_objects import Rating, AudioVideoMedia, MediaStatus
from rest_framework.status import HTTP_200_OK, HTTP_400_BAD_REQUEST, HTTP_404_NOT_FOUND, HTTP_201_CREATED, HTTP_204_NO_CONTENT
from rest_framework.test import APIClient

@pytest.mark.django_db
@pytest.mark.web_service
class TestListAPI:
    def test_list_videos(self):
        video_repository = DjangoORMVideoRepository()
        video_1 = Video(
            title="Sample Video1",
            description="A test video",
            launch_year=2022,
            duration=Decimal("120.5"),
            opened=False,
            rating=Rating.AGE_12,
            categories=set(),
            genres=set(),
            cast_members=set(),
        )

        video_2 = Video(
            title="Sample Video2",
            description="A test video description",
            launch_year=2020,
            duration=Decimal("100.5"),
            opened=False,
            rating=Rating.AGE_14,
            categories=set(),
            genres=set(),
            cast_members=set(),
        )

        video_repository.save(video_1) 
        video_repository.save(video_2) 
        url = "/api/videos/"
        response = APIClient().get(url)

        assert response.status_code == HTTP_200_OK
        assert response.data["data"]
        assert response.data["meta"]

        assert response.data["data"][0]["id"] == str(video_1.id)
        assert response.data["data"][0]["title"] == "Sample Video1"
        assert response.data["data"][0]["description"] == "A test video"
        assert response.data["data"][0]["launch_year"] == 2022
        assert response.data["data"][0]["duration"] == "120.50"
        assert response.data["data"][0]["rating"] == str(Rating.AGE_12)
        assert response.data["data"][0]["opened"] is False
        assert response.data["data"][0]["published"] is False
        assert response.data["data"][0]["categories"] == []
        assert response.data["data"][0]["genres"] == []
        assert response.data["data"][0]["cast_members"] == []

        assert response.data["data"][1]["id"] == str(video_2.id)
        assert response.data["data"][1]["title"] == "Sample Video2"
        assert response.data["data"][1]["description"] == "A test video description"
        assert response.data["data"][1]["launch_year"] == 2020
        assert response.data["data"][1]["duration"] == "100.50"
        assert response.data["data"][1]["rating"] == str(Rating.AGE_14)
        assert response.data["data"][1]["opened"] is False
        assert response.data["data"][1]["published"] is False
        assert response.data["data"][1]["categories"] == []
        assert response.data["data"][1]["genres"] == []
        assert response.data["data"][1]["cast_members"] == []

@pytest.mark.django_db
@pytest.mark.web_service
class TestRetrieveAPI():
    def test_when_id_is_invalid_return_400(self) -> None:
        url = f"/api/videos/159761298546/"
        response = APIClient().get(url)

        assert response.status_code == HTTP_400_BAD_REQUEST

    def test_return_video_when_exists(self):
        video_repository = DjangoORMVideoRepository()
        video = Video(
            title="Sample Video",
            description="A test video",
            launch_year=2022,
            duration=Decimal("120.5"),
            opened=False,
            rating=Rating.AGE_12,
            categories=set(),
            genres=set(),
            cast_members=set(),
        )
        video_repository.save(video) 

        url = f"/api/videos/{video.id}/"
        response = APIClient().get(url)

        assert response.status_code == HTTP_200_OK

        assert response.data["data"]["id"] == str(video.id)
        assert response.data["data"]["title"] == "Sample Video"
        assert response.data["data"]["description"] == "A test video"
        assert response.data["data"]["launch_year"] == 2022
        assert response.data["data"]["duration"] == "120.50"
        assert response.data["data"]["rating"] == str(Rating.AGE_12)
        assert response.data["data"]["opened"] is False
        assert response.data["data"]["published"] is False
        assert response.data["data"]["categories"] == []
        assert response.data["data"]["genres"] == []
        assert response.data["data"]["cast_members"] == []

    def test_return_404_when_not_exists(self):
        url = f"/api/videos/{uuid4()}/"
        response = APIClient().get(url)

        assert response.status_code == HTTP_404_NOT_FOUND

@pytest.mark.django_db
@pytest.mark.web_service
class TestDeleteAPI:
    def test_when_video_does_not_exist_then_raise_404(self):
        url = f"/api/videos/{uuid4()}/"
        response = APIClient().delete(url)
        assert response.status_code == HTTP_404_NOT_FOUND
    
    def test_when_pk_is_invalid_then_raise_400(self):
        url = f"/api/videos/9348561054612806/"
        response = APIClient().delete(url)
        assert response.status_code == HTTP_400_BAD_REQUEST
    
    def test_delete_video_from_repository(self):
        
        video_repository = DjangoORMVideoRepository()
        video = Video(
            title="Sample Video",
            description="A test video",
            launch_year=2022,
            duration=Decimal("120.5"),
            opened=False,
            rating=Rating.AGE_12,
            categories=set(),
            genres=set(),
            cast_members=set(),
        )
        video_repository.save(video) 
        url = f"/api/videos/{video.id}/"
        response = APIClient().delete(url) 
        assert response.status_code == HTTP_204_NO_CONTENT

@pytest.mark.django_db
@pytest.mark.web_service
class TestCreateAPI:
    def test_when_request_data_is_valid_then_create_video(self):

        url = "/api/videos/"
        data = {
            "title": "A sample video",
            "description": "video description",
            "launch_year": 2024,
            "duration": "120.50",
            "rating": "AGE_12",
            "categories": [],
            "genres": [],
            "cast_members": []
        }
        response = APIClient().post(url, data=data, format="json")

        assert response.status_code == HTTP_201_CREATED
        assert response.data["id"]

        repository = DjangoORMVideoRepository()
        saved_video = repository.get_by_id(response.data["id"])

        assert saved_video == Video(
            id=UUID(response.data["id"]),
            title="A sample video",
            description="video description",
            launch_year=2024,
            duration=Decimal("120.5"),
            opened=False,
            rating=Rating.AGE_12,
            categories=set(),
            genres=set(),
            cast_members=set(),
        )

@pytest.mark.django_db
@pytest.mark.web_service
class TestPartialUpdateVideoAPI:
    def test_when_send_video_and_update_partial_video(self):

        video_repository = DjangoORMVideoRepository()
        video = Video(
            title="Sample Video",
            description="A test video",
            launch_year=2022,
            duration=Decimal("120.5"),
            opened=False,
            rating=Rating.AGE_12,
            categories=set(),
            genres=set(),
            cast_members=set(),
        )

        video_repository.save(video) 

        url = f"/api/videos/{video.id}/"

        mp4_file = SimpleUploadedFile("test.mp4", b"fake_mp4_content", content_type="video/mp4")

        data = {"video_file": mp4_file}
        response = APIClient().patch(url, data=data, format="multipart")

        assert response.status_code == HTTP_200_OK
        
