# Create your models here.
from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator, MaxValueValidator
from movies.models import MovieData

TAGS = [
    "액션/스릴러", "드라마/감성", "SF/판타지", "코미디",
    "역사/전쟁", "애니메이션", "기타",
]

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    english_level = models.PositiveIntegerField(
        validators=[MinValueValidator(0), MaxValueValidator(5)],
        null=True,
        default=None
    )
    like_movies = models.ManyToManyField(
        MovieData,
        blank=True,
        related_name='liked_users'
    )
    like_tags = models.JSONField(default=list, blank=True)