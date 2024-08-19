import pytest
import unittest
from uuid import UUID, uuid4
from category import Category

class TestCategory:
    def test_name_is_required(self):
        with pytest.raises(TypeError):
            Category()
    
    def test_name_must_have_less_than_255_characters(self):
        with pytest.raises(ValueError, match="name cannot be longer than 255"):
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
        assert category.description == ""
        assert category.is_active is True
    
    def test_category_is_created_with_provided_values(self):
        id = uuid4()
        category = Category(id = id, name="Filme", description="Filmes em geral", is_active=False)
        assert category.id == id
        assert category.name == "Filme"
        assert category.description == "Filmes em geral"
        assert category.is_active is False
    
    def test_cannot_create_category_with_empty_name(self):
        with pytest.raises(ValueError, match="name cannot be empty"):
            Category(name="")

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
        with pytest.raises(ValueError, match="name cannot be longer than 255"):
            category.update_category(name="a"*256, description="Series em geral")
    
    def test_cannot_update_category_with_empty_name(self):
        category = Category(name="Filme", description="Filmes em geral")
        with pytest.raises(ValueError, match="name cannot be empty"):
            category.update_category(name="", description="Series em geral")

class TestActivate:
    def test_activate_inactive_category(self):
        category = Category(name="Filme", description="Filmes em geral", is_active=False)
        category.activate()

        assert category.is_active is True
    
    def test_activate_active_category(self):
        category = Category(name="Filme", description="Filmes em geral")
        category.activate()

        assert category.is_active is True

class TestDeactivate:
    def test_desactivate_inactive_category(self):
        category = Category(name="Filme", description="Filmes em geral", is_active=False)
        category.deactivate()

        assert category.is_active is False
    
    def test_activate_active_category(self):
        category = Category(name="Filme", description="Filmes em geral")
        category.deactivate()

        assert category.is_active is False

class TestEquality:
    def test_when_categories_have_name_id_they_are_equal(self):
        common_id = uuid4()
        category_1 = Category(id=common_id, name="Filme", description="Filmes em geral")
        category_2 = Category(id=common_id, name="Filme", description="Filmes em geral")

        assert category_1 == category_2
    def test_equality_different_classes(self):
        class Dummy: pass 

        common_id = uuid4()
        category = Category(id=common_id, name="Filme", description="Filmes em geral")

        dummy = Dummy()
        dummy.id = common_id

        assert category != dummy

