import pytest 

from rest_framework.test import APIClient

@pytest.mark.django_db
class TestCreateAndEditCategory:
    def test_user_can_create_and_edit_category(self) -> None:
        api_client = APIClient()

        #Verify empty database
        list_response = api_client.get("/api/categories/")
        assert list_response.data == {"data": []}

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
        assert list_response.data == {"data": [
            {   
                "id": created_category_id,
                "name": "Movie", 
                "description": "Movie Description",
                "is_active": True
            }
        ]}

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
        assert list_response.data == {"data": [
            {   
                "id": created_category_id,
                "name": "Documentary", 
                "description": "Documentary Description",
                "is_active": False
            }
        ]}
    
    def test_user_can_create_and_delete_category(self) -> None:
        api_client = APIClient()

        #Verify empty database
        list_response = api_client.get("/api/categories/")
        assert list_response.data == {"data": []}

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
        assert list_response.data == {"data": [
            {   
                "id": created_category_id,
                "name": "Movie", 
                "description": "Movie Description",
                "is_active": True
            }
        ]}

        #Update created item
        delete_response = api_client.delete(f"/api/categories/{created_category_id}/",)
        assert delete_response.status_code == 204

        #Verify created item
        list_response = api_client.get("/api/categories/")
        assert list_response.data == {"data": []}