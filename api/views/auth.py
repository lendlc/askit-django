from rest_framework.response import Response
from rest_framework import generics, permissions, status
from api.serializers.auth import *

from rest_framework.authtoken.models import Token
from rest_framework.authtoken.views import ObtainAuthToken
from api.utils import create_token


# @route    POST /auth/obtain_auth/token/
# @desc     Get Auth Token for Protected Requests
# @access   Public
class CustomObtainAuthToken(ObtainAuthToken):
    permission_classes = (permissions.AllowAny, )

    def post(self, request, *args, **kwargs):
        response = super(CustomObtainAuthToken, self).post(request, *args, **kwargs)
        token = Token.objects.get(key=response.data['token'])
        user = token.user
        response = {
            'token': token.key,
            'id': user.id,
        }
        return Response(response)


# @route    POST /auth/login
# @desc     User Login
# @access   Public
class Login(generics.GenericAPIView):
    permission_classes = (permissions.AllowAny,)
    queryset = User.objects.all()
    serializer_class = LoginSerializer

    # not entirely sure what this does
    # def dispatch(self, request, *args, **kwargs):
    #     return super(Login, self).dispatch(request, *args, **kwargs)

    def format_response(self):
        return {
            "token": self.token.key,
            "id": self.user.id,
            "full_name": self.user.get_full_name(),
            "role": self.user.role
        }

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data, context={'request': request})
        serializer.is_valid(raise_exception=True)

        self.user = serializer.validated_data['user']
        self.token = create_token(self.user.id)
        res = self.format_response()

        return Response(data=res, status=status.HTTP_200_OK)


# @route    GET /admin/users/
# @desc     View All Users or by their ID
# @access   Private
class Users(generics.ListAPIView):
    permission_classes = (permissions.IsAuthenticated,)
    queryset = User.objects.all()
    serializer_class = AuthSerializer

    def get_queryset(self):
        qs = super().get_queryset()
        user_id = self.request.GET.get('id', None)
        if user_id is not None:
            qs = qs.filter(id=user_id)
        return qs


# @route    POST /auth/register/tutor/
# @desc     Create a Tutor Account
# @access   Public
class RegisterTutor(generics.CreateAPIView):
    permission_classes = (permissions.AllowAny,)
    queryset = Tutor.objects.all()
    serializer_class = RegistrationSerializer

    # shorturl.at/jmLQ5
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        return Response(status=status.HTTP_201_CREATED)
