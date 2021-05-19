from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404
from rest_framework.response import Response
from rest_framework.views import APIView

from .serializers import UserSerializer


class UserList(APIView):
    """
    /api/v1/users/ endpoint.
    """
    def get(self, request):
        """
        Return every user from auth_user table without `write_only` fields.
        """
        users = User.objects.all()
        serializer = UserSerializer(users, many=True)

        return Response(serializer.data)

    def post(self, request):
        """
        Create new user in auth_user table.
        :return: Response object with new user or with an error message.
        """
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=201)
        return Response(serializer.errors, status=400)


class UserDetail(APIView):
    """
    /api/v1/users/{int} endpoint
    [GET, PUT, PATCH, DELETE]
    """

    def get(self, request, pk: int):
        user = get_object_or_404(User, pk=pk)
        serializer = UserSerializer(user)

        return Response(serializer.data)

    def put(self, request, pk: int):
        user = get_object_or_404(User, pk=pk)
        serializer = UserSerializer(user, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=400)

    def patch(self, request, pk: int):
        user = get_object_or_404(User, pk=pk)
        serializer = UserSerializer(user, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=400)

    def delete(self, request, pk: int):
        user = get_object_or_404(User, pk=pk)
        user.delete()
        return Response(status=204)

