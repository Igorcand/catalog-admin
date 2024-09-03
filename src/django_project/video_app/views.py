from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.request import Request
from rest_framework.status import HTTP_200_OK, HTTP_400_BAD_REQUEST, HTTP_404_NOT_FOUND, HTTP_201_CREATED, HTTP_204_NO_CONTENT
from src.django_project.video_app.serializers import CreateVideoWithoutMediaInputSerializer, CreateVideoWithoutMediaOutputSerializer
from src.django_project.category_app.repository import DjangoORMCategoryRepository
from src.django_project.genre_app.repository import DjangoORMGenreRepository
from src.django_project.cast_member_app.repository import DjangoORMCastMemberRepository
from src.django_project.video_app.repository import DjangoORMVideoRepository
from src.core.video.application.use_cases.create_video_without_media import CreateVideoWithoutMedia
from src.core.video.application.use_cases.exceptions import RelatedEntitiesNotFound, InvalidVideo


class VideoViewSet(viewsets.ViewSet):
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