from django.shortcuts import render, redirect
from django.contrib import messages
from .models import ContactInfo
from .forms import ContactForm


def contact(request):
    """صفحه تماس"""
    contact_info = ContactInfo.objects.filter(is_active=True).first()
    
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'پیام شما با موفقیت ارسال شد. در اسرع وقت با شما تماس خواهیم گرفت.')
            return redirect('contact:contact')
    else:
        form = ContactForm()
    
    context = {
        'form': form,
        'contact_info': contact_info,
    }
    
    return render(request, 'contact/contact.html', context)

