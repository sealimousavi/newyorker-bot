# 🗞️ New Yorker Cover Bot

یه تلگرام بات که نزدیک‌ترین جلد مجله‌ی New Yorker به تاریخ تولد شما رو پیدا می‌کنه.

## راه‌اندازی

### ۱. نصب وابستگی‌ها
```bash
pip install -r requirements.txt
```

### ۲. تنظیم متغیرهای محیطی
فایل `.env.example` رو کپی کن و مقادیر رو پر کن:
```bash
cp .env.example .env
```

سپس توکن بات تلگرامت رو از [@BotFather](https://t.me/BotFather) بگیر و توی `.env` بذار.

### ۳. اجرا
ابتدا API رو اجرا کن:
```bash
python api.py
```

سپس در یه ترمینال جداگانه بات رو اجرا کن:
```bash
python bot.py
```

## ساختار پروژه
```
.
├── api.py           # Flask API - پیدا کردن نزدیک‌ترین جلد
├── bot.py           # تلگرام بات
├── all_covers.json  # دیتای جلدهای مجله
├── requirements.txt
├── .env.example     # نمونه‌ی متغیرهای محیطی
└── .gitignore
```
