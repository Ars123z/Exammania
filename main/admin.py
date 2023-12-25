from django.contrib import admin
from .models import *

# Register your models here.

class BookQuestionAdmin(admin.ModelAdmin):
    search_fields= ['body', 'answer']
    filter_horizontal= ('options', 'correct_options')

class ExerciseAdmin(admin.ModelAdmin):
    filter_horizontal= ('questions',)

class BookQuestionOptionAdmin(admin.ModelAdmin):
    search_fields= ['content']


admin.site.register(ExamQuestionOptions)
admin.site.register(ExamQuestion)
admin.site.register(Exam)

admin.site.register(BookQuestionOption, BookQuestionOptionAdmin)
admin.site.register(BookQuestion, BookQuestionAdmin)
admin.site.register(Exercise, ExerciseAdmin)
admin.site.register(Chapter)
admin.site.register(Book)