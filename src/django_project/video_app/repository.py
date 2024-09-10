from uuid import UUID
from django.db import transaction
from src.core.video.domain.video_repository import VideoRepository
from src.core.video.domain.video import Video
from src.core.video.domain.value_objects import Rating
from src.django_project.video_app.models import Video as VideoORM
from src.django_project.video_app.models import AudioVideoMedia as AudioVideoMediaORM
from src.django_project.video_app.models import ImageMedia as ImageMediaORM

from src.core.video.domain.value_objects import AudioVideoMedia, MediaType, MediaStatus

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

    def update(self, video: Video, media_type: MediaType) -> None:
        try:
            video_model = VideoORM.objects.get(id=video.id)
        except VideoORM.DoesNotExist:
            return None
        else:
            with transaction.atomic():
                if media_type in [MediaType.VIDEO.value, MediaType.TRAILER.value]:
                    self._update_audio_video_media(video, video_model, media_type)
                else:
                    self._update_image_media(video, video_model, media_type)

                video_model.categories.set(video.categories)
                video_model.genres.set(video.genres)
                video_model.cast_members.set(video.cast_members)

                video_model.save()

                VideoORM.objects.filter(id=video_model.id).update(
                    title       = video.title,
                    description = video.description,
                    launch_year = video.launch_year,
                    opened      = video.opened,
                    published   = video.published,
                    duration    = video.duration,
                    rating      = video.rating.name,
                )      
        
    def list(self) -> list[Video]:
        return [
            VideoModelMapper.to_entity(video_model)
         for video_model in VideoORM.objects.all()]
    
    def _update_audio_video_media(self, video: Video, video_model, media_type):
        AudioVideoMediaORM.objects.filter(id=video_model.id).delete()

        attribute = video.video if media_type == MediaType.VIDEO.value else video.trailer
        audio_video_media = AudioVideoMediaORM.objects.create(
            name=attribute.name,
            raw_location=attribute.raw_location,
            encoded_location=attribute.encoded_location,
            status=attribute.status.name,
            media_type=attribute.media_type.name
        )

        if media_type == MediaType.VIDEO.value:
            video_model.video = audio_video_media
        elif media_type == MediaType.TRAILER.value:
            video_model.trailer = audio_video_media

    def _update_image_media(self, video: Video, video_model, media_type):
        ImageMediaORM.objects.filter(id=video_model.id).delete()

        attribute = {
            MediaType.BANNER.value: video.banner,
            MediaType.THUMBNAIL.value: video.thumbnail,
            MediaType.THUMBNAIL_HALF.value: video.thumbnail_half,
        }.get(media_type)

        image_media = ImageMediaORM.objects.create(
            name=attribute.name,
            raw_location=attribute.location
        )

        if media_type == MediaType.BANNER.value:
            video_model.banner = image_media
        elif media_type == MediaType.THUMBNAIL.value:
            video_model.thumbnail = image_media
        elif media_type == MediaType.THUMBNAIL_HALF.value:
            video_model.thumbnail_half = image_media


class VideoModelMapper:
    @staticmethod
    def to_model(model: Video) -> VideoORM:
        video_model = VideoORM.objects.create(
            id=model.id,
            title=model.title,
            description=model.description,
            launch_year=model.launch_year,
            duration=model.duration,
            rating=model.rating.name,
            opened=False,
            published=model.published,
        )

        video_model.categories.set(model.categories)
        video_model.genres.set(model.genres)
        video_model.cast_members.set(model.cast_members)
        
        return video_model
    
    def to_entity(model: VideoORM) -> Video:
        video = Video(
            id=model.id,
            title=model.title,
            description=model.description,
            launch_year=model.launch_year,
            duration=model.duration,
            opened=model.opened,
            #published=video.published,
            rating=Rating(model.rating),
            categories={category.id for category in model.categories.all()},
            genres={genre.id for genre in model.genres.all()},
            cast_members={cast_member.id for cast_member in model.cast_members.all()},
        )
    
        if model.video:
            video.video = AudioVideoMedia(
                name=model.video.name,
                raw_location=model.video.raw_location,
                encoded_location=model.video.encoded_location,
                status=MediaStatus(model.video.status),
                media_type=MediaType(model.video.media_type),
            )
        if model.trailer:
            video.trailer = AudioVideoMedia(
                name=model.trailer.name,
                raw_location=model.trailer.raw_location,
                encoded_location=model.trailer.encoded_location,
                status=MediaStatus(model.trailer.status),
                media_type=MediaType(model.trailer.media_type),
            )
        
        return video
    
