from django.db import models
from django.conf import settings

# Create your models here.
class News(models.Model):
    title = models.CharField(max_length=10000)
    description = models.CharField(max_length=10000)
    image_url = models.CharField(max_length=10000)
    link = models.CharField(max_length=10000)
    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
    )