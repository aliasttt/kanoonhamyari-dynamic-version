from django.core.management.base import BaseCommand
from apps.services.models import University


class Command(BaseCommand):
    help = 'ایجاد یک دانشگاه نمونه برای تست'

    def handle(self, *args, **options):
        # بررسی اینکه آیا دانشگاه نمونه وجود دارد
        if University.objects.filter(slug='istanbul-universitesi').exists():
            self.stdout.write(self.style.WARNING('دانشگاه نمونه قبلاً ایجاد شده است.'))
            return

        university = University.objects.create(
            name='دانشگاه استانبول',
            slug='istanbul-universitesi',
            short_description='دانشگاه استانبول یکی از قدیمی‌ترین و معتبرترین دانشگاه‌های دولتی ترکیه است که در سال 1453 تأسیس شده است.',
            description='''
            <h3>درباره دانشگاه استانبول</h3>
            <p>دانشگاه استانبول (Istanbul Üniversitesi) یکی از قدیمی‌ترین و معتبرترین دانشگاه‌های ترکیه است که در سال 1453 میلادی تأسیس شده است. این دانشگاه با بیش از 500 سال سابقه، یکی از برترین مراکز آموزشی و تحقیقاتی در منطقه محسوب می‌شود.</p>
            
            <h4>ویژگی‌های برجسته:</h4>
            <ul>
                <li>رتبه برتر در بین دانشگاه‌های ترکیه</li>
                <li>امکانات آموزشی و تحقیقاتی پیشرفته</li>
                <li>کتابخانه‌های غنی با بیش از 2 میلیون جلد کتاب</li>
                <li>پردیس‌های متعدد در نقاط مختلف استانبول</li>
                <li>همکاری با دانشگاه‌های معتبر بین‌المللی</li>
            </ul>
            
            <h4>زندگی دانشجویی:</h4>
            <p>دانشگاه استانبول امکانات رفاهی مناسبی برای دانشجویان بین‌المللی فراهم می‌کند، از جمله خوابگاه‌های دانشجویی، کافه‌تریا، سالن‌های ورزشی و مراکز فرهنگی.</p>
            ''',
            university_type='public',
            location='استانبول، ترکیه',
            language='ترکی، انگلیسی',
            ranking='رتبه 1-5 در ترکیه',
            price=15000,
            price_note='قیمت برای هر ترم تحصیلی (شهریه سالانه حدود 30,000 لیر)',
            programs='''
            <h4>رشته‌های تحصیلی موجود:</h4>
            <ul>
                <li><strong>مهندسی:</strong> کامپیوتر، برق، مکانیک، عمران</li>
                <li><strong>پزشکی:</strong> پزشکی عمومی، دندانپزشکی، داروسازی</li>
                <li><strong>علوم انسانی:</strong> حقوق، اقتصاد، مدیریت، روانشناسی</li>
                <li><strong>علوم پایه:</strong> ریاضی، فیزیک، شیمی، زیست‌شناسی</li>
                <li><strong>هنر:</strong> معماری، طراحی، موسیقی</li>
            </ul>
            ''',
            admission_requirements='''
            <h4>شرایط پذیرش:</h4>
            <ul>
                <li>دیپلم دبیرستان با معدل حداقل 15</li>
                <li>گذراندن آزمون YÖS یا SAT</li>
                <li>مدرک زبان ترکی (TÖMER) یا انگلیسی (TOEFL/IELTS)</li>
                <li>ترجمه رسمی مدارک تحصیلی</li>
                <li>گواهی سلامت</li>
                <li>عکس پرسنلی</li>
            </ul>
            <p><strong>مهلت ثبت‌نام:</strong> معمولاً از اردیبهشت تا تیرماه هر سال</p>
            ''',
            scholarship_info='''
            <h4>بورسیه‌های موجود:</h4>
            <ul>
                <li><strong>بورسیه دولتی ترکیه (Türkiye Bursları):</strong> شامل شهریه، خوابگاه و کمک هزینه ماهانه</li>
                <li><strong>بورسیه دانشگاه:</strong> برای دانشجویان ممتاز</li>
                <li><strong>بورسیه تحقیقاتی:</strong> برای دانشجویان کارشناسی ارشد و دکتری</li>
            </ul>
            <p>برای اطلاعات بیشتر در مورد بورسیه‌ها با ما تماس بگیرید.</p>
            ''',
            is_active=True,
            is_featured=True,
            order=1
        )

        self.stdout.write(self.style.SUCCESS(f'دانشگاه نمونه "{university.name}" با موفقیت ایجاد شد!'))
        self.stdout.write(f'ID: {university.id}')
        self.stdout.write(f'Slug: {university.slug}')

