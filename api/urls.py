from django.urls import include, path, re_path
from rest_framework import permissions, routers
from drf_yasg.views import get_schema_view
from drf_yasg import openapi

from . import views

app_name = 'api'

schema_view = get_schema_view(
   openapi.Info(
      title="Capstone - ASK IT",
      default_version='v1',
      description="Description",
      terms_of_service="https://www.google.com/policies/terms/",
      contact=openapi.Contact(email="contact@snippets.local"),
      license=openapi.License(name="BSD License"),
   ),
   public=True,
   permission_classes=(permissions.AllowAny,),
)

router = routers.DefaultRouter()


urlpatterns = [
    path('', include(router.urls)),  # shows registered routes

    # swagger
    re_path(r'^docs(?P<format>\.json|\.yaml)$', schema_view.without_ui(cache_timeout=0), name='schema-json'),
    path('docs/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),

    # admin
    path('admin/users/', views.Users.as_view()),

    # auth
    path('auth/obtain_auth_token/', views.CustomObtainAuthToken.as_view()),
    path('auth/login/', views.Login.as_view()),
    path('auth/register/', views.Register.as_view()),
    path('auth/logout/', views.Logout.as_view()),
    path('auth/password_change/', views.ChangePassword.as_view()),
    # path('auth/password_forgot/) # Send Reset Token to Email
    # path('auth/password_reset/) # Validate Send token to Email
    # path('auth/profile')
]