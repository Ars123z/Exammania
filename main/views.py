from django.shortcuts import render, redirect, get_object_or_404
from .models import Exam, Book, Chapter, Exercise, ExamQuestion
from django.contrib import messages
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from random import sample
from datetime import datetime
from django.contrib.auth.decorators import login_required
from users.models import UserProfile


@login_required
def index(request):
  return render(request, "main/index.html")
     


def book_solution(request):
  Maths_Book=Book.objects.filter(subject="math")
  Physics_Book= Book.objects.filter(subject="physics")
  Chem_Book = Book.objects.filter(subject="chemistry")
  print(Maths_Book)
  print(Physics_Book)
  print(Chem_Book)
  dic= {
    "Maths_Book":Maths_Book,
    "Physics_Book":Physics_Book,
    "Chem_Book": Chem_Book,
  }
  return render(request, "main/booklist.html", dic)

def chapterlist(request, book_name):
  book=Book.objects.get(name=book_name)
  chapters=Chapter.objects.filter(book=book)
  dic= {
    "Chapters":chapters,
    "book":book,
  }

  return render(request, "main/chapterlist.html", dic)

def exerciselist(request, book_name, chapter_name):
  book=Book.objects.get(name=book_name)
  chapter = Chapter.objects.get(book__name=book_name, name=chapter_name)
  exercises = Exercise.objects.filter(chapter=chapter)
  dic={
    "Exercises": exercises,
    "Chapter": chapter,
    "Book":book,
    "no":0
  }
  print(book.name)
  print(chapter.name)
  return render(request, "main/exerciselist.html", dic)

def exercisesolution(request, book_name, chapter_name, exercise_name, question_no):
    # Use get_object_or_404 to retrieve the specific book based on the provided book_name
    book = get_object_or_404(Book, name=book_name)
    

    # Use get_object_or_404 to retrieve the specific chapter for the given book
    chapter = get_object_or_404(Chapter, book=book, name=chapter_name)
    

    # Use get_object_or_404 to retrieve the specific exercise for the given chapter
    exercise = get_object_or_404(Exercise, chapter=chapter, name=exercise_name)
    questions = exercise.questions.all()

    
    question= questions[question_no]
    no = question_no + 1
    
    
    
    
    

    context = {
        "Book": book,
        "Chapter": chapter,
        "Exercise": exercise,
        "body": question.body,
        "answer":question.answer,
        "options":question.options.all(),
        "correct_options":question.correct_options.all(),
        "level":question.difficulty_level,
        "no":no
        
        
    }

    return render(request, "main/exercise.html", context)
  
  

def exam_solution(request, exam_name, year, question_no):
    Exam_object=Exam.objects.get(name=exam_name, year=year)
    Question=Exam_object.questions.all()
    question= Question[question_no]
    no = question_no + 1
    
    dic= {
      
      "year": year,
      "name": exam_name,
      "body": question.body,
      "answer":question.answer,
      "options":question.options.all(),
      "correct_options":question.correct_options.all(),
      "subject":question.subject,
      "level":question.difficulty_level,
      "no":no

    }
    

    return render(request, "main/exam.html", dic)


def notes(request, subject):
  if subject=="Physics":
    return render(request, "main/notes/Physics/index.html")
  
  if subject=="Chemistry":
    return render(request, "main/notes/Chemistry/index.html")
  
  if subject=="Maths":
    return render(request, "main/notes/Maths/index.html")
  
def notes_details(request, subject, topic, chapter):
   user_profile= UserProfile.objects.get(user=request.user)
   if user_profile.is_subscriber:
      timezone= user_profile.subscription_end_date.tzinfo
   if user_profile.is_subscriber and user_profile.subscription_end_date > datetime.now(timezone):
    chapter = chapter.lower().replace(" ", "_") + ".html"
    return render(request, f"main/notes/{subject}/Chapters/{topic}/{chapter}")
   else:
        return HttpResponseRedirect(reverse('join'))



def generate_test(request, subject):
    user_profile = UserProfile.objects.get(user=request.user)
    if user_profile.is_subscriber:
      timezone= user_profile.subscription_end_date.tzinfo

    if user_profile.is_subscriber and user_profile.subscription_end_date > datetime.now(timezone):
    
      if subject not in ['physics', 'chemistry', 'math']:
        return HttpResponse("Invalid subject")

    # Get all available question IDs for the chosen subject
      all_question_ids = ExamQuestion.objects.filter(subject=subject).values_list('id', flat=True)

    # Randomly select 90 question IDs for the test
      selected_question_ids = sample(list(all_question_ids), 10)
      print(selected_question_ids)

    # Redirect to the test page with the selected question IDs in the URL
      return HttpResponseRedirect(reverse('main:test_page', args=[subject, ",".join(map(str, selected_question_ids))]))
    else:
       return HttpResponseRedirect(reverse('join'))

def test_page(request, subject, question_ids):
    # Split the question_ids string into a list of integers
    question_ids = [int(id) for id in question_ids.split(',')]
    questions = ExamQuestion.objects.filter(id__in=question_ids)
    context = {
        'subject': subject,
        'question_ids': question_ids,
        'questions': questions,
    }

    return render(request, 'main/test.html', context)

def submit_test(request):
    if request.method == 'POST':
        question_ids = request.GET.get('question_ids', '')
        question_ids = [int(id) for id in question_ids.split(',')]
        # Get the submitted data from the form
        submitted_answers = {}
        for key, value in request.POST.items():
            if key.startswith('question_'):
                question_id = int(key.split('_')[1])
                submitted_answers[question_id] = int(value)

        # Now you have a dictionary with question IDs as keys and selected answer option IDs as values.
        # You can perform grading logic here.
        total_questions = 2
        print(total_questions)
        correct_answers = 0

        for question_id, selected_option_id in submitted_answers.items():
            question = ExamQuestion.objects.get(id=question_id)
            correct_option_ids = [option.id for option in question.correct_options.all()]

            if selected_option_id in correct_option_ids:
                correct_answers += 1

        # Calculate the user's score
        score = (correct_answers / total_questions) * 100

        fireworks = False
        emoji = None

        if score >= 90:
            fireworks = True
            emoji = "🎉"  # Fireworks emoji
        elif score <= 50:
            emoji = "😞"  # Sad emoji
        elif score >= 75:
            emoji = "😃"  # Happy emoji

        context = {
            'score': score,
            'fireworks': fireworks,
            'emoji': emoji,
            'question_ids': question_ids,
        }

        # You can store the test results, e.g., in a UserTestResult model if needed.

        # Display a message with the user's score
        messages.success(request, f'Your score: {score:.2f}%')


    # Redirect the user to a relevant page after submitting the test.
    return render(request,"main/result.html", context)  # Change 'home' to the URL where you want to redirect the user.




def review_test(request):
    question_ids = request.GET.get('question_ids', '').split(',')
    question_ids = [int(id) for id in question_ids]

    # Get the questions for the chosen subject along with their correct answers
    questions = ExamQuestion.objects.filter(id__in=question_ids)

    context = {
        'questions': questions,
    }

    return render(request, 'main/review_test.html', context)

