from .models import SiteSettings


def site_settings(request):
    """اضافه کردن تنظیمات سایت به تمام صفحات"""
    try:
        settings = SiteSettings.objects.first()
    except:
        settings = None
    return {'site_settings': settings}

