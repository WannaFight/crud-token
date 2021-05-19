from django.urls import path

from . import views

app_name = 'crud'
urlpatterns = [
    path('users/', views.UserList.as_view(), name='list'),
    path('users/<int:pk>/', views.UserDetail.as_view(), name='detail'),
]
