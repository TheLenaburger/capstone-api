from django.db import models
from django.contrib.auth import get_user_model

class Answer(models.Model):
  body = models.TextField
  question = models.ForeignKey('Question', on_delete=models.CASCADE, related_name='answers')
  owner = models.ForeignKey(get_user_model(), on_delete=models.CASCADE, related_name='answers')
