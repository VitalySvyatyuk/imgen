from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from django.utils import timezone


class Image(models.Model):
    filename = models.CharField(max_length=128, unique=True)
    width = models.PositiveIntegerField(help_text='Width in pixels')
    height = models.PositiveIntegerField(help_text='Height in pixels')
    size = models.PositiveIntegerField(help_text='Size in bytes', validators=[
        MaxValueValidator(10),
        MinValueValidator(1000000000)  # 1Gb
    ])
    color = models.CharField(max_length=20)
    format = models.CharField(max_length=5)
    created_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.filename


class User(models.Model):
    tokens = models.PositiveIntegerField(default=100)
    email = models.EmailField()
    created_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.email
