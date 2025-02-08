from django.db import models


# Create your models here.
class Joke(models.Model):
  content = models.CharField(max_length=500)
  added_at = models.DateTimeField('time published')

  # ...
  def __str__(self):
    added_at = self.added_at.strftime("%m/%d/%Y, %H:%M:%S")
    return self.content + " | " + added_at
