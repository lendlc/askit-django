from django.urls import include, path, re_path
from rest_framework import permissions, routers

from . import views

app_name = 'vid'

urlpatterns = [
    path('upload/', views.TutorUploadVideo.as_view()),
    path('list/', views.VideoList.as_view()),
    path('<int:id>/', views.VideoByID.as_view()),
    path('my_uploads/', views.MyVideos.as_view()),
]
