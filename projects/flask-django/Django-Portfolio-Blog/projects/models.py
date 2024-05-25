from django.db import models
from datetime import date

# Create your models here.
class Project(models.Model):
  title = models.CharField(max_length=100)
  description = models.TextField()
  technology = models.CharField(max_length=20)
  image = models.CharField(max_length=100)
  date_created = models.DateField(default=date.today)
  
