from rest_framework import serializers
from django.contrib.auth.password_validation import validate_password
from .models import Student
from django.contrib.auth import get_user_model

User = get_user_model()

class AuthorSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['moodleID', 'username', 'first_name', 'last_name', 'email']

class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=True, validators=[validate_password])
    password2 = serializers.CharField(write_only=True, required=True)

    class Meta:
        model = Student
        fields = ('moodleID', 'email', 'username', 'profile_image',
                  'password', 'password2','first_name', 'last_name')
        extra_kwargs = {
            'profile_image': {'required': False},
        }

    def validcate(self, data):
        if data.get("password") != data.get("password2"):
            raise serializers.ValidationError({"password": "Passwords do not match."})
        return data

    def create(self, validated_data):
        validated_data.pop('password2')
        user = Student.objects.create_user(
            email=validated_data['email'],
            username=validated_data['username'],
            password=validated_data['password'],
            profile_image=validated_data.get('profile_image'),
        )
        return user

class UserUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Student
        fields = ['first_name', 'last_name', 'email', 'profile_image', 'phone_number']

class Profile(serializers.ModelSerializer):

    class Meta:
        model = Student
        fields = ['first_name', 'last_name', 'username', 'email', 'profile_image', 'phone_number']

