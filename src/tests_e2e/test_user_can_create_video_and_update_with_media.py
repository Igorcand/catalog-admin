import pytest 
from rest_framework.test import APIClient
from django.core.files.uploadedfile import SimpleUploadedFile

@pytest.mark.django_db
@pytest.mark.e2e
class TestCreateVIdeoWithoutMediaAndUpdate:
    def test_user_can_video_without_media_and_with_no_related_entities_and_update_with_media(self) -> None:
        api_client = APIClient()

        #create item
        create_response = api_client.post(
            "/api/videos/",
            data={
                "title": "A samble video",
                "description": "video description",
                "launch_year": 2024,
                "duration": 120.5,
                "rating": "AGE_12",
                "categories": [],
                "genres": [],
                "cast_members": []
            }, 
            format="json"
            )

        assert create_response.status_code == 201
        created_video_id = create_response.data["id"]

        url = f"/api/videos/{created_video_id}/"

        mp4_file = SimpleUploadedFile("test.mp4", b"fake_mp4_content", content_type="video/mp4")

        data = {"video_file": mp4_file,  'media_type': "VIDEO"}
        response = api_client.patch(url, data=data, format="multipart")

        assert response.status_code == 200