from typing import Union

from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404
from django.http import Http404
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.status import (
    HTTP_201_CREATED,
    HTTP_204_NO_CONTENT,
    HTTP_400_BAD_REQUEST,
)
from rest_framework.views import APIView

from .serializers import UserSerializer


class UserList(APIView):
    """
    /api/v1/users/ endpoint.
    """
    permission_classes = [IsAuthenticated]

    def get(self, request) -> Response:
        """
        Return every user from auth_user table without `write_only` fields.
        """
        users = User.objects.all()
        serializer = UserSerializer(users, many=True)

        return Response(serializer.data)

    def post(self, request) -> Response:
        """
        Create new user in auth_user table and return created user.
        """
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=HTTP_201_CREATED)
        return Response(serializer.errors, status=HTTP_400_BAD_REQUEST)


class UserDetail(APIView):
    """
    /api/v1/users/{int} endpoint
    [GET, PUT, PATCH, DELETE]
    """
    permission_classes = [IsAuthenticated]

    def get(self, request, pk: int) -> Union[Response, Http404]:
        """
        Return single user with id==`pk` or 404.
        """
        user = get_object_or_404(User, pk=pk)
        serializer = UserSerializer(user)
        return Response(serializer.data)

    def put(self, request, pk: int) -> Union[Response, Http404]:
        """
        Update fields for user with id==`pk` and return a new one.

        Have to pass `username` and `password`
        even though they won't be changed.
        """
        user = get_object_or_404(User, pk=pk)
        serializer = UserSerializer(user, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=HTTP_400_BAD_REQUEST)

    def patch(self, request, pk: int) -> Union[Response, Http404]:
        """
        Partially update fields for user with id==`pk`.
        """
        user = get_object_or_404(User, pk=pk)
        serializer = UserSerializer(user, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=HTTP_400_BAD_REQUEST)

    def delete(self, request, pk: int) -> Union[Response, Http404]:
        """
        Delete user with id==`pk`.
        """
        user = get_object_or_404(User, pk=pk)
        user.delete()
        return Response(status=HTTP_204_NO_CONTENT)
