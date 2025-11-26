# Create your models here.
from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator, MaxValueValidator

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    english_level = models.PositiveIntegerField(
        validators=[MinValueValidator(0), MaxValueValidator(5)],
        null=True,
        blank=True,
        default=None
    )