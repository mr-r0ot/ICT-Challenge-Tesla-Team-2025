خب اینجا می خوام راح حل هارو بگم امیدوارم مفید باشه



1. کاهش تکرار در ذخیره‌سازی فایل‌ها
2. قابلیت توقف و ادامه آپلود تا ۳ روز با تغییر احتمالی فایل



 1. حذف داده‌های تکراری 

 هر فایل توسط کلاینت با استفاده از یک تابع هش امن (مثل SHA-256) شناسایی می‌بشه. اگر فایلی با همان هش قبلاً در سرور ذخیره شده باشد، سرور به جای ذخیره فایل جدید صرفاً مرجع به فایل قبلی را بازمی‌گرداند.

پروتوکول اینه (به صورت کلی)

1. محاسبه‌ی هش: قبل از آپلود، کلاینت هش فایل (یا هش بلوک‌های بزرگ) را محاسبه می کنه.
2. درخواست به سرور: کلاینت هش را به سرور ارسال می کنه: POST /check?h=SHA256
3. پاسخ سرور:

    اگر فایل وجود داشته باشد: کد 200 و آدرس CDN یا شناسه‌ی داخلی فایل ارسال می‌بشه.
    در غیر این صورت: کد 404.
4. آپلود فایل: اگر فایل وجود نداشته باشد، کلاینت آپلود را آغاز می کنه (می‌تواند به صورت معمول یا بلوک-بندی شده).

حالا چه مزایایی  داره:

 صرفه‌جویی در حجم ذخیره‌سازی و پهنای باند تکراری.
 استفاده از CDN مشترک بر اساس شناسه‌ی یکتا.



 2. آپلود قابل توقف و ادامه 

نیازمندی‌ها:

 امکان توقف از سمت کاربر و ادامه تا ۳ روز بعد.
 فایل می‌تواند بین توقف و ادامه دچار تغییر بشه.


1. تقسیم فایل به بلوک‌های ثابت (مثلاً 1 MiB هر بلوک).
2. محاسبه‌ی هش هر بلوک (SHA-256). بردار هش‌ها در کلاینت نگهداری می‌بشه.
3. شروع آپلود:

    کلاینت به سرور درخواست POST /start ارسال می کنه و یک session_id دریافت می کنه.
    سرور یک دایرکتوری موقت برای این session_id ایجاد می کنه و متادیتا (تاریخ شروع) ذخیره می کنه.
4. آپلود بلوک‌ها:

    کلاینت برای هر بلوک به ترتیب (یا به صورت موازی) درخواست PUT /upload/{session_id}/{chunk_index} با بدنه‌ی خام داده ارسال می کنه.
    سرور پس از ذخیره، وضعیت بلوک (دریافت شده) را در یک فایل JSON به‌روزرسانی می کنه.
5. توقف و ادامه:

    هنگام توقف، کلاینت از سرور می‌خواهد متادیتای بلوک‌های دریافت‌شده را با GET /status/{session_id}.
    کلاینت بلوک‌هایی که دریافت نشده‌اند را مجدداً ارسال می کنه.
    اگر فایل بین توقف و ادامه تغییر کرده باشد، هش جدید بلوک‌ها متفاوت است؛ در نتیجه بلوک‌های تغییریافته مجدداً آپلود می‌شوند و بلوک‌های بدون تغییر لازم نیست.
6. نهایی‌سازی:

    پس از ارسال همه بلوک‌ها، کلاینت POST /finish/{session_id} را فراخوانی می کنه.
    سرور بلوک‌ها را به ترتیب به هم متصل و فایل نهایی را در محل دائمی ذخیره می کنه.
    متادیتای session پاک یا به آرشیو منتقل می‌بشه.
7. حذف خودکار:

    کرون‌جابی روی سرور هر ۶ ساعت اجرا می‌بشه و sessionهایی را که بیش از ۳ روز از start_time گذشته، همراه با بلوک‌های ناقص پاک می کنه.


 3. نمونه سادهٔ پیاده‌سازی

در ادامه یک سرور بسیار ساده با Flask و کلاینت با Requests ارائه شده است. این دمو روی یک فایل sample.bin با بلوک‌های 1MiB کار می کنه.

 3.1. کد سرور (server.py)


from flask import Flask, request, jsonify, send_file
import os, hashlib, json, time

app = Flask(__name__)
BASE = 'uploads'
os.makedirs(BASE, exist_ok=True)
CRON_THRESHOLD = 3  24  3600   3 days

 پاک‌سازی قدیمی‌ها
@app.before_request
def cleanup():
    now = time.time()
    for sid in os.listdir(BASE):
        meta = os.path.join(BASE, sid, 'meta.json')
        if os.path.exists(meta):
            data = json.load(open(meta))
            if now - data['start'] > CRON_THRESHOLD:
                os.system(f"rm -rf {os.path.join(BASE, sid)}")

@app.route('/start', methods=['POST'])
def start():
    sid = hashlib.sha1(str(time.time()).encode()).hexdigest()
    path = os.path.join(BASE, sid)
    os.makedirs(path)
    meta = {'start': time.time(), 'received': []}
    json.dump(meta, open(os.path.join(path, 'meta.json'), 'w'))
    return jsonify(session_id=sid)

@app.route('/upload/<sid>/<int:idx>', methods=['PUT'])
def upload_chunk(sid, idx):
    path = os.path.join(BASE, sid)
    chunk = request.data
    open(os.path.join(path, f"chunk.{idx}"), 'wb').write(chunk)
    meta = json.load(open(os.path.join(path, 'meta.json')))
    if idx not in meta['received']:
        meta['received'].append(idx)
        json.dump(meta, open(os.path.join(path, 'meta.json'), 'w'))
    return '', 200

@app.route('/status/<sid>')
def status(sid):
    meta = json.load(open(os.path.join(BASE, sid, 'meta.json')))
    return jsonify(received=meta['received'])

@app.route('/finish/<sid>')
def finish(sid):
    path = os.path.join(BASE, sid)
    chunks = sorted([c for c in os.listdir(path) if c.startswith('chunk.')],
                    key=lambda x: int(x.split('.')[1]))
    out = open(os.path.join(BASE, f"{sid}.final"), 'wb')
    for c in chunks:
        out.write(open(os.path.join(path, c), 'rb').read())
    out.close()
    return send_file(os.path.join(BASE, f"{sid}.final"), as_attachment=True)

if __name__ == '__main__':
    app.run(port=5000)





 3.2. کد کلاینت (client.py)


import requests, hashlib, os, math

FILE = 'sample.bin'
CHUNK = 10241024
srv = 'http://localhost:5000'

 شروع جلسه
r = requests.post(f"{srv}/start")
session = r.json()['session_id']

 تقسیم و آپلود
size = os.path.getsize(FILE)
total = math.ceil(size/CHUNK)

with open(FILE, 'rb') as f:
    for idx in range(total):
        data = f.read(CHUNK)
        r = requests.put(f"{srv}/upload/{session}/{idx}", data=data)
        print(f"chunk {idx}: {r.status_code}")

 نهایی‌سازی
r = requests.post(f"{srv}/finish/{session}")
open('downloaded.bin', 'wb').write(r.content)
print('Done')


نحوهٔ اجرا اینوریه

1. یک فایل sample.bin تصادفی بساز: dd if=/dev/urandom of=sample.bin bs=1M count=5
2. python server.py را اجرا کن.
3. python client.py را اجرا کن؛ خروجی downloaded.bin باید با sample.bin یکسان باشد.
