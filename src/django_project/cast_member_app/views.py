from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.request import Request
from rest_framework.status import HTTP_200_OK, HTTP_400_BAD_REQUEST, HTTP_404_NOT_FOUND, HTTP_201_CREATED, HTTP_204_NO_CONTENT
from src.core.cast_member.application.use_cases.list_cast_member import ListCastMember, ListCastMemberRequest, ListCastMemberResponse
from src.core.cast_member.application.use_cases.create_cast_member import CreateCastMember, CreateCastMemberRequest, CreateCastMemberResponse
from src.core.cast_member.application.use_cases.delete_cast_member import DeleteCastMember, DeleteCastMemberRequest
from src.core.cast_member.application.use_cases.update_cast_member import UpdateCastMember, UpdateCastMemberRequest

from src.core.cast_member.application.use_cases.exceptions import InvalidCastMember, CastMemberNotFound
from src.django_project.cast_member_app.repository import DjangoORMCastMemberRepository

from src.django_project.cast_member_app.serializers import (
    CreateCastMemberRequestSerializer,
    CreateCastMemberResponseSerializer,
    DeleteCastMemberRequestSerializer,
    ListCastMemberResponseSerializer,
    UpdateCastMemberRequestSerializer,
)


class CastMemberViewSet(viewsets.ViewSet):
    def list(self, request: Request) -> Response:
        use_case = ListCastMember(repository=DjangoORMCastMemberRepository())
        output: ListCastMemberResponse = use_case.execute(request=ListCastMemberRequest)
        serializer = ListCastMemberResponseSerializer(instance=output)
        return Response(status=HTTP_200_OK, data=serializer.data)
    
    
    def create(self, request: Request) -> Response:
        serializer = CreateCastMemberRequestSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        use_case = CreateCastMember(repository=DjangoORMCastMemberRepository())
        output = use_case.execute(request=CreateCastMemberRequest(**serializer.validated_data))
        
        return Response(
            status=HTTP_201_CREATED,
            data=CreateCastMemberResponseSerializer(instance=output).data
        )

    def update(self,request: Request, pk=None) -> Response:
        serializer = UpdateCastMemberRequestSerializer(
            data={
                **request.data, 
                "id":pk
                }
            )
        serializer.is_valid(raise_exception=True)

        request = UpdateCastMemberRequest(**serializer.validated_data)
        use_case = UpdateCastMember(repository=DjangoORMCastMemberRepository())
        try:
            use_case.execute(request=request)
        except InvalidCastMember as err:
            return Response(data={"error": str(err)}, status=HTTP_400_BAD_REQUEST)
        except CastMemberNotFound as err:
            return Response(data={"error": str(err)}, status=HTTP_404_NOT_FOUND)

        return Response(
            status=HTTP_204_NO_CONTENT,
        )
    
    def destroy(self,request: Request, pk=None) -> Response:
        serializer = DeleteCastMemberRequestSerializer(data={"id":pk})
        serializer.is_valid(raise_exception=True)

        request = DeleteCastMemberRequest(**serializer.validated_data)
        use_case = DeleteCastMember(repository=DjangoORMCastMemberRepository())
        try:
            use_case.execute(request=request)
        except CastMemberNotFound:
            return Response(
                status=HTTP_404_NOT_FOUND,
                data={"error": f"CastMember with id {pk} not found"},)

        return Response(
            status=HTTP_204_NO_CONTENT,
        )

