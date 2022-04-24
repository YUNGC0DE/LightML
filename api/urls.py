from django.urls import path, include, re_path
from .views import *

urlpatterns = [
    path('auth/', include('djoser.urls')),
    re_path('auth/', include('djoser.urls.authtoken')),
    path('account/', AccountAPIView.as_view()),
    path('account/create/', AccountCreateAPIView.as_view()),
    path('projects/', ProjectsAPIView.as_view()),
    path('projects/create/', ProjectCreateAPIView.as_view()),
    path('projects/<int:pk>/', ProjectAPIView.as_view()),
    path('projects/<int:pk>/update/', ProjectUpdateAPIView.as_view()),
    path('projects/<int:pk>/delete/', ProjectDeleteAPIView.as_view()),
]