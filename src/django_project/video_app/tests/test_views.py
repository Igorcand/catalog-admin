import pytest 
from uuid import uuid4
from decimal import Decimal
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



