import pytest 
from decimal import Decimal
from uuid import uuid4, UUID
from src.core.category.domain.category import Category
from src.core.genre.application.use_cases.create_genre import CreateGenre
from src.core.genre.domain.genre_repository import GenreRepository
from src.core.category.domain.category_repository import CategoryRepository
from src.core.cast_member.domain.cast_member_repository import CastMemberRepository
from src.core.cast_member.domain.cast_member import CastMember, CastMemberType
from src.core.video.domain.value_objects import Rating

from src.core.video.domain.video_repository import VideoRepository
from src.core.video.domain.video import Video

from src.core.video.application.use_cases.create_video_without_media import CreateVideoWithoutMedia


from src.core.video.application.use_cases.exceptions import RelatedEntitiesNotFound, InvalidVideo
from src.core.genre.domain.genre import Genre
from unittest.mock import create_autospec


@pytest.fixture
def movie_category() -> Category:
    return Category(name="Movie")

@pytest.fixture
def documentary_category() -> Category:
    return Category(name="Documentary")


@pytest.fixture
def mock_category_repository(movie_category, documentary_category) -> CategoryRepository:
    repository = create_autospec(CategoryRepository)
    repository.list.return_value = [movie_category, documentary_category]
    return repository


@pytest.fixture
def action_genre() -> Genre:
    return Genre(name="Action")

@pytest.fixture
def romance_genre() -> Genre:
    return Genre(name="Romance")

@pytest.fixture
def mock_genre_repository(romance_genre, action_genre) -> GenreRepository:
    repository = create_autospec(GenreRepository)
    repository.list.return_value = [romance_genre, action_genre]
    return repository

@pytest.fixture
def director_cast_member() -> Genre:
    return CastMember(name="John Krasinski",type=CastMemberType.DIRECTOR)

@pytest.fixture
def actor_cast_member() -> Genre:
    return CastMember(name="John Doe",type=CastMemberType.ACTOR)

@pytest.fixture
def mock_cast_member_repository(actor_cast_member, director_cast_member) -> CastMemberRepository:
    repository = create_autospec(CastMemberRepository)
    repository.list.return_value = [actor_cast_member, director_cast_member]
    return repository

@pytest.fixture
def mock_video_repository() -> VideoRepository:
    return create_autospec(VideoRepository)

@pytest.mark.video
class TestCreateVideoWithoutMedia:
    def test_create_video_without_media_with_not_found_related_entities_should_error(
            self, 
            mock_video_repository, 
            mock_category_repository, 
            movie_category, 
            documentary_category,
            mock_genre_repository,
            romance_genre,
            action_genre,
            mock_cast_member_repository,
            actor_cast_member, 
            director_cast_member

            ):
        
        use_case = CreateVideoWithoutMedia(
            repository=mock_video_repository,
            category_repository=mock_category_repository,
            genre_repository=mock_genre_repository,
            cast_member_repository=mock_cast_member_repository
        )
        
        category_id = uuid4()
        genre_id = uuid4()
        cast_member_id = uuid4()

        input = CreateVideoWithoutMedia.Input(
            title="Sample Video",
            description="A test video",
            launch_year=2022,
            duration=Decimal("120.5"),
            rating=Rating.AGE_12,
            categories={category_id},
            genres={genre_id},
            cast_members={cast_member_id},
        )
        with pytest.raises(RelatedEntitiesNotFound) as exc_info:
            use_case.execute(input)
        
        assert str(category_id) in str(exc_info.value)
        assert str(genre_id) in str(exc_info.value)
        assert str(cast_member_id) in str(exc_info.value)

    def test_create_video_without_media_with_related_entities_and_invalid_values(
            self, 
            mock_video_repository, 
            mock_category_repository, 
            movie_category, 
            documentary_category,
            mock_genre_repository,
            romance_genre,
            action_genre,
            mock_cast_member_repository,
            actor_cast_member, 
            director_cast_member

            ):
        
        use_case = CreateVideoWithoutMedia(
            repository=mock_video_repository,
            category_repository=mock_category_repository,
            genre_repository=mock_genre_repository,
            cast_member_repository=mock_cast_member_repository
        )
        input = CreateVideoWithoutMedia.Input(
            title="",
            description="A test video",
            launch_year=2022,
            duration=Decimal("120.5"),
            rating=Rating.AGE_12,
            categories={movie_category.id},
            genres={action_genre.id},
            cast_members={actor_cast_member.id, director_cast_member.id},
        )

        with pytest.raises(InvalidVideo, match="title cannot be empty") as exc_info:
            use_case.execute(input)
        
    
    def test_create_video_without_media_with_provided_values(
            self, 
            mock_video_repository, 
            mock_category_repository, 
            movie_category, 
            documentary_category,
            mock_genre_repository,
            romance_genre,
            action_genre,
            mock_cast_member_repository,
            actor_cast_member, 
            director_cast_member

            ):
        
        use_case = CreateVideoWithoutMedia(
            repository=mock_video_repository,
            category_repository=mock_category_repository,
            genre_repository=mock_genre_repository,
            cast_member_repository=mock_cast_member_repository
        )
        input = CreateVideoWithoutMedia.Input(
            title="Sample Video",
            description="A test video",
            launch_year=2022,
            duration=Decimal("120.5"),
            rating=Rating.AGE_12,
            categories={movie_category.id},
            genres={action_genre.id},
            cast_members={actor_cast_member.id, director_cast_member.id},
        )
        output = use_case.execute(input=input)

        assert isinstance(output.id, UUID)
        mock_video_repository.save.assert_called_once_with(
            Video(
                id=output.id,
                title="Sample Video",
                description="A test video",
                launch_year=2022,
                duration=Decimal("120.5"),
                published=False,
                rating=Rating.AGE_12,
                categories={movie_category.id},
                genres={action_genre.id},
                cast_members={actor_cast_member.id, director_cast_member.id},
            )
        )