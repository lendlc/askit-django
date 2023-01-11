from django.urls import include, path, re_path
from rest_framework import permissions, routers


from . import views

app_name = 'chat'

urlpatterns = [
    path('conversations/', views.GetConservation.as_view()),
    path('conversations/<int:id>/', views.GetMessages.as_view()),
    path('message/', views.SendMessage.as_view()),
]
