from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from .models import UserProfile


class SignupForm(UserCreationForm):
    email = forms.EmailField(required=True)
    phone = forms.CharField(required=False, max_length=20)
    address = forms.CharField(required=False, max_length=255)

    class Meta:
        model = User
        fields = ("username", "email", "password1", "password2", "phone", "address")

    def save(self, commit=True):
        user = super().save(commit)
        if commit:
            email = self.cleaned_data.get('email')
            phone = self.cleaned_data.get('phone')
            address = self.cleaned_data.get('address')
            if email:
                user.email = email
                user.save(update_fields=['email'])
            UserProfile.objects.create(user=user, phone=phone or '', address=address or '')
        return user


class LoginForm(AuthenticationForm):
    username = forms.CharField(label='نام کاربری')
    password = forms.CharField(widget=forms.PasswordInput, label='رمز عبور')





