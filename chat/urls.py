# urls.py
from django.urls import path
from .views import ask_question, question_list, answer_question, edit_question, edit_answer, delete_question, staff_unanswered_questions

urlpatterns = [
    path('ask/', ask_question, name='ask_question'),
    path('questions/', question_list, name='question_list'),
    path('answer/<int:question_id>/', answer_question, name='answer_question'),
    path('edit/<int:question_id>/', edit_question, name='edit_question'),
    path('delete/<int:question_id>/', delete_question, name='delete_question'),
    path('edit_answer/<int:question_id>/', edit_answer, name='edit_answer'),
    path('staff/unanswered/', staff_unanswered_questions, name='staff_unanswered_questions'),
]
