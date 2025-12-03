#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Complete script to fill all empty translations in .po files
"""
import re
import os

# Comprehensive translations dictionary for English
TRANSLATIONS_EN = {
    # Dashboard
    "منو": "Menu",
    "داشبورد": "Dashboard",
    "دوره‌ها": "Courses",
    "اطلاعات کاربر": "User Information",
    "نام کاربری:": "Username:",
    "تلفن:": "Phone:",
    "آدرس:": "Address:",
    "دوره‌های من": "My Courses",
    "قبول": "Passed",
    "ادامه": "Continue",
    "هنوز در دوره‌ای ثبت‌نام نکرده‌اید.": "You haven't enrolled in any course yet.",
    "مدارک و گواهینامه‌ها": "Documents and Certificates",
    "کد:": "Code:",
    "مشاهده": "View",
    "در حال حاضر مدرکی ثبت نشده است.": "No document is currently registered.",
    
    # Login
    "ورود به حساب": "Login to Account",
    "به حساب کاربری خود وارد شوید": "Log in to your account",
    "نام کاربری": "Username",
    "رمز عبور": "Password",
    "ورود ناموفق بود. لطفاً اطلاعات را بررسی کنید و دوباره تلاش کنید.": "Login failed. Please check your information and try again.",
    "حساب ندارید؟ عضویت": "Don't have an account? Sign Up",
    
    # Signup
    "عضویت در کانون": "Join Kanoon",
    "فرم زیر را تکمیل کنید تا حساب کاربری شما ایجاد شود.": "Complete the form below to create your account.",
    "1. اطلاعات شخصی": "1. Personal Information",
    "نام": "First Name",
    "نام خانوادگی": "Last Name",
    "جنسیت": "Gender",
    "تاریخ تولد": "Birth Date",
    "شماره موبایل": "Mobile Number",
    "2. اطلاعات ورود (Login & Security)": "2. Login & Security Information",
    "ایمیل": "Email",
    "تکرار رمز عبور": "Confirm Password",
    "تیک قبول قوانین و حریم خصوصی": "Accept terms and privacy policy",
    "3. اطلاعات آدرس": "3. Address Information",
    "کشور": "Country",
    "شهر": "City",
    "منطقه/محله": "District/Neighborhood",
    "آدرس کامل": "Full Address",
    "کد پستی": "Postal Code",
    "شماره تلفن ثابت (اختیاری)": "Landline Phone (Optional)",
    "4. اطلاعات شغلی": "4. Professional Information",
    "شغل فعلی": "Current Job",
    "زمینه فعالیت": "Field of Activity",
    "نام شرکت": "Company Name",
    "سمت شغلی": "Job Position",
    "سال‌های تجربه": "Years of Experience",
    "وب‌سایت شخصی یا کاری": "Personal or Business Website",
    "لینکدین": "LinkedIn",
    "اینستاگرام / شبکه‌های اجتماعی": "Instagram / Social Media",
    "5. اطلاعات تحصیلی": "5. Educational Information",
    "آخرین مدرک تحصیلی": "Last Education Degree",
    "رشته": "Field of Study",
    "دانشگاه / موسسه": "University / Institution",
    "سال فارغ‌التحصیلی": "Graduation Year",
    "6. ترجیحات": "6. Preferences",
    "دسته‌بندی‌های مورد علاقه": "Favorite Categories",
    "نوع محتوای مورد علاقه": "Preferred Content Type",
    "ساعات ترجیحی دریافت پیام‌ها": "Preferred Message Hours",
    "انتخاب موضوعاتی که دنبال می‌کند": "Select topics you follow",
    "نحوه آشنایی با سایت": "How did you hear about us",
    "لطفاً فیلدهای اجباری را بررسی کنید و دوباره تلاش کنید.": "Please check required fields and try again.",
    "ایجاد حساب": "Create Account",
    "حساب دارید؟ ورود": "Have an account? Login",
    
    # Common
    "بازدید": "Views",
    "قیمت": "Price",
    "مدت زمان": "Duration",
    "مکان": "Location",
    "جزئیات": "Details",
    "اطلاعات بیشتر": "More Information",
    "تماس بگیرید": "Contact Us",
    "جستجو در رویدادها...": "Search in events...",
    "جستجو در املاک...": "Search in properties...",
    "جستجو در خدمات تبلیغاتی...": "Search in advertising services...",
    "جستجو در خدمات بیزینسی...": "Search in business services...",
    "جستجو در خدمات دکوراسیون...": "Search in decoration services...",
    "جستجو در خدمات حقوقی...": "Search in legal services...",
    "جستجو در دانشگاه‌ها...": "Search in universities...",
    
    # About page
    "درباره کانون همیاری فارسی‌زبانان ترکیه": "About Kanoon Hamyari of Persian Speakers in Turkey",
    "تیمی حرفه‌ای از کارشناسان، مشاوران و فعالان اجتماعی": "A professional team of experts, consultants and social activists",
    "🏠 بخش املاک و سرمایه‌گذاری": "🏠 Real Estate & Investment Department",
    "تیم متخصص املاک با تجربه در بازار ترکیه": "Expert real estate team with experience in Turkish market",
    "خدمات املاک و سرمایه‌گذاری": "Real Estate & Investment Services",
    "✅ همکاری با شرکت‌های معتبر ساختمانی": "✅ Cooperation with reputable construction companies",
    "✅ تیم حقوقی همراه برای بررسی قراردادها": "✅ Legal team support for contract review",
    "✅ مشاوره شخصی‌سازی‌شده برای هر پرونده": "✅ Personalized consulting for each case",
    "املاک و سرمایه‌گذاری": "Real Estate & Investment",
    "⚖️ بخش حقوقی و اقامتی": "⚖️ Legal & Residency Department",
    "تیم حقوقی متخصص با تجربه در قوانین مهاجرت ترکیه": "Expert legal team with experience in Turkish immigration laws",
    "خدمات حقوقی و اقامتی": "Legal & Residency Services",
    "✅ همکاری با وکلای ثبت‌شده": "✅ Cooperation with registered lawyers",
    "✅ پشتیبانی کامل فارسی و ترکی": "✅ Full Persian and Turkish support",
    "✅ مشاوره حضوری و آنلاین": "✅ In-person and online consulting",
    "🛠️ دکوراسیون داخلی و بازسازی": "🛠️ Interior Design & Renovation",
    "تیم متخصص طراحی و اجرای پروژه‌های ساختمانی": "Expert design and construction project team",
    "خدمات دکوراسیون داخلی و بازسازی": "Interior Design & Renovation Services",
    "✅ طراحی سه‌بعدی قبل از اجرا": "✅ 3D design before execution",
    
    # Additional common translations
    "دسته‌بندی": "Category",
    "گالری تصاویر": "Image Gallery",
    "تبلیغات مرتبط": "Related Advertisements",
    "قیمت بر اساس توافق": "Price upon agreement",
    "مدت": "Duration",
    "استعلام قیمت و اطلاعات": "Price and Information Inquiry",
    "تماس با ما": "Contact Us",
    "تبلیغات - کانون همیاری": "Advertising - Kanoon Hamyari",
    "زیرمجموعه خدمات تبلیغات": "Advertising Services Subset",
    "طراحی": "Design",
    "طراحی هویت بصری برند (لوگو، رنگ سازمانی، ست اداری)": "Brand visual identity design (logo, corporate colors, stationery)",
    "لوگو": "Logo",
    "رنگ سازمانی": "Corporate Colors",
    "ست اداری": "Stationery",
    "چاپ": "Printing",
    "طراحی و چاپ پوستر، بروشور و بنرهای تبلیغاتی": "Design and printing of posters, brochures and advertising banners",
    "پوستر": "Poster",
    "بروشور": "Brochure",
    "بنر": "Banner",
    "دیجیتال": "Digital",
    "مدیریت شبکه‌های اجتماعی و تولید محتوای تخصصی فارسی-ترکی": "Social media management and production of specialized Persian-Turkish content",
    "فیس‌بوک": "Facebook",
    "اینستاگرام": "Instagram",
    "تلگرام": "Telegram",
    "تبلیغات هدفمند اینستاگرامی و گوگل ادز": "Targeted Instagram and Google Ads advertising",
    "گوگل ادز": "Google Ads",
    "هدفمند": "Targeted",
    "خلاقانه": "Creative",
    "عکاسی و فیلم‌برداری صنعتی و تبلیغاتی": "Industrial and advertising photography and videography",
    "عکاسی": "Photography",
    "فیلم‌برداری": "Videography",
    "صنعتی": "Industrial",
    "وب": "Web",
    "طراحی وب‌سایت و فروشگاه آنلاین برای بیزینس‌ها": "Website and online shop design for businesses",
    "وب‌سایت": "Website",
    "فروشگاه آنلاین": "Online Shop",
    "تماس با ما برای مشاوره": "Contact us for consultation",
    "کانون همیاری فارسی‌زبانان ترکیه - ارائه خدمات جامع ایرانیان در ترکیه": "Kanoon Hamyari of Persian Speakers in Turkey - Comprehensive services for Iranians in Turkey",
    "بازدید:": "Views:",
    "ویژه": "Featured",
    "تگ‌ها:": "Tags:",
    "بازگشت به وبلاگ": "Back to Blog",
    "نظر دهید": "Leave a Comment",
    "مطالب مرتبط": "Related Posts",
    "وبلاگ و خبرنامه": "Blog & Newsletter",
    "وبلاگ و خبرنامه کانون همیاری": "Kanoon Hamyari Blog & Newsletter",
    "خبرها، مقالات و نکات تازه برای جامعه فارسی‌زبانان ترکیه": "News, articles and fresh tips for the Persian-speaking community in Turkey",
    "جستجو در عنوان پست...": "Search in post title...",
    "همه دسته‌ها": "All Categories",
    "اعمال": "Apply",
    "زیرمجموعه خدمات بیزینسی": "Business Services Subset",
    "ثبت شرکت": "Company Registration",
    "انتخاب نوع شرکت (Limited، شخصی یا سهامی) و انجام کامل مراحل ثبت رسمی": "Selecting company type (Limited, personal or joint stock) and completing all official registration steps",
    "انواع شرکت": "Company Types",
    "مشاوره کامل": "Full Consultation",
    "همکاری با حسابداران ترک و ارائه گزارش‌های مالی شفاف": "Cooperation with Turkish accountants and providing transparent financial reports",
    "حسابداری": "Accounting",
    "گزارش مالی": "Financial Report",
    "حسابدار ترک": "Turkish Accountant",
    "مجوز": "License",
    "دریافت مجوز فعالیت برای رستوران، فروشگاه، کلینیک، دفتر خدماتی و…": "Obtaining activity license for restaurant, store, clinic, service office and more",
    "رستوران": "Restaurant",
    "کلینیک": "Clinic",
    "تحلیل بازار": "Market Analysis",
    "تحلیل بازار و تدوین استراتژی فروش": "Market analysis and sales strategy development",
    "شناسایی بازار هدف و برنامه‌ریزی رشد": "Identifying target market and growth planning",
    "بازار هدف": "Target Market",
    "برنامه رشد": "Growth Plan",
    "برندینگ": "Branding",
    "برندینگ و مارکتینگ دیجیتال": "Branding and Digital Marketing",
    "ساخت هویت برند، مدیریت شبکه‌های اجتماعی و تبلیغات آنلاین": "Building brand identity, social media management and online advertising",
    "هویت برند": "Brand Identity",
    "شبکه‌های اجتماعی": "Social Media",
    "تبلیغات آنلاین": "Online Advertising",
    "بین‌المللی": "International",
    "همکاری‌های بین‌المللی": "International Partnerships",
    "اتصال بیزینس‌های ایرانی به بازار و تامین‌کنندگان ترکیه‌ای": "Connecting Iranian businesses to Turkish market and suppliers",
    "اتصال بیزینس": "Business Connection",
    "تامین‌کننده": "Supplier",
    "تماس - کانون همیاری": "Contact - Kanoon Hamyari",
    "آماده پاسخگویی به شما هستیم": "We are ready to answer you",
    "تیم کانون همیاری آماده پاسخگویی به تمام سوالات شماست. از طریق فرم تماس، شبکه‌های اجتماعی یا تماس مستقیم با ما در ارتباط باشید.": "Kanoon Hamyari team is ready to answer all your questions. Contact us through the contact form, social media or direct contact.",
    "ارسال پیام": "Send Message",
    "پیام خود را برای ما ارسال کنید و در کمترین زمان پاسخ دریافت کنید": "Send us your message and receive a response in the shortest time",
    "نام و نام خانوادگی": "Full Name",
    "آدرس ایمیل": "Email Address",
    "موضوع پیام": "Message Subject",
    "متن پیام خود را بنویسید...": "Write your message...",
    "آدرس دفتر مرکزی": "Head Office Address",
    "ترکیه، استانبول، بیلیکدوزو، مرکز خرید بیلیسیوم، طبقه ۴": "Turkey, Istanbul, Beylikdüzü, Bilisium Shopping Center, 4th Floor",
    
    # Additional translations from .po file
    "درباره ما - کانون همیاری": "About Us - Kanoon Hamyari",
    "کانون همیاری فارسی‌زبانان ترکیه با تکیه بر تیمی حرفه‌ای از کارشناسان، مشاوران و فعالان اجتماعی شکل گرفته است تا پلی باشد میان جامعه فارسی‌زبان و فرصت‌های زندگی، تحصیل و کار در ترکیه. ما خدمات خود را بر پایه سه اصل ارائه می‌دهیم: اعتماد، تخصص و ارتباط مؤثر.": "Kanoon Hamyari of Persian Speakers in Turkey was formed with a professional team of experts, consultants and social activists to be a bridge between the Persian-speaking community and opportunities for life, education and work in Turkey. We provide our services based on three principles: trust, expertise and effective communication.",
    "تیم املاک کانون همیاری متشکل از مشاوران رسمی، مسلط به زبان فارسی و ترکی، و آشنا به قوانین خرید و فروش ملک در ترکیه است.": "Kanoon Hamyari's real estate team consists of official consultants, fluent in Persian and Turkish, and familiar with property purchase and sale laws in Turkey.",
    
    # Additional common translations
    "بازطراحی فضاهای مسکونی، اداری و تجاری با طراحی سه‌بعدی و نظارت فنی.": "Redesign of residential, office and commercial spaces with 3D design and technical supervision.",
    "✅ زمان‌بندی دقیق پروژه": "✅ Precise project scheduling",
    "✅ ضمانت کیفیت": "✅ Quality guarantee",
    "دکوراسیون داخلی و بازسازی": "Interior decoration and renovation",
    "تورهای متنوع شهری و طبیعت‌گردی در سراسر ترکیه": "Diverse urban and nature tours throughout Turkey",
    "تورهای تفریحی و طبیعت‌گردی": "Recreational and nature tours",
    "تورها و برنامه‌های تفریحی": "Tours and recreational programs",
    "زنده نگه داشتن فرهنگ و حس ایرانی در ترکیه": "Keeping Iranian culture and spirit alive in Turkey",
    "رویدادها و جشن‌های فرهنگی": "Cultural events and celebrations",
    "رویدادها و جشن‌ها": "Events and celebrations",
    "پنل کاربر": "User Panel",
    "سلام،": "Hello,",
    "ایمیل:": "Email:",
    "دوره": "Course",
    "گواهینامه": "Certificate",
    "🎨 بخش تبلیغات، چاپ و برندینگ": "🎨 Advertising, Printing & Branding Department",
}

# Comprehensive translations dictionary for Turkish
TRANSLATIONS_TR = {
    # Dashboard
    "منو": "Menü",
    "داشبورد": "Kontrol Paneli",
    "دوره‌ها": "Kurslar",
    "اطلاعات کاربر": "Kullanıcı Bilgileri",
    "نام کاربری:": "Kullanıcı Adı:",
    "تلفن:": "Telefon:",
    "آدرس:": "Adres:",
    "دوره‌های من": "Kurslarım",
    "قبول": "Geçti",
    "ادامه": "Devam Et",
    "هنوز در دوره‌ای ثبت‌نام نکرده‌اید.": "Henüz hiçbir kursa kayıt olmadınız.",
    "مدارک و گواهینامه‌ها": "Belgeler ve Sertifikalar",
    "کد:": "Kod:",
    "مشاهده": "Görüntüle",
    "در حال حاضر مدرکی ثبت نشده است.": "Şu anda kayıtlı belge bulunmamaktadır.",
    
    # Login
    "ورود به حساب": "Hesaba Giriş",
    "به حساب کاربری خود وارد شوید": "Hesabınıza giriş yapın",
    "نام کاربری": "Kullanıcı Adı",
    "رمز عبور": "Şifre",
    "ورود ناموفق بود. لطفاً اطلاعات را بررسی کنید و دوباره تلاش کنید.": "Giriş başarısız. Lütfen bilgilerinizi kontrol edin ve tekrar deneyin.",
    "حساب ندارید؟ عضویت": "Hesabınız yok mu? Kayıt Ol",
    
    # Signup
    "عضویت در کانون": "Kanoon'a Katıl",
    "فرم زیر را تکمیل کنید تا حساب کاربری شما ایجاد شود.": "Hesabınızı oluşturmak için aşağıdaki formu doldurun.",
    "1. اطلاعات شخصی": "1. Kişisel Bilgiler",
    "نام": "Ad",
    "نام خانوادگی": "Soyad",
    "جنسیت": "Cinsiyet",
    "تاریخ تولد": "Doğum Tarihi",
    "شماره موبایل": "Cep Telefonu",
    "2. اطلاعات ورود (Login & Security)": "2. Giriş ve Güvenlik Bilgileri",
    "ایمیل": "E-posta",
    "تکرار رمز عبور": "Şifreyi Onayla",
    "تیک قبول قوانین و حریم خصوصی": "Şartları ve gizlilik politikasını kabul ediyorum",
    "3. اطلاعات آدرس": "3. Adres Bilgileri",
    "کشور": "Ülke",
    "شهر": "Şehir",
    "منطقه/محله": "İlçe/Mahalle",
    "آدرس کامل": "Tam Adres",
    "کد پستی": "Posta Kodu",
    "شماره تلفن ثابت (اختیاری)": "Sabit Telefon (İsteğe Bağlı)",
    "4. اطلاعات شغلی": "4. Mesleki Bilgiler",
    "شغل فعلی": "Mevcut İş",
    "زمینه فعالیت": "Faaliyet Alanı",
    "نام شرکت": "Şirket Adı",
    "سمت شغلی": "İş Pozisyonu",
    "سال‌های تجربه": "Deneyim Yılları",
    "وب‌سایت شخصی یا کاری": "Kişisel veya İş Web Sitesi",
    "لینکدین": "LinkedIn",
    "اینستاگرام / شبکه‌های اجتماعی": "Instagram / Sosyal Medya",
    "5. اطلاعات تحصیلی": "5. Eğitim Bilgileri",
    "آخرین مدرک تحصیلی": "Son Eğitim Derecesi",
    "رشته": "Bölüm",
    "دانشگاه / موسسه": "Üniversite / Kurum",
    "سال فارغ‌التحصیلی": "Mezuniyet Yılı",
    "6. ترجیحات": "6. Tercihler",
    "دسته‌بندی‌های مورد علاقه": "Favori Kategoriler",
    "نوع محتوای مورد علاقه": "Tercih Edilen İçerik Türü",
    "ساعات ترجیحی دریافت پیام‌ها": "Tercih Edilen Mesaj Saatleri",
    "انتخاب موضوعاتی که دنبال می‌کند": "Takip ettiğiniz konuları seçin",
    "نحوه آشنایی با سایت": "Bizi nasıl duydunuz",
    "لطفاً فیلدهای اجباری را بررسی کنید و دوباره تلاش کنید.": "Lütfen zorunlu alanları kontrol edin ve tekrar deneyin.",
    "ایجاد حساب": "Hesap Oluştur",
    "حساب دارید؟ ورود": "Hesabınız var mı? Giriş Yap",
    
    # Common
    "بازدید": "Görüntülenme",
    "قیمت": "Fiyat",
    "مدت زمان": "Süre",
    "مکان": "Konum",
    "جزئیات": "Detaylar",
    "اطلاعات بیشتر": "Daha Fazla Bilgi",
    "تماس بگیرید": "İletişime Geçin",
    "جستجو در رویدادها...": "Etkinliklerde ara...",
    "جستجو در املاک...": "Emlaklarda ara...",
    "جستجو در خدمات تبلیغاتی...": "Reklam hizmetlerinde ara...",
    "جستجو در خدمات بیزینسی...": "İş hizmetlerinde ara...",
    "جستجو در خدمات دکوراسیون...": "Dekorasyon hizmetlerinde ara...",
    "جستجو در خدمات حقوقی...": "Hukuk hizmetlerinde ara...",
    "جستجو در دانشگاه‌ها...": "Üniversitelerde ara...",
    
    # About page
    "درباره کانون همیاری فارسی‌زبانان ترکیه": "Kanoon Hamyari Hakkında",
    "تیمی حرفه‌ای از کارشناسان، مشاوران و فعالان اجتماعی": "Uzmanlar, danışmanlar ve sosyal aktivistlerden oluşan profesyonel bir ekip",
    "🏠 بخش املاک و سرمایه‌گذاری": "🏠 Emlak ve Yatırım Bölümü",
    "تیم متخصص املاک با تجربه در بازار ترکیه": "Türkiye pazarında deneyimli uzman emlak ekibi",
    "خدمات املاک و سرمایه‌گذاری": "Emlak ve Yatırım Hizmetleri",
    "✅ همکاری با شرکت‌های معتبر ساختمانی": "✅ Güvenilir inşaat şirketleri ile işbirliği",
    "✅ تیم حقوقی همراه برای بررسی قراردادها": "✅ Sözleşme incelemesi için hukuk ekibi desteği",
    "✅ مشاوره شخصی‌سازی‌شده برای هر پرونده": "✅ Her dava için kişiselleştirilmiş danışmanlık",
    "املاک و سرمایه‌گذاری": "Emlak ve Yatırım",
    "⚖️ بخش حقوقی و اقامتی": "⚖️ Hukuk ve İkamet Bölümü",
    "تیم حقوقی متخصص با تجربه در قوانین مهاجرت ترکیه": "Türkiye göç yasalarında deneyimli uzman hukuk ekibi",
    "خدمات حقوقی و اقامتی": "Hukuk ve İkamet Hizmetleri",
    "✅ همکاری با وکلای ثبت‌شده": "✅ Kayıtlı avukatlarla işbirliği",
    "✅ پشتیبانی کامل فارسی و ترکی": "✅ Tam Farsça ve Türkçe destek",
    "✅ مشاوره حضوری و آنلاین": "✅ Yüz yüze ve online danışmanlık",
    "🛠️ دکوراسیون داخلی و بازسازی": "🛠️ İç Mimarlık ve Yenileme",
    "تیم متخصص طراحی و اجرای پروژه‌های ساختمانی": "Tasarım ve inşaat projeleri uzman ekibi",
    "خدمات دکوراسیون داخلی و بازسازی": "İç Mimarlık ve Yenileme Hizmetleri",
    "✅ طراحی سه‌بعدی قبل از اجرا": "✅ Uygulama öncesi 3D tasarım",
    
    # Additional common translations
    "دسته‌بندی": "Kategori",
    "گالری تصاویر": "Görsel Galerisi",
    "تبلیغات مرتبط": "İlgili Reklamlar",
    "قیمت بر اساس توافق": "Anlaşmaya göre fiyat",
    "مدت": "Süre",
    "استعلام قیمت و اطلاعات": "Fiyat ve Bilgi Talebi",
    "تماس با ما": "Bize Ulaşın",
    "تبلیغات - کانون همیاری": "Reklam - Kanoon Hamyari",
    "زیرمجموعه خدمات تبلیغات": "Reklam Hizmetleri Alt Kategorileri",
    "طراحی": "Tasarım",
    "طراحی هویت بصری برند (لوگو، رنگ سازمانی، ست اداری)": "Marka görsel kimlik tasarımı (logo, kurumsal renkler, ofis seti)",
    "لوگو": "Logo",
    "رنگ سازمانی": "Kurumsal Renkler",
    "ست اداری": "Ofis Seti",
    "چاپ": "Baskı",
    "طراحی و چاپ پوستر، بروشور و بنرهای تبلیغاتی": "Poster, broşür ve reklam afişlerinin tasarımı ve baskısı",
    "پوستر": "Poster",
    "بروشور": "Broşür",
    "بنر": "Afiş",
    "دیجیتال": "Dijital",
    "مدیریت شبکه‌های اجتماعی و تولید محتوای تخصصی فارسی-ترکی": "Sosyal medya yönetimi ve özel Farsça-Türkçe içerik üretimi",
    "فیس‌بوک": "Facebook",
    "اینستاگرام": "Instagram",
    "تلگرام": "Telegram",
    "تبلیغات هدفمند اینستاگرامی و گوگل ادز": "Hedefli Instagram ve Google Ads reklamları",
    "گوگل ادز": "Google Ads",
    "هدفمند": "Hedefli",
    "خلاقانه": "Yaratıcı",
    "عکاسی و فیلم‌برداری صنعتی و تبلیغاتی": "Endüstriyel ve reklam fotoğrafçılığı ve videografi",
    "عکاسی": "Fotoğrafçılık",
    "فیلم‌برداری": "Videografi",
    "صنعتی": "Endüstriyel",
    "وب": "Web",
    "طراحی وب‌سایت و فروشگاه آنلاین برای بیزینس‌ها": "İşletmeler için web sitesi ve online mağaza tasarımı",
    "وب‌سایت": "Web Sitesi",
    "فروشگاه آنلاین": "Online Mağaza",
    "تماس با ما برای مشاوره": "Danışmanlık için bize ulaşın",
    "کانون همیاری فارسی‌زبانان ترکیه - ارائه خدمات جامع ایرانیان در ترکیه": "Türkiye'deki Farsça Konuşanlar Kanoon Hamyari - Türkiye'deki İranlılar için kapsamlı hizmetler",
    "بازدید:": "Görüntülenme:",
    "ویژه": "Öne Çıkan",
    "تگ‌ها:": "Etiketler:",
    "بازگشت به وبلاگ": "Blog'a Dön",
    "نظر دهید": "Yorum Yap",
    "مطالب مرتبط": "İlgili Yazılar",
    "وبلاگ و خبرنامه": "Blog ve Bülten",
    "وبلاگ و خبرنامه کانون همیاری": "Kanoon Hamyari Blog ve Bülten",
    "خبرها، مقالات و نکات تازه برای جامعه فارسی‌زبانان ترکیه": "Türkiye'deki Farsça konuşan topluluk için haberler, makaleler ve yeni ipuçları",
    "جستجو در عنوان پست...": "Gönderi başlığında ara...",
    "همه دسته‌ها": "Tüm Kategoriler",
    "اعمال": "Uygula",
    "زیرمجموعه خدمات بیزینسی": "İş Hizmetleri Alt Kategorileri",
    "ثبت شرکت": "Şirket Kaydı",
    "انتخاب نوع شرکت (Limited، شخصی یا سهامی) و انجام کامل مراحل ثبت رسمی": "Şirket türü seçimi (Limited, kişisel veya anonim) ve resmi kayıt adımlarının tamamlanması",
    "انواع شرکت": "Şirket Türleri",
    "مشاوره کامل": "Tam Danışmanlık",
    "همکاری با حسابداران ترک و ارائه گزارش‌های مالی شفاف": "Türk muhasebecilerle işbirliği ve şeffaf mali raporlar sunma",
    "حسابداری": "Muhasebe",
    "گزارش مالی": "Mali Rapor",
    "حسابدار ترک": "Türk Muhasebeci",
    "مجوز": "Lisans",
    "دریافت مجوز فعالیت برای رستوران، فروشگاه، کلینیک، دفتر خدماتی و…": "Restoran, mağaza, klinik, hizmet ofisi ve daha fazlası için faaliyet lisansı alma",
    "رستوران": "Restoran",
    "کلینیک": "Klinik",
    "تحلیل بازار": "Pazar Analizi",
    "تحلیل بازار و تدوین استراتژی فروش": "Pazar analizi ve satış stratejisi geliştirme",
    "شناسایی بازار هدف و برنامه‌ریزی رشد": "Hedef pazar belirleme ve büyüme planlaması",
    "بازار هدف": "Hedef Pazar",
    "برنامه رشد": "Büyüme Planı",
    "برندینگ": "Markalaşma",
    "برندینگ و مارکتینگ دیجیتال": "Markalaşma ve Dijital Pazarlama",
    "ساخت هویت برند، مدیریت شبکه‌های اجتماعی و تبلیغات آنلاین": "Marka kimliği oluşturma, sosyal medya yönetimi ve online reklamcılık",
    "هویت برند": "Marka Kimliği",
    "شبکه‌های اجتماعی": "Sosyal Medya",
    "تبلیغات آنلاین": "Online Reklamcılık",
    "بین‌المللی": "Uluslararası",
    "همکاری‌های بین‌المللی": "Uluslararası Ortaklıklar",
    "اتصال بیزینس‌های ایرانی به بازار و تامین‌کنندگان ترکیه‌ای": "İran işletmelerini Türk pazarına ve tedarikçilere bağlama",
    "اتصال بیزینس": "İş Bağlantısı",
    "تامین‌کننده": "Tedarikçi",
    "تماس - کانون همیاری": "İletişim - Kanoon Hamyari",
    "آماده پاسخگویی به شما هستیم": "Size cevap vermeye hazırız",
    "تیم کانون همیاری آماده پاسخگویی به تمام سوالات شماست. از طریق فرم تماس، شبکه‌های اجتماعی یا تماس مستقیم با ما در ارتباط باشید.": "Kanoon Hamyari ekibi tüm sorularınızı yanıtlamaya hazırdır. İletişim formu, sosyal medya veya doğrudan iletişim yoluyla bizimle iletişime geçin.",
    "ارسال پیام": "Mesaj Gönder",
    "پیام خود را برای ما ارسال کنید و در کمترین زمان پاسخ دریافت کنید": "Bize mesajınızı gönderin ve en kısa sürede yanıt alın",
    "نام و نام خانوادگی": "Ad Soyad",
    "آدرس ایمیل": "E-posta Adresi",
    "موضوع پیام": "Mesaj Konusu",
    "متن پیام خود را بنویسید...": "Mesajınızı yazın...",
    "آدرس دفتر مرکزی": "Genel Merkez Adresi",
    "ترکیه، استانبول، بیلیکدوزو، مرکز خرید بیلیسیوم، طبقه ۴": "Türkiye, İstanbul, Beylikdüzü, Bilisium Alışveriş Merkezi, 4. Kat",
    
    # Additional translations from .po file
    "درباره ما - کانون همیاری": "Hakkımızda - Kanoon Hamyari",
    "کانون همیاری فارسی‌زبانان ترکیه با تکیه بر تیمی حرفه‌ای از کارشناسان، مشاوران و فعالان اجتماعی شکل گرفته است تا پلی باشد میان جامعه فارسی‌زبان و فرصت‌های زندگی، تحصیل و کار در ترکیه. ما خدمات خود را بر پایه سه اصل ارائه می‌دهیم: اعتماد، تخصص و ارتباط مؤثر.": "Türkiye'deki Farsça Konuşanlar Kanoon Hamyari, uzmanlar, danışmanlar ve sosyal aktivistlerden oluşan profesyonel bir ekiple, Farsça konuşan topluluk ile Türkiye'deki yaşam, eğitim ve iş fırsatları arasında bir köprü olmak için kurulmuştur. Hizmetlerimizi üç temel prensibe dayanarak sunuyoruz: güven, uzmanlık ve etkili iletişim.",
    "تیم املاک کانون همیاری متشکل از مشاوران رسمی، مسلط به زبان فارسی و ترکی، و آشنا به قوانین خرید و فروش ملک در ترکیه است.": "Kanoon Hamyari emlak ekibi, resmi danışmanlardan oluşur, Farsça ve Türkçe'ye hakimdir ve Türkiye'deki mülk satın alma ve satma yasalarına aşinadır.",
    
    # Additional common translations
    "بازطراحی فضاهای مسکونی، اداری و تجاری با طراحی سه‌بعدی و نظارت فنی.": "Konut, ofis ve ticari alanların 3D tasarım ve teknik denetim ile yeniden tasarımı.",
    "✅ زمان‌بندی دقیق پروژه": "✅ Hassas proje zamanlaması",
    "✅ ضمانت کیفیت": "✅ Kalite garantisi",
    "دکوراسیون داخلی و بازسازی": "İç mimarlık ve yenileme",
    "تورهای متنوع شهری و طبیعت‌گردی در سراسر ترکیه": "Türkiye genelinde çeşitli şehir ve doğa turları",
    "تورهای تفریحی و طبیعت‌گردی": "Eğlence ve doğa turları",
    "تورها و برنامه‌های تفریحی": "Turlar ve eğlence programları",
    "زنده نگه داشتن فرهنگ و حس ایرانی در ترکیه": "Türkiye'de İran kültürü ve ruhunu canlı tutmak",
    "رویدادها و جشن‌های فرهنگی": "Kültürel etkinlikler ve kutlamalar",
    "رویدادها و جشن‌ها": "Etkinlikler ve kutlamalar",
    "پنل کاربر": "Kullanıcı Paneli",
    "سلام،": "Merhaba,",
    "ایمیل:": "E-posta:",
    "دوره": "Kurs",
    "گواهینامه": "Sertifika",
    "🎨 بخش تبلیغات، چاپ و برندینگ": "🎨 Reklam, Baskı ve Markalaşma Bölümü",
}

def update_po_file(file_path, translations):
    """Update .po file with translations"""
    with open(file_path, 'r', encoding='utf-8') as f:
        lines = f.readlines()
    
    i = 0
    updated_count = 0
    
    while i < len(lines):
        line = lines[i]
        
        # Check for single-line msgid
        if line.startswith('msgid "'):
            match = re.match(r'msgid "([^"]+)"', line)
            if match:
                msgid_text = match.group(1).replace('\\"', '"').replace('\\n', '\n')
                
                # Check if next line is empty msgstr
                if i + 1 < len(lines) and lines[i + 1].strip() == 'msgstr ""':
                    if msgid_text in translations:
                        translation = translations[msgid_text]
                        translation = translation.replace('\\', '\\\\').replace('"', '\\"').replace('\n', '\\n')
                        lines[i + 1] = f'msgstr "{translation}"\n'
                        updated_count += 1
        
        # Check for multi-line msgid (msgid "" followed by quoted lines)
        elif line.strip() == 'msgid ""':
            # Collect multi-line msgid
            j = i + 1
            msgid_text = ''
            msgid_lines_list = []
            
            while j < len(lines):
                next_line = lines[j]
                
                # Check if it's a quoted line (part of msgid)
                stripped = next_line.strip()
                # Check if line starts with quote (may have leading spaces)
                if stripped and stripped[0] == '"' and stripped[-1] == '"':
                    # Extract text from quoted line (remove quotes and unescape)
                    line_text = stripped[1:-1]
                    line_text = line_text.replace('\\"', '"').replace('\\n', '\n')
                    msgid_text += line_text
                    msgid_lines_list.append(j)
                elif stripped == 'msgstr ""':
                    # Found empty msgstr, check if we have translation
                    # Also try without spaces between lines
                    msgid_clean = msgid_text.strip()
                    if msgid_clean in translations:
                        translation = translations[msgid_clean]
                        # Format translation for multi-line (escape properly)
                        translation = translation.replace('\\', '\\\\').replace('"', '\\"').replace('\n', '\\n')
                        lines[j] = f'msgstr "{translation}"\n'
                        updated_count += 1
                    break
                elif next_line.startswith('msgstr'):
                    # Already has translation, skip
                    break
                elif not stripped.startswith('"') and stripped and not stripped.startswith('#'):
                    # End of msgid block (not a comment, not a quote)
                    break
                
                j += 1
        
        i += 1
    
    with open(file_path, 'w', encoding='utf-8') as f:
        f.writelines(lines)
    
    print(f"Updated {file_path} ({updated_count} translations)")

if __name__ == '__main__':
    en_file = 'locale/en/LC_MESSAGES/django.po'
    tr_file = 'locale/tr/LC_MESSAGES/django.po'
    
    if os.path.exists(en_file):
        update_po_file(en_file, TRANSLATIONS_EN)
        print(f"✓ English translations updated")
    
    if os.path.exists(tr_file):
        update_po_file(tr_file, TRANSLATIONS_TR)
        print(f"✓ Turkish translations updated")
    
    print("\nTranslation files updated successfully!")

