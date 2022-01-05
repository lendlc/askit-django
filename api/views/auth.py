from django.db.models.query import QuerySet
from rest_framework.response import Response
from rest_framework import generics, permissions, status

from api.models import User, Tutor
from api.serializers.auth import *


# @route    GET /admin/users/
# @desc     View All Users or by their ID
# @access   Private
class Users(generics.ListAPIView):
    permission_classes = (permissions.AllowAny,) #TODO - make authenticated
    queryset = User.objects.all()
    serializer_class = AuthSerializer

    def get_queryset(self):
        qs = super().get_queryset()
        id = self.request.GET.get('id', None)
        if id is not None:
            qs = qs.filter(id=id)
        return qs

# @route    POST /auth/register/tutor/
# @desc     Create a Tutor Account
# @access   Public
class RegisterTutor(generics.CreateAPIView):
    permission_classes = (permissions.AllowAny,)
    queryset = Tutor.objects.all()
    serializer_class = RegistrationSerializer

    #shorturl.at/jmLQ5
    def create(self, request, *args, **kwargs): 
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        return Response(status=status.HTTP_201_CREATED) 
