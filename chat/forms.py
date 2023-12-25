# forms.py
from django import forms
from .models import ChatQuestion
class QuestionForm(forms.ModelForm):
    class Meta:
        model = ChatQuestion
        fields = ['question_text']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['question_text'].widget.attrs['class'] = 'latex-input'

class AnswerForm(forms.ModelForm):
    class Meta:
        model = ChatQuestion
        fields = ['answer_text']
