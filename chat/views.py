# views.py
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.urls import reverse
from .models import ChatQuestion
from .forms import QuestionForm
from datetime import datetime
from django.http import HttpResponseRedirect,HttpResponseForbidden
from users.models import UserProfile

@login_required
def ask_question(request):
    if request.method == 'POST':
        form = QuestionForm(request.POST)
        if form.is_valid():
            question = form.save(commit=False)
            question.user = request.user
            question.save()
            return redirect('question_list')
    else:
        form = QuestionForm()
    return render(request, 'chat/ask_question.html', {'form': form})

@login_required
def question_list(request):
    user_profile= UserProfile.objects.get(user=request.user)
    if user_profile.is_subscriber:
      timezone= user_profile.subscription_end_date.tzinfo
    if user_profile.is_subscriber and user_profile.subscription_end_date > datetime.now(timezone):
        if request.user.is_staff:
            questions = ChatQuestion.objects.all()
        else:
            questions = ChatQuestion.objects.filter(user=request.user)
        return render(request, 'chat/question_list.html', {'questions': questions})
    else:
        return HttpResponseRedirect(reverse('join'))

@login_required
def answer_question(request, question_id):
    question = get_object_or_404(ChatQuestion, id=question_id)

    if request.method == 'POST':
        answer_text = request.POST.get('answer_text')
        question.answer_text = answer_text
        question.is_answered = True
        question.save()

        return redirect('question_list')

    return render(request, 'chat/answer_question.html', {'question': question})

from .forms import QuestionForm, AnswerForm

def edit_question(request, question_id):
    question = get_object_or_404(ChatQuestion, id=question_id)

    if request.method == 'POST':
        form = QuestionForm(request.POST, instance=question)
        if form.is_valid():
            form.save()
            return redirect('question_list')
    else:
        form = QuestionForm(instance=question)

    return render(request, 'chat/edit_question.html', {'form': form, 'question': question})

def delete_question(request, question_id):
    question = get_object_or_404(ChatQuestion, id=question_id)

    if request.method == 'POST':
        question.delete()
        return redirect('question_list')

    return render(request, 'chat/delete_question.html', {'question': question})

def edit_answer(request, question_id):
    question = get_object_or_404(ChatQuestion, id=question_id)

    if request.method == 'POST':
        form = AnswerForm(request.POST, instance=question)
        if form.is_valid():
            form.save()
            return redirect('question_list')
    else:
        form = AnswerForm(instance=question)

    return render(request, 'chat/edit_answer.html', {'form': form, 'question': question})


def staff_unanswered_questions(request):
    if not request.user.is_staff:
        return HttpResponseForbidden("You don't have permission to access this page.")

    unanswered_questions = ChatQuestion.objects.filter(is_answered=False)

    return render(request, 'chat/unanswered_questions.html', {'unanswered_questions': unanswered_questions})