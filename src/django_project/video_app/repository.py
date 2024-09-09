from uuid import UUID
from django.db import transaction
from src.core.video.domain.video_repository import VideoRepository
from src.core.video.domain.video import Video
from src.core.video.domain.value_objects import Rating
from src.django_project.video_app.models import Video as VideoORM
from src.django_project.video_app.models import AudioVideoMedia as AudioVideoMediaORM

class DjangoORMVideoRepository(VideoRepository):
    def __init__(self, model: VideoORM | None = None):
            self.model = model or VideoORM

    def save(self, video: Video):
        with transaction.atomic():
            VideoModelMapper.to_model(video)

    def get_by_id(self, id: UUID) -> Video | None:
        try:
            video_model = self.model.objects.get(id=id)
            return VideoModelMapper.to_entity(video_model)
        except VideoORM.DoesNotExist:
            return None


    def delete(self, id: UUID) -> None:
        VideoORM.objects.filter(id=id).delete()

    def update(self, video: Video) -> None:
        try:
            video_model = VideoORM.objects.get(id=video.id)
        except VideoORM.DoesNotExist:
            return None
        else:
            with transaction.atomic():
                AudioVideoMediaORM.objects.filter(id=video.id).delete()

                video_model.categories.set(video.categories)
                video_model.genres.set(video.genres)
                video_model.cast_members.set(video.cast_members)

                video_model.video = AudioVideoMediaORM.objects.create(
                    name = video.video.name,
                    raw_location = video.video.raw_location,
                    encoded_location = video.video.encoded_location,
                    status = video.video.status,
                    media_type = video.video.media_type
                )

                VideoORM.objects.filter(id=video.id).update(
                    title       = video.title,
                    description = video.description,
                    launch_year = video.launch_year,
                    opened      = video.opened,
                    duration    = video.duration,
                    rating      = video.rating.name,
                )
        
    
    def list(self) -> list[Video]:
        return [
            VideoModelMapper.to_entity(video_model)
         for video_model in VideoORM.objects.all()]

class VideoModelMapper:
    @staticmethod
    def to_model(video: Video) -> VideoORM:
        print(f'to_model -> video.rating = {video.rating} -- type = {type(video.rating)}')
        video_model = VideoORM.objects.create(
            id=video.id,
            title=video.title,
            description=video.description,
            launch_year=video.launch_year,
            duration=video.duration,
            rating=video.rating.name,
            opened=False,
            published=video.published,
        )

        video_model.categories.set(video.categories)
        video_model.genres.set(video.genres)
        video_model.cast_members.set(video.cast_members)
        
        return video_model
    
    def to_entity(video: VideoORM) -> Video:
        print(f'to_entity -> video.rating = {video.rating} -- type = {type(video.rating)}')
        return Video(
            id=video.id,
            title=video.title,
            description=video.description,
            launch_year=video.launch_year,
            duration=video.duration,
            opened=video.opened,
            #published=video.published,
            rating=Rating(video.rating),
            categories={category.id for category in video.categories.all()},
            genres={genre.id for genre in video.genres.all()},
            cast_members={cast_member.id for cast_member in video.cast_members.all()},
        )
    
    # Quando não converto video.rating PARA Rating(video.rating) -> ERRO NA REGRA DE NEGOCIO DE VIDEO
    # Qando converto para Rating(video.rating) -> ERRO:  'Rating.AGE_12' is not a valid Rating