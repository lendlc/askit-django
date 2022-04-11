from datetime import datetime
from django.shortcuts import get_object_or_404
from rest_framework import serializers
from api.models import User, Tutor
from django.contrib.auth import authenticate


class LoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField(style={'input_type': 'password'})

    def _validate_username(self, username, password):
        user = None
        if username and password:
            q_user = User.objects.filter(email=username)

            if q_user.exists():
                user = authenticate(username=q_user.first().username, password=password)
        else:
            raise serializers.ValidationError('must include email and password')

        return user

    def validate(self, data):
        username = data.get('username', None)
        password = data.get('password', None)

        user = None

        if username:
            user = self._validate_username(username, password)

            # if user:
            if not user:
                raise serializers.ValidationError('unable to login with provided credentials')

        data['user'] = user
        return data


class RegistrationSerializer(serializers.Serializer):
    first_name = serializers.CharField()
    middle_name = serializers.CharField(required=False)
    last_name = serializers.CharField()
    email = serializers.EmailField()
    role = serializers.CharField()
    password = serializers.CharField(write_only=True, style={'input_type': 'password'})

    def validate(self, data):
        if User.objects.filter(email=data['email']).exists():
            raise serializers.ValidationError({"email": "email already in use"})

        if data['role'] not in ['tutor', 'tutee']:
            raise serializers.ValidationError({"role": "invalid role"})

        data['username'] = data['email'].split("@")[0]

        return data

    def create(self, validated_data):
        user = User.objects.create(**validated_data)
        user.set_password(validated_data.get('password'))
        user.save()

        if validated_data['role'] == 'tutor':
            Tutor.objects.create(user=user)
        else:
            # TODO - Create Tutee
            return user

        return user


class ChangePasswordSerializer(serializers.Serializer):
    old_password = serializers.CharField(required=True)
    new_password = serializers.CharField(required=True)
    new_password_2 = serializers.CharField(required=True)

    def validate(self, data):
        user = self.context['request'].user

        # check if old_password is valid
        if not user.check_password(data.get('old_password')):
            raise serializers.ValidationError({"old_password": "invalid password"})

        # check if new password matches
        if not data.get('new_password') == data.get('new_password_2'):
            raise serializers.ValidationError({"new_password": "new password mismatch"})

        return data

class ResetPasswordSerializer(serializers.Serializer):
    email = serializers.CharField()
    code = serializers.CharField(required=True)
    new_password = serializers.CharField()
    new_password_2 = serializers.CharField()
    
    def validate(self, data):
        user = get_object_or_404(User, email=data.get('email', None))
        
        if not user.reset_pw_code and not user.reset_pw_exp:
            raise serializers.ValidationError({'code': 'no existing code, please request a new one'})
        elif user.reset_pw_code == data.get('code').upper():
            raise serializers.ValidationError({'code': 'invalid code.'})
        elif datetime.now() > user.reset_pw_exp:
            raise serializers.ValidationError({'code': 'code expired, please request a new one.'})
        
        if not data.get('new_password') == data.get('new_password_2'):
            raise serializers.ValidationError({'password': 'password mismatch.'})
        
        return data

class UserListSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username', 'email', 'role')
