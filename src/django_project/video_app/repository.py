from uuid import UUID
from django.db import transaction
from src.core.video.domain.video_repository import VideoRepository
from src.core.video.domain.video import Video
from src.django_project.video_app.models import Video as VideoORM

class DjangoORMVideoRepository(VideoRepository):
    def save(self, video: Video):
        with transaction.atomic():
            VideoModelMapper.to_model(video)

    def get_by_id(self, id: UUID) -> Video | None:
        try:
            video_model = VideoORM.objects.get(id=id)
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
        
        with transaction.atomic():
            VideoORM.objects.filter(id=video.id).update(
                title=video.title,
                description=video.description,
                launch_year=video.launch_year,
                duration=video.duration,
                published=video.published,
                rating=video.rating,
            )

            video_model.categories.set(video.categories)
            video_model.genres.set(video.genres)
            video_model.cast_members.set(video.cast_members)

    
    def list(self) -> list[Video]:
        return [
            VideoModelMapper.to_entity(video_model)
         for video_model in VideoORM.objects.all()]

class VideoModelMapper:
    @staticmethod
    def to_model(video: Video) -> VideoORM:
        video_model = VideoORM.objects.create(
            id=video.id,
            title=video.title,
            description=video.description,
            launch_year=video.launch_year,
            duration=video.duration,
            opened=False,
            published=video.published,
            rating=video.rating,
        )

        video_model.categories.set(video.categories)
        video_model.genres.set(video.genres)
        video_model.cast_members.set(video.cast_members)
        
        return video_model
    
    def to_entity(video: VideoORM) -> Video:
        return Video(
            id=video.id,
            title=video.title,
            description=video.description,
            launch_year=video.launch_year,
            duration=video.duration,
            published=video.published,
            rating=video.rating,
            categories={category.id for category in video.categories.all()},
            genres={genre.id for genre in video.genres.all()},
            cast_members={cast_member.id for cast_member in video.cast_members.all()},
        )