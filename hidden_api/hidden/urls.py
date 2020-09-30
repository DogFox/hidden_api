from django.urls import path
from rest_framework.routers import DefaultRouter
from . import views

urlpatterns = [
    path('api/customer/', views.UserListCreate.as_view()),
    path('api/customer/postlist/', views.post_peoples),
    path('api/draft/', views.SecretBoxListView.as_view(), name='draft-list'),
    path('api/draft/<int:pk>/', views.draft_detail.as_view(), name='draft-detail'),
]
