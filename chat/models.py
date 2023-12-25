# models.py
from django.db import models
from django.contrib.auth.models import User

class ChatQuestion(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    question_text = models.TextField()
    answer_text = models.TextField(blank=True, null=True)
    is_answered = models.BooleanField(default=False)

    def __str__(self):
        return self.question_text

