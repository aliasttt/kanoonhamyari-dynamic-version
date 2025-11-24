from django import forms
from .models import Enrollment


class InitialForm(forms.Form):
    full_name = forms.CharField(max_length=200, label='نام و نام خانوادگی')
    phone = forms.CharField(max_length=20, label='شماره تماس')
    city = forms.CharField(max_length=100, required=False, label='شهر')


class QuizForm(forms.Form):
    # will be generated dynamically in the view per question
    pass





