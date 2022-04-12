import base64
import json
from rest_framework.response import Response
from rest_framework import generics, permissions, status
from rest_framework.authtoken.models import Token
from rest_framework.authtoken.views import ObtainAuthToken

from django.shortcuts import get_object_or_404
from django.contrib.auth.tokens import default_token_generator
from django.contrib.auth.models import update_last_login
from django.conf import settings
from api.serializers.AuthSerializer import *
from datetime import datetime, timedelta

from api.utils import create_token, required_field_err, send_basic_email, gen_six_digit_code, send_html_email

"""
@route    POST /auth/obtain_auth_token/
@desc     Get Auth Token for Protected Requests
@access   Public
"""
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


"""
@route    POST /auth/login
@desc     User Login
@access   Public
"""
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
            "role": self.user.role,
        }

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data, context={'request': request})
        serializer.is_valid(raise_exception=True)

        self.user = serializer.validated_data['user']
        self.token = create_token(self.user)
        res = self.format_response()
        update_last_login(None, self.user)

        return Response(data=res, status=status.HTTP_200_OK)


"""
@route    POST /auth/register/
@desc     Create a Tutor Account
@access   Public
"""
class Register(generics.CreateAPIView):
    permission_classes = (permissions.AllowAny,)
    queryset = User.objects.all()
    serializer_class = RegistrationSerializer

    # shorturl.at/jmLQ5
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)

        return Response(status=status.HTTP_201_CREATED)


"""
@route    POST /auth/logout/
@desc     Remove Auth Token from User
@access   Private
"""
class Logout(generics.GenericAPIView):
    permission_classes = (permissions.IsAuthenticated,)

    def post(self, request):
        try:
            request.user.auth_token.delete()
        except Exception as e:
            pass

        # could add a logger for this action
        return Response({"message": "successfully logged out"}, status=status.HTTP_200_OK)

"""
@route    PUT /auth/password_change/
@desc     Change User's Password
@access   Private
"""
class ChangePassword(generics.GenericAPIView):
    permission_classes = (permissions.IsAuthenticated,)
    serializer_class = ChangePasswordSerializer

    def put(self, request):
        serializer = self.get_serializer(data=request.data, context={'request': request})
        serializer.is_valid(raise_exception=True)

        user = request.user
        user.set_password(serializer.data.get('new_password'))
        user.save()

        return Response({"message": "password updated"}, status=status.HTTP_200_OK)

"""
@route    POST /auth/password_forgot/
@desc     Send Change Password Token to User's email
@access   Public
"""
class ForgotPassword(generics.GenericAPIView):
    permission_classes = (permissions.AllowAny,)
    
    def post(self, request):
        email = request.data.get('email', None)
        
        if not email:
            return required_field_err('email')
           
        user = get_object_or_404(User, email=email)
        
        user.reset_pw_exp = datetime.now() + timedelta(minutes=5)
        user.reset_pw_code = gen_six_digit_code()
        user.save()
        
        body = """Your password reset code is %s, this code is valid for 5mins. Please do not share this code with others.
        """ % user.reset_pw_code
        send_basic_email(title='Forgot Password', body=body, email_to=user.email)
            
        return Response({"msg": "email sent"}, status=status.HTTP_200_OK)

"""
@route    POST /auth/password_reset/
@desc     Reset User's Password
@access   Public
"""
class ResetPassword(generics.GenericAPIView):
    permission_classes = (permissions.AllowAny,)
    serializer_class = ResetPasswordSerializer
    
    def put(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        user = get_object_or_404(User, email=serializer.data.get('email'))
        user.set_password(serializer.data.get('new_password'))
        user.reset_pw_code = None
        user.reset_pw_exp = None
        user.save()
        
        return Response("updated", status=status.HTTP_200_OK)


"""
@route  POST /auth/account/send_verification/
@desc   Send Account Activation Link to email.
@access Public
"""
class SendEmailVerification(generics.GenericAPIView):
    permission_classes = (permissions.AllowAny,)
    
    def post(self, request):
        email = request.data.get('email', None)
        
        if not email:
            return required_field_err('email')
        
        user = get_object_or_404(User, email=email)
        
        token = self.get_verification_token(user)
        url = "%s/account_activate/%s/" % (settings.WEB_APP_URL, token)
    
        send_html_email(
            subject='Account Activation', 
            template='account_activation.html', 
            data={'url': url},  
            email_to='cuyuganjohnlendl@gmail.com'
        )
        
        return Response({"msg": "email sent", "token": token}, status=status.HTTP_200_OK)
    
    @staticmethod
    def get_verification_token(user):
        token = json.dumps({
            'uid': user.id,
            'email': user.email,
            'token': default_token_generator.make_token(user)
        }).encode('utf-8')
        
        b64_token = base64.urlsafe_b64encode(token)
        
        return b64_token


"""
@route  POST /auth/account/verify/
@desc   Verify Account Using Token
@access Public
"""
class VerifyEmailToken(generics.GenericAPIView):
    permission_classes = (permissions.AllowAny,)
    
    def post(self, request):
        token = request.data.get('token', None)
        
        if not token:
            return required_field_err('token')
        
        user, error = self.validate_b64_token(token)
        
        if error:
            return Response({"err": error}, status=status.HTTP_400_BAD_REQUEST)
        
        user.is_verified = True
        user.save()
        
        return Response({"msg": "account verified"}, status=status.HTTP_200_OK)
    
    @staticmethod
    def validate_b64_token(token):
        try:
            json_data = base64.urlsafe_b64decode(token)
            data = json.loads(json_data)
        except Exception as e:
            return None, 'broken b64 data.'

        uid = data.get('uid', None)
        token = data.get('token', None)
        user = None

        try:
            assert uid and token and isinstance(uid, int)
        except AssertionError:
            return user, 'broken uid data.'
        
        try:
            user = User.objects.get(id=uid)
        except User.DoesNotExist:
            return user, 'user not found'

        if not default_token_generator.check_token(user, token):
            msg = "This password recovery link has expired or associated user does not exist."
            return user, msg
        
        if user and user.is_verified:
            return user, 'email already verified'
        
        return user, None


"""
@route  GET /admin/users/
@desc   View All Users or by their ID
@access Private
"""
class Users(generics.ListAPIView):
    permission_classes = (permissions.IsAuthenticated,)
    queryset = User.objects.all()
    serializer_class = UserListSerializer

    def get_queryset(self):
        qs = super().get_queryset()
        user_id = self.request.GET.get('id', None)
        if user_id is not None:
            qs = qs.filter(id=user_id)
        return qs