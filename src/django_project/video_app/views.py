from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.request import Request
from rest_framework.status import HTTP_200_OK, HTTP_400_BAD_REQUEST, HTTP_404_NOT_FOUND, HTTP_201_CREATED, HTTP_204_NO_CONTENT
from src.django_project.video_app.serializers import CreateVideoWithoutMediaInputSerializer, CreateVideoWithoutMediaOutputSerializer, ListOutputSerializer, RetrieveVideoInputSerializer, RetrieveVideoOutputSerializer
from src.django_project.category_app.repository import DjangoORMCategoryRepository
from src.django_project.genre_app.repository import DjangoORMGenreRepository
from src.django_project.cast_member_app.repository import DjangoORMCastMemberRepository
from src.django_project.video_app.repository import DjangoORMVideoRepository
from src.core.video.application.use_cases.create_video_without_media import CreateVideoWithoutMedia
from src.core.video.application.use_cases.list_videos import ListVideo
from src.core.video.application.use_cases.get_video import GetVideo


from src.core.video.application.use_cases.exceptions import RelatedEntitiesNotFound, InvalidVideo, VideoNotFound
from uuid import UUID
from src.core.video.application.use_cases.upload_video import UploadVideo
from src.core._shered.infrastructure.storage.local_storage import LocalStorage


class VideoViewSet(viewsets.ViewSet):
    def list(self, request: Request) -> Response:
        order_by = request.query_params.get("order_by", "")
        current_page = int(request.query_params.get("current_page", 1))
        use_case = ListVideo(repository=DjangoORMVideoRepository())
        output: ListVideo.Output = use_case.execute(input=ListVideo.Input(order_by=order_by, current_page=current_page))
        serializer = ListOutputSerializer(instance=output)
        return Response(status=HTTP_200_OK, data=serializer.data)

    def retrieve(self, request: Request, pk=None) -> Response:
        serializer = RetrieveVideoInputSerializer(data={"id":pk})
        serializer.is_valid(raise_exception=True)
        
        input = GetVideo.Input(**serializer.validated_data)
        use_case = GetVideo(repository=DjangoORMVideoRepository())
        try:
            result = use_case.execute(input=input)
        except VideoNotFound:
            return Response(status=HTTP_404_NOT_FOUND)

        genre_output = RetrieveVideoOutputSerializer(instance=result)

        return Response(status=HTTP_200_OK, data=genre_output.data)
    
    def create(self, request: Request) -> Response:
        serializer = CreateVideoWithoutMediaInputSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        use_case = CreateVideoWithoutMedia(
            repository=DjangoORMVideoRepository(), 
            category_repository=DjangoORMCategoryRepository(), 
            genre_repository=DjangoORMGenreRepository(),
            cast_member_repository=DjangoORMCastMemberRepository())
        try:
            output = use_case.execute(input=CreateVideoWithoutMedia.Input(**serializer.validated_data))
        except (InvalidVideo, RelatedEntitiesNotFound) as err:
            return Response(data={"error": str(err)}, status=HTTP_400_BAD_REQUEST)

        return Response(
            status=HTTP_201_CREATED,
            data=CreateVideoWithoutMediaOutputSerializer(instance=output).data
        )

    def partial_update(self, request: Request, pk: UUID = None) -> Response:
        file = request.FILES['video_file']
        content = file.read()
        content_type = file.content_type

        upload_video = UploadVideo(
            repository=DjangoORMVideoRepository(), 
            storage_service=LocalStorage()
        )

        try:
            upload_video.execute(
                input=UploadVideo.Input(
                    video_id=pk,
                    file_name=file.name,
                    content=content,
                    content_type=content_type
                )
            )
        except VideoNotFound as err:
            return Response(data={"error": str(err)}, status=HTTP_404_NOT_FOUND)
        
        return Response(
            status=HTTP_200_OK,
        )
