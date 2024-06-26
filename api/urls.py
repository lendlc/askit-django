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
   re_path(r'^docs(?P<format>\.json|\.yaml)$', schema_view.without_ui(
      cache_timeout=0), name='schema-json'),
   path('docs/', schema_view.with_ui('swagger',
      cache_timeout=0), name='schema-swagger-ui'),

   # admin
   path('admin/users/', views.Users.as_view()),
   path('admin/schedules/', views.Schedules.as_view()),
   path('admin/appointments/', views.AppointmentsAdminList.as_view()),
   path('admin/dashboard/cards/', views.GetDataTypeCount.as_view()),
   path('admin/dashboard/donut_chart/', views.GetDonutChartData.as_view()),
   path('admin/dashboard/line_chart/', views.GetBarGraphData.as_view()),

   # auth
   path('auth/obtain_auth_token/', views.CustomObtainAuthToken.as_view()),
   path('auth/profile/', views.Profile.as_view()),
   path('auth/login/', views.Login.as_view()),
   path('auth/register/', views.Register.as_view()),
   path('auth/logout/', views.Logout.as_view()),
   path('auth/password_change/', views.ChangePassword.as_view()),
   path('auth/password_forgot/', views.ForgotPassword.as_view()),
   path('auth/password_reset/', views.ResetPassword.as_view()),
   path('auth/account/send_verification/',
      views.SendEmailVerification.as_view()),
   path('auth/account/verify/', views.VerifyEmailToken.as_view()),
   # path('auth/profile')

   # schedule
   path('schedules/', views.ListCreateSchedule.as_view()),
   path('schedule_list/', views.ScheduleList.as_view()),
   path('schedules/<int:pk>/', views.GetEditDeleteSchedule.as_view()),

   # appointment
   path('tutee/appointments/', views.TuteeAppointment.as_view()),
   
   path('tutors/', views.Tutors.as_view())
   #  path('/tutee/appointments/<int:pk>/', views.GetEditDeleteAppointment()),

]