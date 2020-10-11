from django.urls import path
from rest_framework.routers import DefaultRouter
from . import views

urlpatterns = [
    path('api/customer/', views.MemberListCreate.as_view()),
    path('api/customer/postlist/', views.post_peoples),
    path('api/draft/', views.SecretBoxListView.as_view(), name='draft-list'),
    path('api/draft/<int:pk>/', views.draft_detail.as_view(), name='draft-detail'),
    path('api/draftpermission/<int:pk>/', views.draft_permission, name='draft-permission'),
    path('api/draft/swop/', views.swop_peoples),
    path('api/membership/<int:pk>/', views.membership_detail.as_view(), name='membership-detail'),
    path('api/users/register/', views.UserCreate.as_view(), name='user-create'),
    path('api/users/login/', views.UserLogin.as_view(), name='user-login'),
    # path('api/check_system/', views.check_system, name='check-system'),
    
]
