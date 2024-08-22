from django.test import TestCase
from rest_framework.test import APITestCase
from django_project.category_app.repository import DjangoORMCategoryRepository
from src.core.category.domain.category import Category

class TestCategoryAPI(APITestCase):
    def test_list_categories(self):
        category = Category(
            name= "Movie",
            description="Description"
        )
        repository = DjangoORMCategoryRepository()
        repository.save(category)

        url = "/api/categories/"
        response = self.client.get(url)

        expected_data = [
            {
                "id": str(category.id),
                "name": category.name,
                "description": category.description,
                "is_active": category.is_active,
            }
        ]
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data, expected_data)

        
