import pytest
import unittest
from uuid import UUID, uuid4
from category import Category

class TestCategory:
    def test_name_is_required(self):
        with pytest.raises(TypeError):
            Category()
    
    def test_name_must_have_less_than_255_characters(self):
        with pytest.raises(ValueError, match="name must have less than 256 characteres"):
            Category(name="a"*256)
    
    def test_category_must_be_created_with_id_as_uuid_by_default(self):
        category = Category(name="Filme")
        assert isinstance(category.id, UUID)
    
    def test_category_is_created_as_active_by_default(self):
        category = Category(name="Filme")
        assert category.is_active is True
    
    def test_cretaed_category_with_defult_values(self):
        category = Category(name="Filme")
        assert category.name == "Filme"
        assert category.desciption == ""
        assert category.is_active is True
    
    def test_category_is_created_with_provided_values(self):
        id = uuid4()
        category = Category(id = id, name="Filme", description="Filmes em geral", is_active=False)
        assert category.id == id
        assert category.name == "Filme"
        assert category.desciption == "Filmes em geral"
        assert category.is_active is False

    def test_category_str_default_attribute(self):
        category = Category(name="Filme")
        assert str(category) == "Filme -  (True)"
    
    def test_category_repr_default_attribute(self):
        id = uuid4()
        category = Category(id=id, name="Filme")
        assert repr(category) == f"Category Filme ({id})"

class TestUpdateCategory:
    def test_update_category_with_name_and_description(self):
        category = Category(name="Filme", description="Filmes em geral")
        category.update_category(name="Serie", description="Series em geral")

        assert category.name == "Serie"
        assert category.description == "Series em geral"

    def test_update_category_with_invalid_name_raise_exception(self):
        category = Category(name="Filme", description="Filmes em geral")
        with pytest.raises(ValueError, match="name must have less than 256 characteres"):
            category.update_category(name="a"*256, description="Series em geral")

