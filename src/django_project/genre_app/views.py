from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.request import Request
from rest_framework.status import HTTP_200_OK, HTTP_400_BAD_REQUEST, HTTP_404_NOT_FOUND, HTTP_201_CREATED, HTTP_204_NO_CONTENT
from src.core.genre.application.use_cases.list_genre import ListGenre
from src.core.genre.application.use_cases.create_genre import CreateGenre
from src.core.genre.application.use_cases.delete_genre import DeleteGenre
from src.core.genre.application.use_cases.get_genre import GetGenre
from src.core.genre.application.use_cases.update_genre import UpdateGenre

from src.core.genre.application.use_cases.exceptions import InvalidGenre, RelatedCategoriesNotFound, GenreNotFound
from src.django_project.genre_app.serializers import ListOutputSerializer, CreateGenreInputSerializer, CreateGenreOutputSerializer, DeleteGenreInputSerializer, RetrieveGenreInputSerializer, RetrieveGenreOutputSerializer, UpdateGenreInputSerializer
from src.django_project.category_app.repository import DjangoORMCategoryRepository
from src.django_project.genre_app.repository import DjangoORMGenreRepository
from src.django_project.permissions import IsAdmin, IsAuthenticated



class GenreViewSet(viewsets.ViewSet):
    permission_classes = [IsAuthenticated & IsAdmin]

    def list(self, request: Request) -> Response:
        order_by = request.query_params.get("order_by", "")
        current_page = int(request.query_params.get("current_page", 1))
        use_case = ListGenre(repository=DjangoORMGenreRepository())
        output: ListGenre.Output = use_case.execute(input=ListGenre.Input(order_by=order_by, current_page=current_page))
        serializer = ListOutputSerializer(instance=output)
        return Response(status=HTTP_200_OK, data=serializer.data)
    
    def retrieve(self, request: Request, pk=None) -> Response:
        serializer = RetrieveGenreInputSerializer(data={"id":pk})
        serializer.is_valid(raise_exception=True)
        
        input = GetGenre.Input(**serializer.validated_data)
        use_case = GetGenre(repository=DjangoORMGenreRepository())
        try:
            result = use_case.execute(input=input)
        except GenreNotFound:
            return Response(status=HTTP_404_NOT_FOUND)

        genre_output = RetrieveGenreOutputSerializer(instance=result)

        return Response(status=HTTP_200_OK, data=genre_output.data)
    
    
    def create(self, request: Request) -> Response:
        serializer = CreateGenreInputSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        use_case = CreateGenre(repository=DjangoORMGenreRepository(), category_repository=DjangoORMCategoryRepository())
        try:
            output = use_case.execute(input=CreateGenre.Input(**serializer.validated_data))
        except (InvalidGenre, RelatedCategoriesNotFound) as err:
            return Response(data={"error": str(err)}, status=HTTP_400_BAD_REQUEST)

        return Response(
            status=HTTP_201_CREATED,
            data=CreateGenreOutputSerializer(instance=output).data
        )

    def update(self,request: Request, pk=None) -> Response:
        serializer = UpdateGenreInputSerializer(
            data={
                **request.data, 
                "id":pk
                }
            )
        serializer.is_valid(raise_exception=True)

        input = UpdateGenre.Input(**serializer.validated_data)
        use_case = UpdateGenre(repository=DjangoORMGenreRepository(), category_repository=DjangoORMCategoryRepository())
        try:
            use_case.execute(input=input)
        except (InvalidGenre, RelatedCategoriesNotFound) as err:
            return Response(data={"error": str(err)}, status=HTTP_400_BAD_REQUEST)
        except GenreNotFound as err:
            return Response(data={"error": str(err)}, status=HTTP_404_NOT_FOUND)

        return Response(
            status=HTTP_204_NO_CONTENT,
        )
    
    def destroy(self,request: Request, pk=None) -> Response:
        serializer = DeleteGenreInputSerializer(data={"id":pk})
        serializer.is_valid(raise_exception=True)

        input = DeleteGenre.Input(**serializer.validated_data)
        use_case = DeleteGenre(repository=DjangoORMGenreRepository())
        try:
            use_case.execute(input=input)
        except GenreNotFound:
            return Response(
                status=HTTP_404_NOT_FOUND,
                data={"error": f"Genre with id {pk} not found"},)

        return Response(
            status=HTTP_204_NO_CONTENT,
        )

    """
    def partial_update(self, request, pk: UUID = None) -> Response:
        serializer = UpdatePartialCategoryRequestSerializer(
            data={
                **request.data, 
                "id":pk
                }
            )
        serializer.is_valid(raise_exception=True)

        input = UpdateCategoryRequest(**serializer.validated_data)
        use_case = UpdateCategory(repository=DjangoORMCategoryRepository())
        try:
            use_case.execute(request=input)
        except CategoryNotFound:
            return Response(status=HTTP_404_NOT_FOUND)

        return Response(
            status=HTTP_204_NO_CONTENT,
        )
         """