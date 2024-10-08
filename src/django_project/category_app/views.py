from django.shortcuts import render
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.request import Request
from rest_framework.status import HTTP_200_OK, HTTP_400_BAD_REQUEST, HTTP_404_NOT_FOUND, HTTP_201_CREATED, HTTP_204_NO_CONTENT
from uuid import UUID
from src.core.category.application.use_cases.list_category import ListCategoryRequest, ListCategory
from src.core.category.application.use_cases.get_category import GetCategory, GetCategoryRequest
from src.core.category.application.use_cases.create_category import CreateCategoryRequest, CreateCategory
from src.core.category.application.use_cases.update_category import UpdateCategoryRequest, UpdateCategory
from src.core.category.application.use_cases.delete_category import DeleteCategoryRequest, DeleteCategory
from src.core.category.application.use_cases.exceptions import CategoryNotFound
from src.django_project.category_app.serializers import ListCategoryResponseSerializer, RetrieveCategoryRequestSerializer, RetrieveCategoryResponseSerializer, CreateCategoryRequestSerializer, CreateCategoryResponseSerializer, UpdateCategoryRequestSerializer, DeleteCategoryRequestSerializer, UpdatePartialCategoryRequestSerializer
from src.django_project.category_app.repository import DjangoORMCategoryRepository
from src.django_project.permissions import IsAdmin, IsAuthenticated


class CategoryViewSet(viewsets.ViewSet):
    permission_classes = [IsAuthenticated & IsAdmin]

    def list(self, request: Request) -> Response:
        order_by = request.query_params.get("order_by", "")
        current_page = int(request.query_params.get("current_page", 1))

        input = ListCategoryRequest(order_by=order_by, current_page=current_page)
        use_case = ListCategory(repository=DjangoORMCategoryRepository())
        response = use_case.execute(input)
        serializer = ListCategoryResponseSerializer(instance=response)
        return Response(status=HTTP_200_OK, data=serializer.data)
    
    def retrieve(self, request: Request, pk=None) -> Response:
        serializer = RetrieveCategoryRequestSerializer(data={"id":pk})
        serializer.is_valid(raise_exception=True)
        
        use_case = GetCategory(repository=DjangoORMCategoryRepository())
        try:
            result = use_case.execute(request=GetCategoryRequest(id=serializer.validated_data["id"]))
        except CategoryNotFound:
            return Response(status=HTTP_404_NOT_FOUND)

        category_output = RetrieveCategoryResponseSerializer(instance=result)

        return Response(status=HTTP_200_OK, data=category_output.data)
    
    def create(self, request: Request) -> Response:
        serializer = CreateCategoryRequestSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        input = CreateCategoryRequest(**serializer.validated_data)
        use_case = CreateCategory(repository=DjangoORMCategoryRepository())
        output = use_case.execute(request=input)

        return Response(
            status=HTTP_201_CREATED,
            data=CreateCategoryResponseSerializer(instance=output).data
        )

    def update(self,request: Request, pk=None) -> Response:
        serializer = UpdateCategoryRequestSerializer(
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
    
    def destroy(self,request: Request, pk=None) -> Response:
        serializer = DeleteCategoryRequestSerializer(data={"id":pk})
        serializer.is_valid(raise_exception=True)

        input = DeleteCategoryRequest(**serializer.validated_data)
        use_case = DeleteCategory(repository=DjangoORMCategoryRepository())
        try:
            use_case.execute(request=input)
        except CategoryNotFound:
            return Response(status=HTTP_404_NOT_FOUND)

        return Response(
            status=HTTP_204_NO_CONTENT,
        )

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
        