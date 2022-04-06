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


class AuthSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username', 'email', 'role')


class RegistrationSerializer(serializers.Serializer):
    first_name = serializers.CharField()
    middle_name = serializers.CharField(required=False)
    last_name = serializers.CharField()
    email = serializers.EmailField()
    role = serializers.CharField()
    password = serializers.CharField(write_only=True, style={'input_type': 'password'})

    def validate(self, data):
        if User.objects.filter(email=data['email']).exists():
            raise serializers.ValidationError(
                {"email": "email already in use"})

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
