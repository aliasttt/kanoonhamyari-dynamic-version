from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from .models import UserProfile


class CustomUserCreationForm(UserCreationForm):
    email = forms.EmailField(required=True, label='ایمیل')
    
    # اطلاعات شخصی
    first_name = forms.CharField(max_length=100, required=True, label='نام')
    last_name = forms.CharField(max_length=100, required=True, label='نام خانوادگی')
    gender = forms.ChoiceField(
        choices=UserProfile.GENDER_CHOICES,
        required=False,
        label='جنسیت',
        widget=forms.Select(attrs={'class': 'form-control'})
    )
    birth_date = forms.DateField(
        required=False,
        label='تاریخ تولد',
        widget=forms.DateInput(attrs={'type': 'date', 'class': 'form-control'})
    )
    mobile = forms.CharField(max_length=20, required=True, label='شماره موبایل')
    
    # اطلاعات آدرس
    country = forms.CharField(max_length=100, required=False, label='کشور')
    city = forms.CharField(max_length=100, required=False, label='شهر')
    district = forms.CharField(max_length=100, required=False, label='منطقه/محله')
    full_address = forms.CharField(
        widget=forms.Textarea(attrs={'rows': 3}),
        required=False,
        label='آدرس کامل'
    )
    postal_code = forms.CharField(max_length=20, required=False, label='کد پستی')
    landline = forms.CharField(max_length=20, required=False, label='شماره تلفن ثابت (اختیاری)')
    
    # اطلاعات شغلی
    current_job = forms.CharField(max_length=200, required=False, label='شغل فعلی')
    field_of_activity = forms.CharField(max_length=200, required=False, label='زمینه فعالیت')
    company_name = forms.CharField(max_length=200, required=False, label='نام شرکت')
    job_position = forms.CharField(max_length=200, required=False, label='سمت شغلی')
    years_of_experience = forms.IntegerField(required=False, label='سال‌های تجربه')
    website = forms.URLField(required=False, label='وب‌سایت شخصی یا کاری')
    linkedin = forms.URLField(required=False, label='لینکدین')
    instagram = forms.CharField(max_length=200, required=False, label='اینستاگرام / شبکه‌های اجتماعی')
    
    # اطلاعات تحصیلی
    education_level = forms.ChoiceField(
        choices=UserProfile.EDUCATION_CHOICES,
        required=False,
        label='آخرین مدرک تحصیلی',
        widget=forms.Select(attrs={'class': 'form-control'})
    )
    field_of_study = forms.CharField(max_length=200, required=False, label='رشته')
    university = forms.CharField(max_length=200, required=False, label='دانشگاه / موسسه')
    graduation_year = forms.IntegerField(required=False, label='سال فارغ‌التحصیلی')
    
    # ترجیحات
    favorite_categories = forms.CharField(
        max_length=500,
        required=False,
        label='دسته‌بندی‌های مورد علاقه',
        widget=forms.Textarea(attrs={'rows': 2})
    )
    preferred_content_type = forms.ChoiceField(
        choices=UserProfile.CONTENT_TYPE_CHOICES,
        required=False,
        label='نوع محتوای مورد علاقه',
        widget=forms.Select(attrs={'class': 'form-control'})
    )
    preferred_message_hours = forms.CharField(max_length=100, required=False, label='ساعات ترجیحی دریافت پیام‌ها')
    followed_topics = forms.CharField(
        required=False,
        label='انتخاب موضوعاتی که دنبال می‌کند',
        widget=forms.Textarea(attrs={'rows': 3})
    )
    how_did_you_hear = forms.CharField(max_length=200, required=False, label='نحوه آشنایی با سایت')
    
    # قبول قوانین
    terms_accepted = forms.BooleanField(required=True, label='قبول قوانین و حریم خصوصی')

    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # استایل فیلدهای User
        self.fields['username'].widget.attrs.update({'class': 'form-control', 'placeholder': 'نام کاربری'})
        self.fields['email'].widget.attrs.update({'class': 'form-control', 'placeholder': 'ایمیل'})
        self.fields['password1'].widget.attrs.update({'class': 'form-control', 'placeholder': 'رمز عبور'})
        self.fields['password2'].widget.attrs.update({'class': 'form-control', 'placeholder': 'تکرار رمز عبور'})
        
        # استایل فیلدهای Profile
        for field_name, field in self.fields.items():
            if field_name not in ['username', 'email', 'password1', 'password2', 'gender', 'birth_date', 'education_level', 'preferred_content_type', 'terms_accepted']:
                if isinstance(field.widget, forms.Textarea):
                    field.widget.attrs.update({'class': 'form-control'})
                elif not isinstance(field.widget, (forms.Select, forms.CheckboxInput)):
                    field.widget.attrs.update({'class': 'form-control'})
    
    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data['email']
        user.first_name = self.cleaned_data.get('first_name', '')
        user.last_name = self.cleaned_data.get('last_name', '')
        
        if commit:
            user.save()
            profile, created = UserProfile.objects.get_or_create(user=user)
            
            # ذخیره اطلاعات پروفایل
            profile.first_name = self.cleaned_data.get('first_name', '')
            profile.last_name = self.cleaned_data.get('last_name', '')
            profile.gender = self.cleaned_data.get('gender', '')
            profile.birth_date = self.cleaned_data.get('birth_date')
            profile.mobile = self.cleaned_data.get('mobile', '')
            profile.country = self.cleaned_data.get('country', '')
            profile.city = self.cleaned_data.get('city', '')
            profile.district = self.cleaned_data.get('district', '')
            profile.full_address = self.cleaned_data.get('full_address', '')
            profile.postal_code = self.cleaned_data.get('postal_code', '')
            profile.landline = self.cleaned_data.get('landline', '')
            profile.current_job = self.cleaned_data.get('current_job', '')
            profile.field_of_activity = self.cleaned_data.get('field_of_activity', '')
            profile.company_name = self.cleaned_data.get('company_name', '')
            profile.job_position = self.cleaned_data.get('job_position', '')
            profile.years_of_experience = self.cleaned_data.get('years_of_experience')
            profile.website = self.cleaned_data.get('website', '')
            profile.linkedin = self.cleaned_data.get('linkedin', '')
            profile.instagram = self.cleaned_data.get('instagram', '')
            profile.education_level = self.cleaned_data.get('education_level', '')
            profile.field_of_study = self.cleaned_data.get('field_of_study', '')
            profile.university = self.cleaned_data.get('university', '')
            profile.graduation_year = self.cleaned_data.get('graduation_year')
            profile.favorite_categories = self.cleaned_data.get('favorite_categories', '')
            profile.preferred_content_type = self.cleaned_data.get('preferred_content_type', '')
            profile.preferred_message_hours = self.cleaned_data.get('preferred_message_hours', '')
            profile.followed_topics = self.cleaned_data.get('followed_topics', '')
            profile.how_did_you_hear = self.cleaned_data.get('how_did_you_hear', '')
            profile.terms_accepted = self.cleaned_data.get('terms_accepted', False)
            profile.save()
        
        return user


class CustomAuthenticationForm(AuthenticationForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'].widget.attrs.update({'class': 'form-control', 'placeholder': 'نام کاربری'})
        self.fields['password'].widget.attrs.update({'class': 'form-control', 'placeholder': 'رمز عبور'})

