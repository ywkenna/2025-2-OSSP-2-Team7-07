from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Profile


# ------------------------------------------------
# 프로필 Serializer
# ------------------------------------------------
class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = ["english_level"]


# ------------------------------------------------
# 사용자 공개 정보 Serializer
# (로그인 후 userinfo 에서 사용하는 형태)
# ------------------------------------------------
class UserPublicSerializer(serializers.ModelSerializer):
    english_level = serializers.CharField(source="profile.english_level", read_only=True)
    like_movies = serializers.PrimaryKeyRelatedField(
        many=True,
        read_only=True,
        source="profile.like_movies"
    )
    like_tags = serializers.ListField(
        source="profile.like_tags",
        child=serializers.CharField(),
        read_only=True
    )
    profile_image = serializers.SerializerMethodField()

    def get_profile_image(self, obj):
        if obj.profile.profile_image:
            return obj.profile.profile_image.url
        return None

    class Meta:
        model = User
        fields = [
            "id",
            "username",
            "email",
            "first_name",
            "last_name",
            "english_level",
            "like_movies",
            "like_tags",
            "profile_image",
        ]


# ------------------------------------------------
# 회원가입 Serializer
# ------------------------------------------------
class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, min_length=1)
    english_level = serializers.IntegerField(required=False, allow_null=True)

    class Meta:
        model = User
        fields = ["username", "password", "email", "english_level"]

    def create(self, validated_data):
        password = validated_data.pop("password")
        english_level = validated_data.pop("english_level", None)

        # User 생성
        user = User(
            username=validated_data.get("username"),
            email=validated_data.get("email", "")
        )
        user.set_password(password)
        user.save()

        # Profile 생성 및 english_level 저장
        profile = user.profile
        profile.english_level = english_level
        profile.save()

        return user
