from django.db import models

# Create your models here.

class ExamQuestionOptions(models.Model):
    content= models.TextField(unique=True)
    def __str__(self):
        return self.content
    
    

class ExamQuestion(models.Model):
    DIFFICULTY_CHOICES = (
        ('easy', 'Easy'),
        ('medium', 'Medium'),
        ('hard', 'Hard'),
    )
    SUBJECT_CHOICES=(
        ('physics', 'Physics'),
        ('chemistry', 'Chemistry'),
        ('math', 'Math'),
    )
    body= models.TextField(unique=True)
    answer= models.TextField(default=None)
    options= models.ManyToManyField(ExamQuestionOptions, related_name="options")
    correct_options = models.ManyToManyField(ExamQuestionOptions, related_name="correct_options")
    subject= models.CharField(max_length=25, choices=SUBJECT_CHOICES, default='physics')
    difficulty_level= models.CharField(max_length=20, choices=DIFFICULTY_CHOICES, default='medium')

    def __str__(self):
        return self.body


class Exam(models.Model):
    
    name= models.CharField(max_length=25)
    year= models.IntegerField()
    questions = models.ManyToManyField(ExamQuestion, related_name='Exams', blank=True)
    def __str__(self):
        return f"{self.name}-{self.year}"
    class Meta:
        ordering = ['name', 'year']

class BookQuestionOption(models.Model):
    content= models.TextField(unique=True)
    def __str__(self):
        return self.content   

class BookQuestion(models.Model):
    DIFFICULTY_CHOICES = (
        ('easy', 'Easy'),
        ('medium', 'Medium'),
        ('hard', 'Hard'),
    )
    
    body= models.TextField(unique=True)
    answer= models.TextField(default=None)
    options= models.ManyToManyField(BookQuestionOption, related_name="options")
    correct_options = models.ManyToManyField(BookQuestionOption, related_name="correct_options")
    difficulty_level= models.CharField(max_length=20, choices=DIFFICULTY_CHOICES, default='medium')

    def __str__(self):
        return self.body

class Book(models.Model):
    name= models.CharField(max_length=250)
    SUBJECT_CHOICES=(
        ('physics', 'Physics'),
        ('chemistry', 'Chemistry'),
        ('math', 'Math'),
    )
    subject= models.CharField(max_length=100, choices=SUBJECT_CHOICES)
    image= models.ImageField(upload_to="images/")

    def __str__(self):
        return self.name


class Chapter(models.Model):
    name= models.CharField(max_length=250)
    book= models.ForeignKey(Book, related_name="chapters", on_delete=models.CASCADE)
    def __str__(self):
        return self.name


class Exercise(models.Model):
    name= models.CharField(max_length=250)
    questions= models.ManyToManyField(BookQuestion, related_name="Exercises")
    chapter= models.ForeignKey(Chapter, related_name="exercises", on_delete=models.CASCADE)

    def __str__(self):
        return self.name


    


    











