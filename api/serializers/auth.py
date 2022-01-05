from rest_framework import serializers
from api.models import User, Tutor


class AuthSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username', 'email', 'role')


class RegistrationSerializer(serializers.Serializer):
    first_name = serializers.CharField()
    middle_name = serializers.CharField(required=False)
    last_name = serializers.CharField()
    email = serializers.EmailField()
    birth_date = serializers.DateField()
    role = serializers.CharField()

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

        if validated_data['role'] == 'tutor':
            Tutor.objects.create(user=user)
        else:
            # TODO - Create Tutee
            return user

        return user
