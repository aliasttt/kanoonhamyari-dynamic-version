from django import forms
from .models import LegalInquiry


class LegalInquiryForm(forms.ModelForm):
    class Meta:
        model = LegalInquiry
        fields = ['name', 'phone', 'email', 'message']
        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'نام و نام خانوادگی'
            }),
            'phone': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'شماره تماس'
            }),
            'email': forms.EmailInput(attrs={
                'class': 'form-control',
                'placeholder': 'ایمیل (اختیاری)'
            }),
            'message': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 4,
                'placeholder': 'پیام یا توضیحات (اختیاری)'
            }),
        }
        labels = {
            'name': 'نام و نام خانوادگی',
            'phone': 'شماره تماس',
            'email': 'ایمیل',
            'message': 'پیام',
        }




