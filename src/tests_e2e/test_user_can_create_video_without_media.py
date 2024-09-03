import pytest 

from rest_framework.test import APIClient

@pytest.mark.django_db
@pytest.mark.e2e
class TestCreateVIdeoWithoutMedia:
    def test_user_can_video_without_media_and_with_no_related_entities(self) -> None:
        api_client = APIClient()

        #create item
        create_response = api_client.post(
            "/api/videos/",
            data={
                "title": "A samble video",
                "description": "video description",
                "launch_year": 2024,
                "duration": 120.5,
                "rating": "AGE 12",
                "categories": [],
                "genres": [],
                "cast_members": []
            }, 
            format="json"
            )

        assert create_response.status_code == 201
    
    def test_user_can_video_without_media_and_with_related_entities_existing(self) -> None:
        api_client = APIClient()

        create_response = api_client.post(
            "/api/categories/",
            data={"name": "Movie", "description": "Movie Description"}, 
            format="json"
            )

        assert create_response.status_code == 201
        created_category_id = create_response.data["id"]


        create_response = api_client.post(
            "/api/genres/",
            data={"name": "Movie", "is_active": True, "categories": [created_category_id]}, 
            format="json"
            )

        assert create_response.status_code == 201
        created_genre_id = create_response.data["id"]

        create_response = api_client.post(
            "/api/cast_members/",
            data={"name": "John", "type": "ACTOR"}, 
            format="json"
            )

        assert create_response.status_code == 201
        created_cast_member_id = create_response.data["id"]

        #create item
        create_response = api_client.post(
            "/api/videos/",
            data={
                "title": "A samble video",
                "description": "video description",
                "launch_year": 2024,
                "duration": 120.5,
                "rating": "AGE 12",
                "categories": [created_category_id],
                "genres": [created_genre_id],
                "cast_members": [created_cast_member_id]
            }, 
            format="json"
            )

        assert create_response.status_code == 201
        