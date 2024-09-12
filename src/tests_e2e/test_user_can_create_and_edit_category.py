import pytest 
from rest_framework.test import APIClient
from src.django_project.category_app.views import CategoryViewSet
from unittest.mock import patch

@pytest.mark.django_db
@pytest.mark.e2e
class TestCreateAndEditCategory:
    @patch.object(CategoryViewSet, "permission_classes", [])
    def test_user_can_create_and_edit_category(self) -> None:
        api_client = APIClient()

        #Verify empty database
        list_response = api_client.get("/api/categories/")
        assert list_response.status_code == 200
        assert list_response.data == {
            "data": [],
            "meta": {
               "current_page": 1,
                "per_page": 2,
                "total": 0 
            }
            }

        #create item
        create_response = api_client.post(
            "/api/categories/",
            data={"name": "Movie", "description": "Movie Description"}, 
            format="json"
            )

        assert create_response.status_code == 201
        created_category_id = create_response.data["id"]

        #Verify created item
        list_response = api_client.get("/api/categories/")
        assert list_response.data == {
            "data": [
                {   
                    "id": created_category_id,
                    "name": "Movie", 
                    "description": "Movie Description",
                    "is_active": True
                }
            ],
            "meta": {
               "current_page": 1,
                "per_page": 2,
                "total": 1 
            }
        }

        #Update created item
        update_response = api_client.put(f"/api/categories/{created_category_id}/",
                data = {   
                "name": "Documentary", 
                "description": "Documentary Description",
                "is_active": False
            }, format="json"
            )


        assert update_response.status_code == 204

        #Verify created item
        list_response = api_client.get("/api/categories/")
        assert list_response.data == {
            "data": [
                {   
                    "id": created_category_id,
                    "name": "Documentary", 
                    "description": "Documentary Description",
                    "is_active": False
                }
            ],
            "meta": {
               "current_page": 1,
                "per_page": 2,
                "total": 1 
            }
        }
    
    @patch.object(CategoryViewSet, "permission_classes", [])
    def test_user_can_create_and_delete_category(self) -> None:
        api_client = APIClient()

        #Verify empty database
        list_response = api_client.get("/api/categories/")
        assert list_response.data == {
            "data": [],
            "meta": {
               "current_page": 1,
                "per_page": 2,
                "total": 0 
            }
            }

        #create item
        create_response = api_client.post(
            "/api/categories/",
            data={"name": "Movie", "description": "Movie Description"}, 
            format="json"
            )

        assert create_response.status_code == 201
        created_category_id = create_response.data["id"]

        #Verify created item
        list_response = api_client.get("/api/categories/")
        assert list_response.data == {
            "data": [
                {   
                    "id": created_category_id,
                    "name": "Movie", 
                    "description": "Movie Description",
                    "is_active": True
                }
            ],
            "meta": {
               "current_page": 1,
                "per_page": 2,
                "total": 1 
            }
        }

        #Update created item
        delete_response = api_client.delete(f"/api/categories/{created_category_id}/",)
        assert delete_response.status_code == 204

        #Verify created item
        list_response = api_client.get("/api/categories/")
        assert list_response.data == {
            "data": [],
            "meta": {
               "current_page": 1,
                "per_page": 2,
                "total": 0 
            }
        }