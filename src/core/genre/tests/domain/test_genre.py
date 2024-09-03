import pytest
from uuid import UUID, uuid4
from src.core.genre.domain.genre import Genre

@pytest.mark.genre
class TestGenre:
    def test_name_is_required(self):
        with pytest.raises(TypeError):
            Genre()
    
    def test_name_must_have_less_than_255_characters(self):
        with pytest.raises(ValueError, match="name cannot be longer than 255"):
            Genre(name="a"*256)

    def test_cannot_create_genre_with_empty_name(self):
        with pytest.raises(ValueError, match="name cannot be empty"):
            Genre(name="")
    
    def test_create_genre_with_default_values(self):
        genre = Genre(name="Romance")
        assert isinstance(genre.id, UUID)
        assert genre.is_active is True
        assert genre.name == "Romance"
        assert genre.categories == set()

    
    def test_genre_is_created_with_provided_values(self):
        id = uuid4()
        categories=[uuid4(), uuid4()]
        genre = Genre(
            id=id, 
            name="Romance", 
            is_active=False, 
            categories=categories
            )
        
        assert genre.id == id
        assert genre.name == "Romance"
        assert genre.categories == categories
        assert genre.is_active is False
    

    def test_genre_str_default_attribute(self):
        genre = Genre(name="Romance")
        assert str(genre) == "Romance - (True)"
    
    def test_genre_repr_default_attribute(self):
        id = uuid4()
        genre = Genre(id=id, name="Romance")
        assert repr(genre) == f"Genre Romance ({id})"

@pytest.mark.genre
class TestActivate:
    def test_activate_inactive_genre(self):
        genre = Genre(
            name="Romance", 
            is_active=False
            )
        genre.activate()

        assert genre.is_active is True
    
    def test_activate_active_genre(self):
        genre = Genre(
            name="Romance", 
            is_active=False
            )
        genre.activate()

        assert genre.is_active is True

@pytest.mark.genre
class TestDeactivate:
    def test_desactivate_inactive_genre(self):
        genre = Genre(
            name="Romance", 
            is_active=False
            )
        genre.deactivate()

        assert genre.is_active is False
    
    def test_deactivate_active_genre(self):
        genre = Genre(
            name="Romance", 
            is_active=False
            )
        genre.deactivate()

        assert genre.is_active is False

@pytest.mark.genre
class TestChangeName():
    def test_change_name(self):
        genre = Genre(name="Romance")
        genre.change_name("Terror")
        assert genre.name == "Terror"
    
    def test_when_name_is_empty(self):
        genre = Genre(name="Romance")
        with pytest.raises(ValueError, match="name cannot be empty"):
            genre.change_name("")

@pytest.mark.genre
class TestAddCategory:
    def test_add_category_to_genre(self):
        genre = Genre(name="Romance")
        category_id = uuid4()
        assert category_id not in genre.categories

        genre.add_category(category_id)
        assert category_id in genre.categories

@pytest.mark.genre
class TestRemoveCategory:
    def test_remove_category_to_genre(self):
        category_id = uuid4()
        genre = Genre(name="Romance", categories={category_id})
        assert category_id in genre.categories

        genre.remove_category(category_id)
        assert category_id not in genre.categories
        assert genre.categories == set()

@pytest.mark.genre
class TestEquality:
    def test_when_categories_have_name_id_they_are_equal(self):
        common_id = uuid4()
        genre_1 = Genre(
            id=common_id,
            name="Romance", 
            is_active=False
            )
        genre_2 = Genre(
            id=common_id,
            name="Romance", 
            is_active=False
            )

        assert genre_1 == genre_2

    def test_equality_different_classes(self):
        class Dummy: pass 

        common_id = uuid4()
        genre_1 = Genre(
            id=common_id,
            name="Romance", 
            is_active=False
            )

        dummy = Dummy()
        dummy.id = common_id

        assert genre_1 != dummy

