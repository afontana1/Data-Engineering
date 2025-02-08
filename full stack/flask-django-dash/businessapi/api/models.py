from django.db import models

# Create your models here.
class Business(models.Model):
    name = models.CharField(max_length=1000)
    no_of_employees = models.IntegerField()

    def __str__(self):
        return self.name