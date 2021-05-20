from django.contrib.auth.models import User
from rest_framework import status
from rest_framework.generics import (
    ListCreateAPIView,
    RetrieveUpdateDestroyAPIView
)
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from .serializers import UserSerializer


class UserList(ListCreateAPIView):
    """
    /api/v1/users/ endpoint.

    GET: list all users  or create a new user.
    POST: create a new user.
    Have to pass authorization token obtained from /api-token-auth/.
    """
    permission_classes = [IsAuthenticated]
    queryset = User.objects.all()
    serializer_class = UserSerializer


class UserDetail(RetrieveUpdateDestroyAPIView):
    """
    /api/v1/users/{int} endpoint.

    GET: list user with id==`pk`.
    PUT, PATCH: update user with id==`pk`
    DELETE: delete users with id==`pk`
    """
    permission_classes = [IsAuthenticated]
    queryset = User.objects.all()
    serializer_class = UserSerializer

    def delete(self, request, *args, **kwargs):
        """
        Delete user with id==`pk`. User isn't able to delete himself.
        """
        if kwargs['pk'] == request.user.pk:
            return Response(
                {'detail': "You can not delete yourself."},
                status=status.HTTP_409_CONFLICT
            )
        return self.destroy(request, *args, **kwargs)
