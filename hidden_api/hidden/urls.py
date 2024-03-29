from django.urls import path
from rest_framework.routers import DefaultRouter
from . import views

urlpatterns = [
    path('api/member/', views.MemberListCreate.as_view()),
    path('api/member/part_update/<int:pk>/',
         views.MemberPartialUpdate.as_view()),
    path('api/customer/postlist/', views.post_peoples),
    path('api/draft/', views.SecretBoxListView.as_view(), name='draft-list'),
    path('api/draft/<int:pk>/', views.draft_detail.as_view(), name='draft-detail'),
    path('api/draft/part_update/<int:pk>/',
         views.SecretPartialUpdate.as_view()),
    path('api/draftpermission/<int:pk>/',
         views.draft_permission, name='draft-permission'),
    path('api/draft/swop/', views.swop_peoples),
    path('api/draft/email/', views.send_emails),
    path('api/membership/<int:pk>/',
         views.membership_detail.as_view(), name='membership-detail'),
    path('api/membership/part_update/<int:pk>/',
         views.MembershipPartialUpdate.as_view()),
    path('api/users/register/', views.UserCreate.as_view(), name='user-create'),
    path('api/users/login/', views.UserLogin.as_view(), name='user-login'),
    path('api/users/current/', views.current_user, name='user-current'),
    path('api/users/part_update/<int:pk>/', views.UserPartialUpdate.as_view()),
    path('api/users/change_password/',
         views.UserPasswordUpdate.as_view(), name="change_password"),
    path('api/users/restore_password/', views.restore_password),

    # path('api/check_system/', views.check_system, name='check-system'),

]
