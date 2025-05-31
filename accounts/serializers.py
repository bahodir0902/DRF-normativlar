from rest_framework import serializers
from rest_framework.exceptions import ValidationError
from accounts.models import User, Profile
from django.contrib.auth import authenticate
from accounts.utils import generate_random_username

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'first_name', 'last_name', 'email', 'date_joined', 'password']
        extra_kwargs = {
            'id': {'read_only': True},
            'date_joined': {'read_only': True},
            'password': {'write_only': True}
        }

    def update(self, instance, validated_data):
        instance.email = validated_data.get('email', instance.email)
        password = validated_data.get('password', None)
        if password:
            instance.set_password(password)
        instance.save()
        return instance

class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = ['bio', 'address']


class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(max_length=255)

    def validate(self, attrs):
        email = attrs.get('email')
        password = attrs.get('password')

        if not User.objects.filter(email=email).exists():
            raise ValidationError(f"User with {email} email not found.")

        user = authenticate(email=email, password=password)

        if not user:
            raise ValidationError("Email or password is incorrect")

        return user

class RegisterUserSerializer(serializers.ModelSerializer):
    re_password = serializers.CharField(max_length=255, write_only=True)
    profile = ProfileSerializer(required=False)
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email', 'profile', 'password', 're_password']
        extra_kwargs = {
            'password': {'write_only': True}
        }

    def validate(self, attrs):
        password = attrs.get('password')
        re_password = attrs.get('re_password')
        email = attrs.get("email")

        if not password or not re_password:
            raise ValidationError("Password are not entered!")

        if str(password) != str(re_password):
            raise ValidationError("Passwords doesn\'t match")

        if User.objects.filter(email=email).exists():
            raise ValidationError(f"User with {email} already exists in database!")

        return attrs

    def create(self, validated_data):
        re_password = validated_data.pop("re_password")

        profile_data = validated_data.pop('profile', None)

        user =User.objects.create_user(
            username=generate_random_username(),
            **validated_data
        )

        if profile_data:
            Profile.objects.create(
                user=user,
                **profile_data
            )

        return user



