# ICT-Challenge-Tesla-Team-2025


---


# سوال پردازش تصویر و تشخیص دست نویس فارسی با Ai
https://github.com/mr-r0ot/ICT-Challenge-Tesla-Team-2025/tree/main/AI_Recognition%20of%20Persian%20manuscripts
```
یکی از چالش‌های هوش مصنوعی، خواندن متون دست‌نویس است. در این سؤال، شما باید برنامه‌ای طراحی کنید که بتواند دست‌خط فارسی را از روی تصاویر بخواند و متن دقیق آن را استخراج کند.


دیتاست مورد نیاز به پیوست ارائه شده است


🎯 هدف

برنامه شما باید با استفاده از روش‌های پردازش تصویر، یادگیری ماشین، OCR یا هر روش دیگر، دست‌خط فارسی موجود در تصاویر را به متن دیجیتال (متن قابل خواندن توسط کامپیوتر) تبدیل کند.


📥 ورودی

مجموعه‌ای از تصاویر دست‌نویس با فرمت .png یا .jpg در اختیار شما قرار خواهد گرفت. این تصاویر شامل متونی هستند که با دستخط فارسی نوشته شده‌اند.

فایل مورد نظربه پیوست ارائه شده است.


handwritten_data/
├── 1.png
├── 2.png
├── 3.png
...
    

📤 خروجی

یک فایل متنی با فرمت .txt که در آن، در هر خط متن خوانده‌شده‌ی تصویر متناظر نوشته شده باشد.


1.png → این یک متن تستی است
2.png → سلام، حال شما چطور است؟
3.png → پرداخت شد
...
    

⚖️ معیار داوری

دقت در تشخیص کلمات (Word Accuracy)
دقت در حروف (Character Accuracy)
سرعت اجرای برنامه
انعطاف‌پذیری در تشخیص انواع مختلف دستخط‌ها
طراحی تمیز و قابل اجرا


🛠 محدودیت‌ها

می‌توانید از کتابخانه‌های استاندارد OCR مانند Tesseract استفاده کنید.
ارزیابی بر اساس خروجی نهایی انجام خواهد شد نه صرف استفاده از ابزار خاص.
اگر از مدل یادگیری ماشین استفاده می‌کنید، مدل باید قابل آموزش و اجرا توسط داور باشد (فایل مدل یا لینک آن ارائه شود).
```
---


# سوال بولتن
https://github.com/mr-r0ot/ICT-Challenge-Tesla-Team-2025/tree/main/news_sender
```
بسیاری از شرکت‌های رسانه‌ای، بولتن‌هایی اختصاصی برای اشخاص و برندهای سرشناس تهیه می‌کنند. این بولتن‌ها شامل آخرین مطالب منتشر شده در مورد فرد یا شرکت مورد نظر در رسانه‌های دیجیتال (وب‌سایت‌ها، خبرگزاری‌ها، وبلاگ‌ها و ...) هستند.

بولتن خبری معمولاً به صورت دوره ای منتشر می شود و تمرکز آن بر ارائه اطلاعات سریع و به روز رسانی های فوری است. این نشریات بیشتر شامل اخبار، گزارش ها، و اطلاعات مهمی هستند که نیاز به اطلاع رسانی فوری دارند. هدف اصلی بولتن خبری، اطلاع رسانی به مخاطبان در مورد وقایع و تغییرات جاری است.



ایده بسیار جذابی دارید: برنامه‌ای طراحی کنید که با دریافت نام یک شخص یا شرکت (مثلاً "حسین افشین") و یک بازه زمانی مشخص (مثلاً هفتگی)، در بازه‌های مشخص‌شده، وب را پایش کرده و یک بولتن خبری بسازد. این بولتن باید شامل لیستی از آخرین مطالبی باشد که در مورد آن شخص یا شرکت منتشر شده است، به همراه:

عنوان مطلب
تاریخ انتشار
لینک به منبع اصلی
تصویر شاخص (در صورت وجود)

در نهایت بولتن ساخته‌شده به صورت یک ایمیل منظم و خوانا به آدرس ایمیلی که کاربر مشخص کرده است ارسال شود.

نیازمندی‌ها:

برنامه باید قابلیت تعریف چند فرد یا شرکت با بازه‌های جداگانه را داشته باشد (مثلاً هر هفته برای "حسین افشین" و هر 3 روز برای "اپل").
نتایج باید مرتب، خوش‌ساختار و قابل خواندن در قالب ایمیل HTML باشند.
ایمیل‌ها باید به صورت خودکار و در زمان مقرر ارسال شوند.
برای جلوگیری از داده‌های تکراری، سیستم باید مطالب قبلاً ارسال‌شده را ذخیره کند و دوباره ارسال نکند.

راهنمایی‌ها:

می‌توانید از سرویس‌هایی مانند Google News API، Bing News Search یا روش‌های scraping استفاده کنید.
ارسال ایمیل می‌تواند از طریق SMTP، Mailgun، یا هر سرویس مشابه انجام شود.
خروجی بولتن را به صورت HTML طراحی کنید تا روی موبایل هم به خوبی نمایش داده شود.

پیشنهاد: برای امتیاز بیشتر، نسخه دمو برای یک نام خاص و ایمیل فرضی اجرا کنید که حداقل یک بولتن بسازد و ارسال کند.



باید یک رابط کاربری با کتابخانه CTK داشته باشد
و در آن بتوان بازه های زمانی با اسم فرد هدف و ایمیل هدف
بازی زمانی باید یکی از گزینه های روزانه یا هفتگی یا ماهانه باشد
در هر سه حالت باید ساعت دقیق را بگیرد
اما اگر هفتگی را انتخاب کرد روز های هفته را نمایش دهد و بتواند هر چندتا که می خواهم انتخاب کند
اگر ماهانه را زد از او بخواهد شماره یک ماه و روز یک ماه را وارد کند مثلا 1403/05/22

و باید برنامه در هر بازه زمانی که ذکر شده بود همواره و همیشه اسم آن فرد را در گوگل جستجوی کند و 10 لینک برتر را پیدا و مطالب را استخراج کند شامل:
عنوان مطلب
تاریخ انتشار
لینک به منبع اصلی
تصویر شاخص (در صورت وجود)


و این اطلاعات را به صورت یک html بسیار زیبا از طریق یک ارایه دهنده email مثلا mailtrap.io یا هر چیز دیگر ارسال کند
```

---

# سوال telegram
https://github.com/mr-r0ot/ICT-Challenge-Tesla-Team-2025/blob/main/telegram/tel.md
```
تلگرام مجهز به یک فضای ذخیره سازی ابری است. توسعه دهندگان تلگرام مشکلات عدیده ای داشته اند که از پس آنها بر آمده اند. از طرفی ویژگی های جذابی به آن اضافه نموده اند.



پاول دورف، تعاریف بسیار جذابی از تیم شما شنیده است. او فرصت را غنیمت شمرده، با شما تماس می‌گیرد و از شما می‌خواهد دو نیازمندی تلگرام را پیاده سازی کنید. او درخواست خود را به این شرح بیان نموده است:

در تلگرام معمولا بیش از ۵۰ درصد فایل‌هایی که منتقل می‌شوند در چت‌های مختلف مشترک هستند. برای مثال شما از فیلمی خوشتان آمده آن را برای دوستتان ارسال کرده‌اید، همچنین در جای دیگر کشور، جوانی به نام جواد، دقیقا همین فایل را مجدداً آپلود کرده و برای پدرش ارسال نموده است، در صورتی که این فایل یکسان است. (تلگرام در نسخه حاضر این امکان را دارد که اگر فایلی یک بار آپلود شود و چند بار ارسال گردد، بر خلاف واتس‌اپ، همان فایل را ارسال نموده و زمان و حجم اضافه نمی‌گیرد)

راه حلی پیشنهاد دهید که در چنین شرایطی در زمان و حجم صرفه‌جویی شود. برنامه نویسان کلاینت و سرور تلگرام گوش به فرمان شما هستند.

از طرفی تلگرام نیاز دارد در هنگام آپلود فایل، کاربر بتواند با کلیک بر روی دکمه توقف، فرآیند را متوقف کند، اما با این تفاوت که بعد از بازگشت به برنامه و در صورت نیاز با کلیک بر روی ادامه، ادامه فایل آپلود شود.

این ویژگی منحصر به فرد حتی باید بتواند به مدت چند روز نیز برای ادامه فرآیند آپلود منتظر بماند.

راه حل های خود را مستند کنید.
توجه داشته باشید که کاربر تنها به مدت ۳ روز امکان ادامه آپلود خواهد داشت.
توجه داشته باشید که در مدت زمان توقف تا ادامه، فایل کاربر می‌تواند تغییر کند.

پاول دورف همچنین از شما می‌خواهد برای آنکه برنامه نویسانش، بتوانند آنچه را که مستند کرده‌اید پیاده کنند، شما خود به صورت کاملاً ساده و خلاصه، برای هر دو بخش مسئله، نمونه برنامه‌ای حاضر کنید، شامل سرور و یک کلاینت به شدت ساده، که فرآیند را برای حداقل یک فایل مشخص و به صورت دمو انجام دهد.

توجه داشته باشید

پاسخ ناقص نیز امتیاز در بر دارد.
```

---

# سوال rule
https://github.com/mr-r0ot/ICT-Challenge-Tesla-Team-2025/tree/main/Rule
```
شما یک سیستم مالی آماده خریده‌اید که شامل ماژول‌های مختلفی مثل دریافت، پرداخت، ثبت اسناد حسابداری، مدیریت طرف حساب‌ها، ثبت فاکتور، صورت‌حساب بانکی و ... است.

اما فقط به دیتابیس این سیستم دسترسی دارید و به کد اصلی آن دسترسی ندارید. یعنی نمی‌توانید به‌راحتی در روال کار سیستم تغییراتی ایجاد کنید یا منطق جدیدی اضافه کنید.

با این حال، شما می‌خواهید یک سیستم هوشمند بسازید که بتواند به صورت داینامیک و بر اساس اتفاقاتی که در این سیستم مالی رخ می‌دهد، واکنش‌های  قابل تعریف توسط کاربر انجام دهد. یعنی یک سیستم داینامیک طراحی کنید که بتواند با مانیتور کردن تغییرات در پایگاه داده (Database Events)، یک سری «قوانین (Rules)» را اجرا کند. هر قانون شامل یک شرط (Trigger Condition) و یک عمل (Action) است.



این سیستم مالی دارای ساختار  زیر است ( اسکریپت ایجاد جداول در اختیار شما قرار میگیرد)
ثبت تراکنش مالی (پرداخت / دریافت):
فیلدهای کلیدی: مبلغ، نوع تراکنش، تاریخ، طرف حساب، حساب بانکی، پروژه، توضیحات
اسناد حسابداری: 
شامل بدهکار/بستانکار، شماره سند، تاریخ سند، شرح سند 
طرف حساب‌ها:
شامل مشتری‌ها و تامین‌کننده‌ها، مانده حساب، مشخصات تماس 
فاکتورها و صورتحساب‌ها

هدف:

ساخت سیستمی که با مانیتور کردن دیتابیس بتواند:

تغییرات را تشخیص دهد
بررسی کند آیا شرط یا شرطهایی برای این تغییر تعریف شده است.
در صورت برقرار بودن، عملیات مشخصی را انجام دهد.

این سیستم باید داری امکانات زیر باشد:

تعریف رابطی برای ساخت قوانین توسط کاربر نهایی (برای کاربر باید امکانی فراهم شود که پیام مطلوب خود را تعریف کند تا پیامی حاوی اطلاعات مورد نیاز را در زمان اتفاق افتادن رویداد دریافت کند و نه لزوما یک پیام کلی. مثلا بتواند نام کاربری مربوط به کاربر وارد شده به سیستم یا شماره سفارش خرید را در پیام ارسالی  مشخص کند.)
معرفی کاربر و کانال های ارتباطی مطلوب آنها
امکان فعال/غیر فعال کردن قوانین وجود داشته باشد.
در سریع ترین زمان ممکن قوانین اجرا شوند.
ترتیب رخ دادن رویدادها حفظ شود.
اطلاع رسانی یک رویداد نباید از دست برود.
کاربر بتواند گزارشی از قوانین اجرا شده را ببیند ( سیستم مانیتورینگ میتواند گسترده تر باشد)
سامانه باید مقیاس پذیر باشد. رویدادهای زیادی از طریق کانال های ارتباطی متعدد با گیرندگان زیادی اطلاع رسانی شوند.
رعایت اصول امنیتی
ارائه مستندات مرتبط و مناسب، به همراه معماری راه حل
پشتیبانی از انواع مختلف Action مثل:
ارسال ایمیل
ارسال پیام به تلگرام یا واتساپ
ذخیره لاگ
صدا زدن یک API خارجی

قوانین 

قوانین می توانند کاملا داینامیک باشند. مثال های زیر را ببینید:



مثال‌های ساده:

اگر تراکنشی با مبلغ بیشتر از ۵۰,۰۰۰,۰۰۰ ثبت شد → برای مدیر ایمیل ارسال شود.
اگر مانده یک طرف حساب منفی شد → پیام به تلگرام حسابدار ارسال شود.
اگر سند حسابداری جدیدی ثبت شد که در شرح آن عبارت «جریمه» بود → در یک جدول جداگانه لاگ شود.



مثال‌های متوسط:

اگر طی ۱۰ دقیقه گذشته بیش از ۵ تراکنش ثبت شد → نوتیفیکیشن هشدار ارسال شود.
اگر فاکتور جدیدی ثبت شد و مبلغ آن بیشتر از ۲۰٪ بالاتر از میانگین ماه گذشته بود → API اطلاع‌رسانی اجرا شود.
اگر سندی حذف شد → اطلاعات آن برای بررسی به یک ایمیل خاص ارسال شود.

 

مثال‌های پیشرفته (برای تیم‌های قوی‌تر):

اگر طرف حسابی سه بار متوالی در طی ۳۰ روز اخیر با تأخیر پرداخت کرده → برای بخش حقوقی پیام ارسال شود.
اگر در 5 دقیقه گذشته ۳ تراکنش بالای ۱۰۰ میلیون تومان اتفاق افتاد ، برای مدیر ایمیل ارسال شود.
اگر پرداختی به حساب بانکی خاصی انجام شد که در لیست سیاه ثبت شده → سیستم خودکار آن را به عنوان تراکنش مشکوک علامت‌گذاری کند.

قوانین در قالب yaml تعریف میشوند. فایل yaml به همراه ساختار جداول دیتابیس به پیوست ارائه شده است.
```
---

# سوال بازاریاب
https://github.com/mr-r0ot/ICT-Challenge-Tesla-Team-2025/tree/main/Erp
```
عنوان: بیشینه‌سازی ارزش بازدیدهای بازاریاب در بستر ERP با درنظر گرفتن محدودیت‌های زمانی، مکانی و ترافیکی

در یک سیستم ERP پخش، هر بازاریاب موظف است در یک روز کاری، تعدادی از مشتریان را ویزیت کند.

هدف بازاریاب:
در بازه‌ی کاری روزانه (مثلاً از ساعت ۸:۳۰ تا ۱۶:۳۰)، با ویزیت تعدادی از مشتریان، بیشترین ارزش تجاری ممکن را خلق کند.

مشخصات ورودی:

مشتری‌ها:
هر مشتری دارای ویژگی‌های زیر است:
- location: مختصات جغرافیایی (مثلاً GPS)
- visit_value: عددی که نشان‌دهنده ارزش ویزیت اوست (مثلاً بر اساس حجم خرید، یا میزان اهمیت)
- available_from و available_to: بازه زمانی که مشتری در دسترس است برای ویزیت
- visit_duration: زمانی که طول می‌کشد تا ویزیت کامل شود (مثلاً ۱۵ دقیقه)

ملاحظات مسیریابی:
زمان سفر بین دو نقطه با توجه به ترافیک (مقدار تقریبی یا تابعی از ساعت روز) متغیر است.

هدف نهایی:
یافتن دنباله‌ای از مشتریان که بازاریاب باید ویزیت کند، به طوری که:
- مجموع ارزش بازدیدها (visit_value) ماکزیمم شود.
- هیچ بازدیدی خارج از بازه‌ی دسترسی مشتری نباشد.
- بازدیدها از زمان کاری بازاریاب تجاوز نکند.
- زمان سفر بین مشتری‌ها و زمان ویزیت رعایت شده باشد.

ورودی / خروجی: به پیوست ارائه شده است.
```
---


# سوال آزمون
https://github.com/mr-r0ot/ICT-Challenge-Tesla-Team-2025/tree/main/exam
```
فرض کنید 100000 نفر در 10 آزمون و در هر آزمون در 5 درس شرکت می‌کنند. پس از برگزاری آزمون‌ها، پاسخدهی شرکت کنندگان بررسی شده و به هر نفر در هر درس چهار رنگ (از ضعیف تا قوی) قرمز، زرد، سبز و آبی اختصاص داده می‌شود:

قرمز: صفر
زرد: یک
سبز: دو
آبی: سه

بنابراین برای هر شرکت‌کننده 50 رنگ اختصاص داده می‌شود.

مفروضات:

شماره شناسایی شرکت‌کنندگان از 1 الی 100000 می‌باشد.
شماره آزمون‌ها از 1 الی 10 می‌باشد.
شماره درس‌ها در هر آزمون 1 الی 5 می‌باشد، ضریب هر درس همان شماره درس است.

الگوریتمی طراحی کنید که:

پاسخ اولیه شرکت‌کنندگان به صورت Random تولید شود.
امکان درج رنگ هر درس در هر آزمون برای هر شرکت‌کننده وجود داشته باشد.
اطلاعات جمع‌آوری‌شده ذخیره و بازیابی شود.
میزان حافظه مصرفی برای نگهداری این اطلاعات در کمترین حالت ممکن باشد: 100000×10×5×4 حالت یعنی کمتر از 2.5MB
امکان ارائه آمارهای مختلف نظیر موارد ذیل وجود داشته باشد:
N نفر برتر (رنگ آبی) یک درس در یک آزمون
N نفر برتر در یک آزمون با توجه به ضرایب دروس
N برتر کل آزمون‌ها
میانگین پاسخگویی در هر درس در هر آزمون

نکات:

با هر زبانی که بلدید می‌توانید این الگوریتم را تولید کنید.
UI بایستی شفاف و عملکرد آن سریع باشد.
اطلاعات را می‌توانید در یک فایل یا بانک اطلاعاتی نگهداری کنید.
حجم حافظه مصرفی در مدیای نگهداری‌شده و در حافظه (Memory) کمتر از 2.5MB باشد.
```
