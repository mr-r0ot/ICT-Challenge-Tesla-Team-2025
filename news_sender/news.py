import os
import json
import requests
from bs4 import BeautifulSoup
from datetime import datetime
import customtkinter as ctk
from tkinter import Toplevel, Text, END, messagebox
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.cron import CronTrigger
import smtplib
import webbrowser

# -------------------- Configuration --------------------
CONFIG_PATH = 'config.json'
SEND_FILE = 'send.html'

def load_config():
    if not os.path.exists(CONFIG_PATH):
        default = {
            "smtp": {
                "server": "smtp.mailtrap.io",
                "port": 587,
                "user": "",
                "pass": ""
            }
        }
        with open(CONFIG_PATH, 'w', encoding='utf-8') as f:
            json.dump(default, f, ensure_ascii=False, indent=4)
    with open(CONFIG_PATH, 'r', encoding='utf-8') as f:
        return json.load(f)

config = load_config()
smtp_cfg = config.get('smtp', {})
SMTP_SERVER = smtp_cfg.get('server')
SMTP_PORT = smtp_cfg.get('port')
SMTP_USER = smtp_cfg.get('user')
SMTP_PASS = smtp_cfg.get('pass')

# -------------------- Fetch News --------------------
def fetch_news(query, max_items=10):
    url = f"https://www.isna.ir/search?q={query}"
    headers = {'User-Agent': 'Mozilla/5.0'}
    try:
        resp = requests.get(url, headers=headers)
        resp.raise_for_status()
        soup = BeautifulSoup(resp.content, 'html.parser')
        container = soup.select_one('section.box.card.horizontal.full-card')
        if not container:
            return []
        articles = []
        for li in container.select('div.items > ul > li')[:max_items]:
            title_tag = li.select_one('h3 a')
            if not title_tag:
                continue
            title = title_tag.get_text(strip=True)
            link = title_tag['href']
            if not link.startswith('http'):
                link = f"https://www.isna.ir{link}"
            date_tag = li.select_one('time a')
            date = date_tag.get_text(strip=True) if date_tag else ''
            img_tag = li.select_one('figure img')
            img_url = img_tag['src'] if img_tag else None
            snippet = ' '.join(p.get_text(strip=True) for p in li.select('div.desc > p'))
            articles.append({
                'title': title,
                'link': link,
                'date': date,
                'snippet': snippet,
                'image_url': img_url
            })
        return articles
    except Exception as e:
        print(f"Error fetching news: {e}")
        return []

# -------------------- Build HTML --------------------
def build_html(articles, name, status=None):
    parts = [
        f"<h2>بولتن خبری {name} - {datetime.now().strftime('%Y/%m/%d %H:%M')}</h2>",
        "<ul style='list-style:none;'>"
    ]
    for art in articles:
        img_html = f"<img src='{art['image_url']}' width='100'/><br/>" if art['image_url'] else ''
        snippet_html = f"<p>{art['snippet']}</p>" if art['snippet'] else ''
        parts.append(
            f"<li><a href='{art['link']}'>{art['title']}</a> ({art['date']})<br/>{img_html}{snippet_html}</li>"
        )
    parts.append("</ul>")
    if status:
        parts.append(f"<p><strong>نتیجه ارسال ایمیل: {status}</strong></p>")
    return ''.join(parts)

# -------------------- Save and Open --------------------
def save_and_open_html(html_content):
    with open(SEND_FILE, 'w', encoding='utf-8') as f:
        f.write(html_content)
    webbrowser.open(f"file://{os.path.abspath(SEND_FILE)}")

# -------------------- Send Email --------------------
def send_email(to_email, subject, html_content):
    msg = MIMEMultipart('alternative')
    msg['Subject'] = subject
    msg['From'] = SMTP_USER
    msg['To'] = to_email
    msg.attach(MIMEText(html_content, 'html'))
    try:
        with smtplib.SMTP(SMTP_SERVER, SMTP_PORT) as server:
            server.login(SMTP_USER, SMTP_PASS)
            server.sendmail(msg['From'], [to_email], msg.as_string())
        return True
    except Exception as e:
        print(f"Error sending email: {e}")
        return False

# -------------------- Bulletin Execution --------------------
def execute_bulletin(name, email):
    articles = fetch_news(name)
    if not articles:
        messagebox.showinfo("اطلاع", "هیچ خبری یافت نشد.")
        return
    html_before = build_html(articles, name)
    save_and_open_html(html_before)
    success = send_email(email, f"بولتن خبری: {name}", html_before)
    status = "موفق" if success else "ناموفق"
    html_after = build_html(articles, name, status)
    save_and_open_html(html_after)

# -------------------- Scheduler --------------------
scheduler = BackgroundScheduler()
scheduler.start()

def schedule_job(name, email, sched_type, time_str, weekdays=None, monthly_date=None):
    hour, minute = map(int, time_str.split(':'))
    if sched_type == 'daily':
        trigger = CronTrigger(hour=hour, minute=minute)
    elif sched_type == 'weekly':
        dow = ','.join(weekdays or [])
        trigger = CronTrigger(day_of_week=dow, hour=hour, minute=minute)
    else:
        day = int(monthly_date.split('/')[-1])
        trigger = CronTrigger(day=day, hour=hour, minute=minute)
    scheduler.add_job(lambda: execute_bulletin(name, email), trigger, id=f"job_{name}_{email}", replace_existing=True)

# -------------------- GUI Setup --------------------
ctk.set_appearance_mode('System')
ctk.set_default_color_theme('blue')
app = ctk.CTk()
app.title('News Bulletin Scheduler')
app.geometry('600x700')

# Edit SMTP Config
def open_config_editor():
    win = Toplevel(app)
    win.title('ویرایش تنظیمات ایمیل')
    text = Text(win, width=60, height=20)
    text.pack(padx=10, pady=10)
    with open(CONFIG_PATH, 'r', encoding='utf-8') as f:
        text.insert(END, f.read())
    def save_cfg():
        try:
            data = text.get('1.0', END)
            json.loads(data)
            with open(CONFIG_PATH, 'w', encoding='utf-8') as f:
                f.write(data)
            messagebox.showinfo('موفق', 'ذخیره شد')
            win.destroy()
        except Exception as e:
            messagebox.showerror('خطا', f'JSON نامعتبر: {e}')
    ctk.CTkButton(win, text='ذخیره', command=save_cfg).pack(pady=5)

ctk.CTkButton(app, text='ویرایش ایمیل', command=open_config_editor).place(x=10, y=10)

# User Inputs
name_var = ctk.StringVar()
email_var = ctk.StringVar()
sched_var = ctk.StringVar(value='daily')
time_var = ctk.StringVar()
week_vars = {d: ctk.BooleanVar() for d in ['mon','tue','wed','thu','fri','sat','sun']}
month_var = ctk.StringVar(value='1403/05/22')

ctk.CTkLabel(app, text='نام/شرکت:').pack(pady=5)
ctk.CTkEntry(app, textvariable=name_var).pack(pady=5)
ctk.CTkLabel(app, text='ایمیل:').pack(pady=5)
ctk.CTkEntry(app, textvariable=email_var).pack(pady=5)

ctk.CTkLabel(app, text='نوع زمان‌بندی:').pack(pady=5)
ctk.CTkOptionMenu(app, variable=sched_var, values=['daily','weekly','monthly']).pack(pady=5)
ctk.CTkLabel(app, text='ساعت HH:MM:').pack(pady=5)
ctk.CTkEntry(app, textvariable=time_var).pack(pady=5)

# Weekly/Monthly Frames
week_frame = ctk.CTkFrame(app)
for d, var in week_vars.items(): ctk.CTkCheckBox(week_frame, text=d, variable=var).pack(side='left', padx=5)
month_frame = ctk.CTkFrame(app)
ctk.CTkLabel(month_frame, text='تاریخ yyyy/mm/dd:').pack(side='left')
ctk.CTkEntry(month_frame, textvariable=month_var, width=100).pack(side='left', padx=5)

def update_frames(*args):
    week_frame.pack_forget()
    month_frame.pack_forget()
    if sched_var.get() == 'weekly':
        week_frame.pack(pady=5)
    elif sched_var.get() == 'monthly':
        month_frame.pack(pady=5)

sched_var.trace('w', update_frames)
update_frames()

# Info Label and Schedule Button
info_label = ctk.CTkLabel(app, text='')
info_label.pack(pady=10)

def on_schedule():
    schedule_job(
        name_var.get(), email_var.get(), sched_var.get(), time_var.get(),
        [d for d, v in week_vars.items() if v.get()], month_var.get()
    )
    info_label.configure(text='زمان‌بندی انجام شد؛ send.html روی سیستم باز می‌شود و ایمیل ارسال می‌شود.')

ctk.CTkButton(app, text='ثبت زمان‌بندی', command=on_schedule).pack(pady=15)

app.mainloop()