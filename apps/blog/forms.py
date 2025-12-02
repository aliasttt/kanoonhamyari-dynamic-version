from django import forms
from .models import BlogComment, NewsletterSubscriber, Tag


class BlogCommentForm(forms.ModelForm):
    class Meta:
        model = BlogComment
        fields = ['name', 'email', 'content']
        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'نام و نام خانوادگی'
            }),
            'email': forms.EmailInput(attrs={
                'class': 'form-control',
                'placeholder': 'ایمیل (اختیاری)'
            }),
            'content': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 4,
                'placeholder': 'نظر شما...'
            }),
        }
        labels = {
            'name': 'نام و نام خانوادگی',
            'email': 'ایمیل',
            'content': 'نظر',
        }


class NewsletterSubscribeForm(forms.ModelForm):
    """فرم اشتراک در خبرنامه"""
    tags = forms.ModelMultipleChoiceField(
        queryset=Tag.objects.all(),
        widget=forms.CheckboxSelectMultiple(attrs={'class': 'tag-checkboxes'}),
        required=False,
        label='دسته‌بندی‌های مورد علاقه'
    )
    
    class Meta:
        model = NewsletterSubscriber
        fields = ['email', 'name', 'tags']
        widgets = {
            'email': forms.EmailInput(attrs={
                'class': 'form-control',
                'placeholder': 'ایمیل شما',
                'required': True
            }),
            'name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'نام شما (اختیاری)'
            }),
        }
        labels = {
            'email': 'ایمیل',
            'name': 'نام',
            'tags': 'دسته‌بندی‌های مورد علاقه',
        }
    
    def clean_email(self):
        email = self.cleaned_data.get('email')
        if NewsletterSubscriber.objects.filter(email=email, is_active=True).exists():
            raise forms.ValidationError('این ایمیل قبلاً ثبت شده است.')
        return email
