from django.urls import path
from . import views

urlpatterns = [
    path('api/customer/', views.CustomerListCreate.as_view()),
    path('api/customer/postlist/', views.post_peoples),
    path('api/draft/', views.SecretBoxListView.as_view()),
]
