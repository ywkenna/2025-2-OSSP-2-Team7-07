from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Profile

class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = ["english_level"]


class UserPublicSerializer(serializers.ModelSerializer):
    english_level = serializers.CharField(source="profile.english_level", read_only=True)
    like_movies = serializers.PrimaryKeyRelatedField(
        many=True,
        read_only=True,
        source="profile.like_movies"
    )

    class Meta:
        model = User
        fields = ["id", "username", "email", "first_name", "last_name", "english_level", "like_movies"]

class RegisterSerializer(serializers.ModelSerializer):
    english_level = serializers.IntegerField(
        required=False, 
        allow_null = True,
    )
    password = serializers.CharField(write_only=True, min_length=8)

    class Meta:
        model = User
        fields = ["username", "password", "email", "first_name", "english_level"]

    def create(self, validated_data):
        password = validated_data.pop("password")

        user = User(
            username=validated_data["username"],
            email=validated_data.get("email", ""),
            first_name=validated_data.pop("first_name"),
            last_name=""
        )
        user.set_password(password)
        user.save()

        profile = user.profile
        profile.english_level = validated_data.get("english_level", None)
        profile.save()

        return user

