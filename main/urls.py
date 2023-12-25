from django.urls import path
from . import views



app_name = "main"

urlpatterns = [
    path("", views.index, name="index"),
    path("book-solution/", views.book_solution, name="book_solution"),
    path("chapter-list/<str:book_name>/", views.chapterlist, name="chapter_list"),
    path("exercise-list/<str:book_name>/<str:chapter_name>/", views.exerciselist, name="exercise_list"),
    path("exercise-solution/<str:book_name>/<str:chapter_name>/<str:exercise_name>/<int:question_no>", views.exercisesolution, name="exercise_solution"),
    path("exam-solution/<str:exam_name>/<int:year>/<int:question_no>/", views.exam_solution, name="exam_solution"),
    path("notes/<str:subject>/", views.notes, name="notes"),
    path("notes-detailes/<str:subject>/<str:topic>/<str:chapter>/", views.notes_details, name="notes_details"),
    path('generate-test/<str:subject>/', views.generate_test, name='generate_test'),
    path('test/<str:subject>/<str:question_ids>/', views.test_page, name='test_page'),
    path('submit-test/',views.submit_test, name='submit_test'),
    path('review-test/', views.review_test, name="review_test")
]


