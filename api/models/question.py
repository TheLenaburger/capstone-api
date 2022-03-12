from django.db import models
from django.contrib.auth import get_user_model

class Question(models.Model):
  title = models.CharField(max_length=150)
  body = models.TextField()
  owner = models.ForeignKey(get_user_model(), on_delete=models.CASCADE, related_name='questions')

  def __str__(self):
    return f"Title: {self.title} Body: {self.body}"
