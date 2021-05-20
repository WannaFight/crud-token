from typing import Union

from django.contrib.auth.models import User
from django.http import Http404
from rest_framework import mixins, generics
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from .serializers import UserSerializer


class UserList(mixins.ListModelMixin,
               mixins.CreateModelMixin,
               generics.GenericAPIView):
    """
    /api/v1/users/ endpoint.
    """
    permission_classes = [IsAuthenticated]
    queryset = User.objects.all()
    serializer_class = UserSerializer

    def get(self, request, *args, **kwargs):
        """
        Return every user from auth_user table without `write_only` fields.
        """
        return self.list(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        """
        Create new user in auth_user table and return created user.
        """
        return self.create(request, *args, **kwargs)


class UserDetail(mixins.RetrieveModelMixin,
                 mixins.UpdateModelMixin,
                 mixins.DestroyModelMixin,
                 generics.GenericAPIView):
    """
    /api/v1/users/{int} endpoint
    [GET, PUT, PATCH, DELETE]
    """
    permission_classes = [IsAuthenticated]
    queryset = User.objects.all()
    serializer_class = UserSerializer

    def get(self, request, *args, **kwargs) -> Union[Response, Http404]:
        """
        Return single user with id==`pk` or 404.
        """
        return self.retrieve(request, *args, **kwargs)

    def put(self, request, *args, **kwargs) -> Union[Response, Http404]:
        """
        Update fields for user with id==`pk` and return a new one.

        Have to pass `username`, `password` and `is_active`
        even though they won't be changed.
        """
        return self.update(request, *args, **kwargs)

    def patch(self, request, *args, **kwargs):
        """
        Partially update fields for user with id==`pk`.
        """
        kwargs['partial'] = True
        return self.update(request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        """
        Delete user with id==`pk`.
        """
        return self.destroy(request, *args, **kwargs)
