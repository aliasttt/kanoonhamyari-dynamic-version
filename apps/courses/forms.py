from django import forms
from .models import QuizOption


class InitialForm(forms.Form):
    full_name = forms.CharField(max_length=200, label='نام و نام خانوادگی')
    phone = forms.CharField(max_length=20, label='شماره تماس')
    city = forms.CharField(max_length=100, required=False, label='شهر')


class QuizForm(forms.Form):
    # will be generated dynamically in the view per question
    pass


class QuizAnswerForm(forms.Form):
    """فرم پاسخ به یک سوال"""
    option_id = forms.IntegerField(required=True, widget=forms.HiddenInput())
    
    def __init__(self, question, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.question = question
        options = question.options.all()
        self.fields['option_id'].widget = forms.RadioSelect(
            choices=[(opt.id, opt.text) for opt in options],
            attrs={'class': 'quiz-option-radio'}
        )
