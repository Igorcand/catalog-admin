import pytest 
from uuid import uuid4
from decimal import Decimal
from src.core.video.domain.video import Video
from src.core.video.domain.value_objects import Rating, AudioVideoMedia, MediaStatus

from src.django_project.video_app.repository import DjangoORMVideoRepository
from src.django_project.category_app.repository import DjangoORMCategoryRepository
from src.django_project.genre_app.repository import DjangoORMGenreRepository
from src.django_project.cast_member_app.repository import DjangoORMCastMemberRepository

from src.core.category.domain.category import Category
from src.core.genre.domain.genre import Genre
from src.core.cast_member.domain.cast_member import CastMember, CastMemberType


from src.django_project.video_app.models import Video as VideoORM
from src.django_project.video_app.models import AudioVideoMedia as AudioVideoMediaORM

@pytest.fixture
def movie_category() -> Category:
    return Category(name="Movie")

@pytest.fixture
def actor_cast_member():
    return CastMember(
        name="John Doe",
        type=CastMemberType.ACTOR,
    )


@pytest.fixture
def action_genre() -> Genre:
    return Genre(name="Action")


@pytest.fixture
def video(movie_category, action_genre, actor_cast_member) -> Video:
    return Video(
        title="Sample Video",
        description="A test video",
        launch_year=2022,
        duration=Decimal("120.5"),
        opened=False,
        rating=Rating.AGE_12,
        categories={movie_category.id},
        genres={action_genre.id},
        cast_members={actor_cast_member.id},
    )


@pytest.mark.django_db
@pytest.mark.web_service
class TestSaveVideo:
    def test_saves_video_in_database_without_related_entities(
            self, 
            ):

        video = Video(
            title="Sample Video",
            description="A test video",
            launch_year=2022,
            duration=Decimal("120.5"),
            opened=False,
            rating=Rating.AGE_12,
            categories=set(),
            genres=set(),
            cast_members=set(),
        )
        video_repository = DjangoORMVideoRepository() 


        assert VideoORM.objects.count() == 0
        video_repository.save(video)

        assert VideoORM.objects.count() == 1

        video_model = video_repository.get_by_id(id=video.id)
        assert video_model.id           == video.id
        assert video_model.title        == video.title
        assert video_model.description  == video.description
        assert video_model.launch_year  == video.launch_year
        assert video_model.duration     == video.duration
        assert Rating(video_model.rating)       == Rating.AGE_12
        assert video_model.opened       == video.opened
        assert video_model.published    == video.published
        
    def test_saves_video_in_database_with_related_entities(
            self, 
            video,
            movie_category, 
            action_genre, 
            actor_cast_member
            ):
        category_repository = DjangoORMCategoryRepository() 
        category_repository.save(movie_category)

        genre_repository = DjangoORMGenreRepository() 
        genre_repository.save(action_genre)

        cast_member_repository = DjangoORMCastMemberRepository() 
        cast_member_repository.save(actor_cast_member)

        video_repository = DjangoORMVideoRepository() 


        assert VideoORM.objects.count() == 0
        video_repository.save(video)

        assert VideoORM.objects.count() == 1

        video_model = VideoORM.objects.get(id=video.id)
        assert video_model.id           == video.id
        assert video_model.title        == video.title
        assert video_model.description  == video.description
        assert video_model.launch_year  == video.launch_year
        assert video_model.duration     == video.duration
        assert Rating(video_model.rating)       == Rating.AGE_12
        assert video_model.opened       == video.opened
        assert video_model.published    == video.published
        
        related_category = video_model.categories.get()
        related_genres = video_model.genres.get()
        related_cast_members = video_model.cast_members.get()

        assert movie_category.id == related_category.id
        assert action_genre.id == related_genres.id
        assert actor_cast_member.id == related_cast_members.id

@pytest.mark.django_db
@pytest.mark.web_service
class TestGetGenre:
    def test_get_video_does_not_exists_should_return_none(self):
        video_repository = DjangoORMVideoRepository()  

        assert VideoORM.objects.count() == 0

        genre = video_repository.get_by_id(id=uuid4())
        assert genre is None
        assert VideoORM.objects.count() == 0
    
    def test_get_video_existing_should_return_success(self):
        video = Video(
            title="Sample Video",
            description="A test video",
            launch_year=2022,
            duration=Decimal("120.5"),
            opened=False,
            rating=Rating.AGE_12,
            categories=set(),
            genres=set(),
            cast_members=set(),
        )
        video_repository = DjangoORMVideoRepository() 

        assert VideoORM.objects.count() == 0
        video_repository.save(video)
        assert VideoORM.objects.count() == 1

        video_model = VideoORM.objects.get(id=video.id)
        assert video_model.id             == video.id
        assert video_model.title          == video.title
        assert video_model.description    == video.description
        assert video_model.launch_year    == video.launch_year
        assert video_model.duration       == video.duration
        assert Rating(video_model.rating) == Rating.AGE_12
        assert video_model.opened         == video.opened
        assert video_model.published      == video.published
 
@pytest.mark.django_db
@pytest.mark.web_service
class TestDeleteVideo:
    def test_delete_video_does_not_exists_should_return_none(self):
        video_repository = DjangoORMVideoRepository() 

        assert VideoORM.objects.count() == 0

        video_repository.delete(id=uuid4())

        assert VideoORM.objects.count() == 0
    
    def test_delete_genre_existing_should_return_success(self):
        video = Video(
            title="Sample Video",
            description="A test video",
            launch_year=2022,
            duration=Decimal("120.5"),
            opened=False,
            rating=Rating.AGE_12,
            categories=set(),
            genres=set(),
            cast_members=set(),
        )
        video_repository = DjangoORMVideoRepository() 

        assert VideoORM.objects.count() == 0
        video_repository.save(video)
        assert VideoORM.objects.count() == 1
        video_repository.delete(id=video.id)
        assert VideoORM.objects.count() == 0

@pytest.mark.django_db
@pytest.mark.web_service
class TestUpdateVideoWithMedia:    
    def test_update_genre_existing_should_return_success(self):
        video = Video(
            title="Sample Video",
            description="A test video",
            launch_year=2022,
            duration=Decimal("120.5"),
            opened=False,
            rating=Rating.AGE_12,
            categories=set(),
            genres=set(),
            cast_members=set(),
        )
        video_repository = DjangoORMVideoRepository() 

        assert VideoORM.objects.count() == 0
        video_repository.save(video)

        assert VideoORM.objects.count() == 1

        video_model = VideoORM.objects.get(id=video.id)

        assert video_model.id           == video.id
        assert video_model.title        == video.title
        assert video_model.description  == video.description
        assert video_model.launch_year  == video.launch_year
        assert video_model.duration     == video.duration
        assert Rating(video_model.rating)       == Rating.AGE_12
        assert video_model.opened       == video.opened
        assert video_model.published    == video.published

        update_video = Video(
            id = video.id,
            title="Sample Video updated",
            description="A test video",
            launch_year=int(2023),
            duration=Decimal("120.5"),
            opened=False,
            rating=Rating.AGE_14,
            categories=set(),
            genres=set(),
            cast_members=set(),
            video = AudioVideoMedia("trailer.mp4", "raw_path", "encoded_path", MediaStatus.COMPLETED),
        )
        video_repository.update(update_video)

        genre_model_uptaded = VideoORM.objects.get(id=update_video.id)
        assert genre_model_uptaded.id == video.id
        assert genre_model_uptaded.title == "Sample Video updated"
        assert genre_model_uptaded.launch_year == 2023
        assert Rating(genre_model_uptaded.rating) == Rating.AGE_14
        
@pytest.mark.django_db
@pytest.mark.web_service
class TestGetVideo:    
    def test_get_video_existing_should_return_success(self):
        video = Video(
            title="Sample Video",
            description="A test video",
            launch_year=2022,
            duration=Decimal("120.5"),
            opened=False,
            rating=Rating.AGE_12,
            categories=set(),
            genres=set(),
            cast_members=set(),
        )
        video_repository = DjangoORMVideoRepository() 

        assert VideoORM.objects.count() == 0
        video_repository.save(video)
        assert VideoORM.objects.count() == 1

        video_model = VideoORM.objects.get(id=video.id)
        assert video_model.id           == video.id
        assert video_model.title        == video.title
        assert video_model.description  == video.description
        assert video_model.launch_year  == video.launch_year
        assert video_model.duration     == video.duration
        assert Rating(video_model.rating)       == Rating.AGE_12
        assert video_model.opened       == video.opened
        assert video_model.published    == video.published

