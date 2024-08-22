from django.test import TestCase
from rest_framework.test import APITestCase

class TestCategoryAPI(APITestCase):
    def test_list_categories(self):
        url = "/api/categories/"
        response = self.client.get(url)

        expected_data = [
            {
                "id": "235387631586",
                "name": "Movie",
                "description": "Description",
                "is_active": True
            }
        ]
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data, expected_data)

        
