from django.urls import include, path, re_path
from rest_framework import permissions, routers
from drf_yasg.views import get_schema_view
from drf_yasg import openapi

from api.views.auth import *

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
    path('', include(router.urls)), #shows registered routes
    re_path(r'^docs(?P<format>\.json|\.yaml)$', schema_view.without_ui(cache_timeout=0), name='schema-json'),
    path('docs/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),

    #app routes
    path('admin/users/', Users.as_view()),
    path('auth/register/tutor/', RegisterTutor.as_view())
]