<div dir="rtl" align="center">

# AristaPanel


[![Telegram](https://img.shields.io/badge/@aristapanel-229ED9?style=for-the-badge&logo=telegram&logoColor=white)](https://t.me/aristapanel)
[![Web Panel](https://img.shields.io/badge/Web_Panel-F38020?style=for-the-badge&logo=cloudflare&logoColor=white)](https://arista-panel.arista-panel.workers.dev/)

---

سیستم خودکار استخراج، اعتبارسنجی، دسته‌بندی و ترکیب کانفیگ‌های پروکسی از منابع عمومی تلگرام و گیت‌هاب.

---

## معماری سیستم

  پروژه تماماً خودکار است که هر ۶ ساعت یکبار اجرا می‌شود. ورودی‌ها شامل ۵۰۰+ کانال تلگرامی و ۱۰+ مخزن گیت‌هاب هستند. خروجی نهایی به صورت فایل‌های متنی دسته‌بندی شده در مخزن ذخیره می‌گردد.

### مؤلفه‌ها

1. **telegram_extractor.py**  
   اسکرپ کانال‌های عمومی با فرمت t.me/s/… استخراج محتوای متنی، شناسایی الگوهای پروکسی با regex، اعتبارسنجی ساختار هر کانفیگ (بررسی UUID، پورت، فرمت encoding). کانال‌هایی که بیش از ۴۸ ساعت پست جدید ندارند به حالت تعلیق ۷ روزه می‌روند. کانال‌هایی که ۳ بار متوالی پاسخ نمی‌دهند به مدت ۲۴ ساعت در کش مرده قرار می‌گیرند.

2. **github_extractor.py**  
   دریافت مستقیم فایل‌های خام از ۱۰ سورس مختلف شامل raw.githubusercontent.com، cdn.jsdelivr.net، gitverse.ru. پشتیبانی از فرمت‌های vmess://, vless://, trojan://, ss://, hysteria2://, tuic://. استانداردسازی خودکار لینک‌های ss:// با فرمت نامعتبر.

3. **combine_configs.py**  
   ادغام خروجی دو استخراج‌کننده، حذف دایپلیکیت با الگوریتم هش MD5، تولید ساختار تیربندی با همپوشانی ۱۰ تایی بین تیرهای متوالی. تیرها شامل ۵۰، ۱۰۰، ۱۵۰، ۲۰۰، ۲۵۰، ۳۰۰، ۴۰۰، ۵۰۰ و ALL هستند.

4. **GitHub Actions (main.yml)**  
   زمانبندی cron */6 * * * *، تاخیر تصادفی ۶۰ تا ۳۶۰ ثانیه برای جلوگیری از rate limit، commit و push خودکار تنها در صورت وجود تغییر.

---

## مدیریت کانال‌های مرده

سیستم به صورت خودکار وضعیت هر کانال را ردیابی می‌کند:

| وضعیت | شرط | اقدام | مدت |
|--------|------|--------|------|
| تعلیق موقت | آخرین پست > ۴۸ ساعت | توقف اسکرپ | ۷ روز |
| کش مرده | ۳ بار متوالی فیلتر | توقف اسکرپ | ۲۴ ساعت |
| بلاک دائم | پس از ۷ روز تعلیق بدون فعالیت | حذف از چرخه | دائم |

فایل‌های وضعیت در مسیر configs/telegram/ ذخیره می‌شوند:

- dead_cache.json
- permanent_blacklist.json
- temp_suspend.json
- last_seen.json

---

## ساختار خروجی

پس از هر اجرا، فایل‌های زیر تولید می‌شوند:

configs/
├── telegram/
│   ├── vmess.txt
│   ├── vless.txt
│   ├── trojan.txt
│   ├── ss.txt
│   ├── hysteria2.txt
│   ├── tuic.txt
│   ├── all.txt
│   ├── vmess/50.txt, 100.txt, ...
│   └── ALL/50.txt, 100.txt, ...
├── github/
│   └── (همان ساختار)
└── combined/
    └── (ادغام دو منبع با ذکر تعداد هرکدام در هدر فایل)

هر فایل پوشه شامل همپوشانی ۱۰ تایی با پوشه قبلی است. مثال: فایل ۱۰۰ تایی شامل ۱۰ کانفیگ انتهایی فایل ۵۰ تایی به اضافه ۹۰ کانفیگ جدید.

---

## اعتبارسنجی کانفیگ‌ها

سیستم قبل از ذخیره هر کانفیگ، موارد زیر را بررسی می‌کند:

- پروتکل vmess: وجود فیلدهای v, ps, add, port, id, aid + اعتبار UUID + محدوده پورت ۱-۶۵۵۳۵
- پروتکل vless/trojan: وجود کاراکترهای @ و # در رشته
- پروتکل ss: اعتبار base64 encoding + وجود : پس از دیکد + اعتبار پورت
- سایر پروتکل‌ها: تطابق با الگوی پروتکل و عدم وجود کاراکترهای مخرب

کانفیگ‌های نامعتبر حذف می‌شوند. تعداد آنها در لاگ نهایی گزارش می‌گردد.

---

## کانال تلگرام

تمامی لینک‌های سابسکریپشن، پروکسی‌های تلگرام (MTProto)، آیپی‌های تمیز کلادفلر اسکن شده از صدها میلیون آیپی، و کانفیگ‌های به‌روز روزانه فقط در کانال تلگرام ارائه می‌شوند.

لینک سابسکریپشن در این مخزن گیت‌هاب قرار ندارد.
جهت دسترسی راحت به لینک‌های سابسکراپشن به کانال تلگرام ما بپیوندید.
https://t.me/aristapanel

---

## پنل عمومی

برای شخصی‌سازی خروجی، فیلتر بر اساس پروتکل، دریافت سابسکریپشن اختصاصی و بهینه‌سازی کانفیگ‌ها می‌توانید از پنل عمومی استفاده کنید. این پنل روی Cloudflare Workers پیاده‌سازی شده و کاملاً رایگان است.

https://arista-panel.arista-panel.workers.dev/

---

## 📥 لینک‌های دسترسی به کانفیگ‌ها و قابل استفاده در کلاینت‌های محبوب: V2rayNG, Hiddify, NekoBox , ...

### 🚀 مجموعه کانفیگ‌های تلگرام | پنل آریستا

| تعداد | لینک دانلود |
|-------|------------|
| 📌 ۵۰ کانفیگ | [دانلود](https://cdn.jsdelivr.net/gh/aristapanell-cell/AriataPanel@main/configs/telegram/ALL/50.txt) |
| 📌 ۱۰۰ کانفیگ | [دانلود](https://cdn.jsdelivr.net/gh/aristapanell-cell/AriataPanel@main/configs/telegram/ALL/100.txt) |
| 📌 ۱۵۰ کانفیگ | [دانلود](https://cdn.jsdelivr.net/gh/aristapanell-cell/AriataPanel@main/configs/telegram/ALL/150.txt) |
| 📌 ۲۰۰ کانفیگ | [دانلود](https://cdn.jsdelivr.net/gh/aristapanell-cell/AriataPanel@main/configs/telegram/ALL/200.txt) |
| 📌 ۲۵۰ کانفیگ | [دانلود](https://cdn.jsdelivr.net/gh/aristapanell-cell/AriataPanel@main/configs/telegram/ALL/250.txt) |
| 📌 ۳۰۰ کانفیگ | [دانلود](https://cdn.jsdelivr.net/gh/aristapanell-cell/AriataPanel@main/configs/telegram/ALL/300.txt) |
| 📌 ۴۰۰ کانفیگ | [دانلود](https://cdn.jsdelivr.net/gh/aristapanell-cell/AriataPanel@main/configs/telegram/ALL/400.txt) |
| 📌 ۵۰۰ کانفیگ | [دانلود](https://cdn.jsdelivr.net/gh/aristapanell-cell/AriataPanel@main/configs/telegram/ALL/500.txt) |
| 🌍 تمامی کانفیگ‌ها | [دانلود](https://cdn.jsdelivr.net/gh/aristapanell-cell/AriataPanel@main/configs/telegram/ALL/ALL.txt) |

---

### 🚀 مجموعه کانفیگ‌های گیت‌هاب | پنل آریستا

| تعداد | لینک دانلود |
|-------|------------|
| 📌 ۵۰ کانفیگ | [دانلود](https://cdn.jsdelivr.net/gh/aristapanell-cell/AriataPanel@main/configs/github/ALL/50.txt) |
| 📌 ۱۰۰ کانفیگ | [دانلود](https://cdn.jsdelivr.net/gh/aristapanell-cell/AriataPanel@main/configs/github/ALL/100.txt) |
| 📌 ۱۵۰ کانفیگ | [دانلود](https://cdn.jsdelivr.net/gh/aristapanell-cell/AriataPanel@main/configs/github/ALL/150.txt) |
| 📌 ۲۰۰ کانفیگ | [دانلود](https://cdn.jsdelivr.net/gh/aristapanell-cell/AriataPanel@main/configs/github/ALL/200.txt) |
| 📌 ۲۵۰ کانفیگ | [دانلود](https://cdn.jsdelivr.net/gh/aristapanell-cell/AriataPanel@main/configs/github/ALL/250.txt) |
| 📌 ۳۰۰ کانفیگ | [دانلود](https://cdn.jsdelivr.net/gh/aristapanell-cell/AriataPanel@main/configs/github/ALL/300.txt) |
| 📌 ۴۰۰ کانفیگ | [دانلود](https://cdn.jsdelivr.net/gh/aristapanell-cell/AriataPanel@main/configs/github/ALL/400.txt) |
| 📌 ۵۰۰ کانفیگ | [دانلود](https://cdn.jsdelivr.net/gh/aristapanell-cell/AriataPanel@main/configs/github/ALL/500.txt) |
| 🌍 تمامی کانفیگ‌ها | [دانلود](https://cdn.jsdelivr.net/gh/aristapanell-cell/AriataPanel@main/configs/github/ALL/ALL.txt) |

---

### 🚀 مجموعه کانفیگ‌های ترکیبی تلگرام + گیت‌هاب | پنل آریستا

| تعداد | لینک دانلود |
|-------|------------|
| 📌 ۵۰ کانفیگ | [دانلود](https://cdn.jsdelivr.net/gh/aristapanell-cell/AriataPanel@main/configs/combined/ALL/50.txt) |
| 📌 ۱۰۰ کانفیگ | [دانلود](https://cdn.jsdelivr.net/gh/aristapanell-cell/AriataPanel@main/configs/combined/ALL/100.txt) |
| 📌 ۱۵۰ کانفیگ | [دانلود](https://cdn.jsdelivr.net/gh/aristapanell-cell/AriataPanel@main/configs/combined/ALL/150.txt) |
| 📌 ۲۰۰ کانفیگ | [دانلود](https://cdn.jsdelivr.net/gh/aristapanell-cell/AriataPanel@main/configs/combined/ALL/200.txt) |
| 📌 ۲۵۰ کانفیگ | [دانلود](https://cdn.jsdelivr.net/gh/aristapanell-cell/AriataPanel@main/configs/combined/ALL/250.txt) |
| 📌 ۳۰۰ کانفیگ | [دانلود](https://cdn.jsdelivr.net/gh/aristapanell-cell/AriataPanel@main/configs/combined/ALL/300.txt) |
| 📌 ۴۰۰ کانفیگ | [دانلود](https://cdn.jsdelivr.net/gh/aristapanell-cell/AriataPanel@main/configs/combined/ALL/400.txt) |
| 📌 ۵۰۰ کانفیگ | [دانلود](https://cdn.jsdelivr.net/gh/aristapanell-cell/AriataPanel@main/configs/combined/ALL/500.txt) |
| 🌍 تمامی کانفیگ‌ها | [دانلود](https://cdn.jsdelivr.net/gh/aristapanell-cell/AriataPanel@main/configs/combined/ALL/ALL.txt) |

</div>

---

<div dir="rtl" align="center">

ساخته شده توسط تیم آریستا (🇲‌🇲‌🇩‌)❤️

---
