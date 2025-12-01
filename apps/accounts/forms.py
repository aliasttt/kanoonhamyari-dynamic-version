from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User


class CustomUserCreationForm(UserCreationForm):
    email = forms.EmailField(required=True, label='ایمیل')
    phone = forms.CharField(max_length=20, required=False, label='تلفن')
    address = forms.CharField(widget=forms.Textarea(attrs={'rows': 3}), required=False, label='آدرس')

    class Meta:
        model = User
        fields = ('username', 'email', 'phone', 'address', 'password1', 'password2')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'].widget.attrs.update({'class': 'form-control', 'placeholder': 'نام کاربری'})
        self.fields['email'].widget.attrs.update({'class': 'form-control', 'placeholder': 'ایمیل'})
        self.fields['phone'].widget.attrs.update({'class': 'form-control', 'placeholder': 'تلفن'})
        self.fields['address'].widget.attrs.update({'class': 'form-control', 'placeholder': 'آدرس'})
        self.fields['password1'].widget.attrs.update({'class': 'form-control', 'placeholder': 'رمز عبور'})
        self.fields['password2'].widget.attrs.update({'class': 'form-control', 'placeholder': 'تکرار رمز عبور'})


class CustomAuthenticationForm(AuthenticationForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'].widget.attrs.update({'class': 'form-control', 'placeholder': 'نام کاربری'})
        self.fields['password'].widget.attrs.update({'class': 'form-control', 'placeholder': 'رمز عبور'})

