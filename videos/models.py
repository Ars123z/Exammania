from django.db import models

# Create your models here
# models.py


class Subject(models.Model):
    name = models.CharField(max_length=100)
    def __str__(self):
        return self.name

class Topic(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField()
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE)
    def __str__(self):
        return self.title
    
class Video(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField()
    video_id = models.CharField(max_length=20)
    order = models.IntegerField()
    topic = models.ForeignKey(Topic, on_delete=models.CASCADE)
    code = models.CharField(max_length=10, default="MEC-1")
    def __str__(self):
        return self.title
