<div dir="rtl" align="center">

# ⚡ AristaPanel ⚡

> **سیستم خودکار استخراج، اعتبارسنجی، دسته‌بندی و ترکیب کانفیگ‌های پروکسی از منابع عمومی تلگرام و گیت‌هاب**

[![Telegram](https://img.shields.io/badge/Telegram-229ED9?style=for-the-badge&logo=telegram&logoColor=white)](https://t.me/aristapanel)
[![YouTube](https://img.shields.io/badge/YouTube-FF0000?style=for-the-badge&logo=youtube&logoColor=white)](https://youtube.com/@aristaproject-m3o?si)
[![Element](https://img.shields.io/badge/Element-0DBD8B?style=for-the-badge&logo=element&logoColor=white)](https://matrix.to/#/%23aristaproject:matrix.org)
[![Web Panel](https://img.shields.io/badge/Web_Panel-F38020?style=for-the-badge&logo=cloudflare&logoColor=white)](https://arista-panel.arista-panel.workers.dev/)

---

## 🧩 معماری سیستم

| مؤلفه | توضیحات |
|-------|---------|
| **📡 telegram_extractor.py** | اسکرپ کانال‌های عمومی، استخراج محتوای متنی، شناسایی الگوهای پروکسی با regex، اعتبارسنجی ساختار هر کانفیگ |
| **🐙 github_extractor.py** | دریافت مستقیم فایل‌های خام از ۱۰ سورس مختلف، پشتیبانی از vmess://, vless://, trojan://, ss://, hysteria2://, tuic:// |
| **🔗 combine_configs.py** | ادغام خروجی دو استخراج‌کننده، حذف دایپلیکیت با MD5، تولید ساختار تیربندی با همپوشانی ۱۰ تایی |
| **⚙️ GitHub Actions** | زمانبندی `*/6 * * * *`، commit و push خودکار |

---

## 🚦 مدیریت کانال‌های مرده

| وضعیت | شرط | اقدام | مدت |
|--------|------|--------|------|
| تعلیق موقت | آخرین پست > ۴۸ ساعت | توقف اسکرپ | ۷ روز |
| کش مرده | ۳ بار متوالی فیلتر | توقف اسکرپ | ۲۴ ساعت |
| بلاک دائم | پس از ۷ روز تعلیق بدون فعالیت | حذف از چرخه | دائم |

**📂 فایل‌های وضعیت:** `configs/telegram/`

---

## 🔍 اعتبارسنجی کانفیگ‌ها

| پروتکل | بررسی‌ها |
|--------|---------|
| **vmess** | وجود فیلدهای `v, ps, add, port, id, aid` + اعتبار UUID + محدوده پورت |
| **vless / trojan** | وجود کاراکترهای `@` و `#` در رشته |
| **ss** | اعتبار base64 encoding + وجود `:` پس از دیکد |
| **سایر** | تطابق با الگوی پروتکل و عدم وجود کاراکترهای مخرب |

---

## 📢 کانال تلگرام

تمامی لینک‌های **سابسکریپشن**، **پروکسی‌های تلگرام (MTProto)**، **آیپی‌های تمیز کلادفلر** و کانفیگ‌های به‌روز روزانه در کانال تلگرام ارائه می‌شوند.

👉 [https://t.me/aristapanel](https://t.me/aristapanel)

---

## 🌐 پنل عمومی

برای **شخصی‌سازی خروجی**، **فیلتر بر اساس پروتکل**، **دریافت سابسکریپشن اختصاصی** از پنل عمومی استفاده کنید.

👉 [https://arista-panel.arista-panel.workers.dev/](https://arista-panel.arista-panel.workers.dev/)

---

## 📥 لینک‌های دسترسی به کانفیگ‌ها

### 🔹 کلاینت‌های محبوب: V2rayNG, Hiddify, NekoBox, ...

#### 📌 تلگرام

| تعداد | لینک دانلود |
|-------|------------|
| ۵۰ کانفیگ | [دانلود](https://cdn.jsdelivr.net/gh/aristapanell-cell/AriataPanel@main/configs/telegram/ALL/50.txt) |
| ۱۰۰ کانفیگ | [دانلود](https://cdn.jsdelivr.net/gh/aristapanell-cell/AriataPanel@main/configs/telegram/ALL/100.txt) |
| ۱۵۰ کانفیگ | [دانلود](https://cdn.jsdelivr.net/gh/aristapanell-cell/AriataPanel@main/configs/telegram/ALL/150.txt) |
| ۲۰۰ کانفیگ | [دانلود](https://cdn.jsdelivr.net/gh/aristapanell-cell/AriataPanel@main/configs/telegram/ALL/200.txt) |
| ۲۵۰ کانفیگ | [دانلود](https://cdn.jsdelivr.net/gh/aristapanell-cell/AriataPanel@main/configs/telegram/ALL/250.txt) |
| ۳۰۰ کانفیگ | [دانلود](https://cdn.jsdelivr.net/gh/aristapanell-cell/AriataPanel@main/configs/telegram/ALL/300.txt) |
| ۴۰۰ کانفیگ | [دانلود](https://cdn.jsdelivr.net/gh/aristapanell-cell/AriataPanel@main/configs/telegram/ALL/400.txt) |
| ۵۰۰ کانفیگ | [دانلود](https://cdn.jsdelivr.net/gh/aristapanell-cell/AriataPanel@main/configs/telegram/ALL/500.txt) |
| تمامی کانفیگ‌ها | [دانلود](https://cdn.jsdelivr.net/gh/aristapanell-cell/AriataPanel@main/configs/telegram/ALL/ALL.txt) |

#### 📌 گیت‌هاب

| تعداد | لینک دانلود |
|-------|------------|
| ۵۰ کانفیگ | [دانلود](https://cdn.jsdelivr.net/gh/aristapanell-cell/AriataPanel@main/configs/github/ALL/50.txt) |
| ۱۰۰ کانفیگ | [دانلود](https://cdn.jsdelivr.net/gh/aristapanell-cell/AriataPanel@main/configs/github/ALL/100.txt) |
| ۱۵۰ کانفیگ | [دانلود](https://cdn.jsdelivr.net/gh/aristapanell-cell/AriataPanel@main/configs/github/ALL/150.txt) |
| ۲۰۰ کانفیگ | [دانلود](https://cdn.jsdelivr.net/gh/aristapanell-cell/AriataPanel@main/configs/github/ALL/200.txt) |
| ۲۵۰ کانفیگ | [دانلود](https://cdn.jsdelivr.net/gh/aristapanell-cell/AriataPanel@main/configs/github/ALL/250.txt) |
| ۳۰۰ کانفیگ | [دانلود](https://cdn.jsdelivr.net/gh/aristapanell-cell/AriataPanel@main/configs/github/ALL/300.txt) |
| ۴۰۰ کانفیگ | [دانلود](https://cdn.jsdelivr.net/gh/aristapanell-cell/AriataPanel@main/configs/github/ALL/400.txt) |
| ۵۰۰ کانفیگ | [دانلود](https://cdn.jsdelivr.net/gh/aristapanell-cell/AriataPanel@main/configs/github/ALL/500.txt) |
| تمامی کانفیگ‌ها | [دانلود](https://cdn.jsdelivr.net/gh/aristapanell-cell/AriataPanel@main/configs/github/ALL/ALL.txt) |

#### 📌 ترکیبی (تلگرام + گیت‌هاب)

| تعداد | لینک دانلود |
|-------|------------|
| ۵۰ کانفیگ | [دانلود](https://cdn.jsdelivr.net/gh/aristapanell-cell/AriataPanel@main/configs/combined/ALL/50.txt) |
| ۱۰۰ کانفیگ | [دانلود](https://cdn.jsdelivr.net/gh/aristapanell-cell/AriataPanel@main/configs/combined/ALL/100.txt) |
| ۱۵۰ کانفیگ | [دانلود](https://cdn.jsdelivr.net/gh/aristapanell-cell/AriataPanel@main/configs/combined/ALL/150.txt) |
| ۲۰۰ کانفیگ | [دانلود](https://cdn.jsdelivr.net/gh/aristapanell-cell/AriataPanel@main/configs/combined/ALL/200.txt) |
| ۲۵۰ کانفیگ | [دانلود](https://cdn.jsdelivr.net/gh/aristapanell-cell/AriataPanel@main/configs/combined/ALL/250.txt) |
| ۳۰۰ کانفیگ | [دانلود](https://cdn.jsdelivr.net/gh/aristapanell-cell/AriataPanel@main/configs/combined/ALL/300.txt) |
| ۴۰۰ کانفیگ | [دانلود](https://cdn.jsdelivr.net/gh/aristapanell-cell/AriataPanel@main/configs/combined/ALL/400.txt) |
| ۵۰۰ کانفیگ | [دانلود](https://cdn.jsdelivr.net/gh/aristapanell-cell/AriataPanel@main/configs/combined/ALL/500.txt) |
| تمامی کانفیگ‌ها | [دانلود](https://cdn.jsdelivr.net/gh/aristapanell-cell/AriataPanel@main/configs/combined/ALL/ALL.txt) |

---

### 🔹 SingBox

#### 📌 تلگرام

| تعداد | لینک دانلود |
|-------|------------|
| ۵۰ کانفیگ | [دانلود](https://cdn.jsdelivr.net/gh/aristapanell-cell/AriataPanel@main/config.json/telegram/ALL/50.json) |
| ۱۰۰ کانفیگ | [دانلود](https://cdn.jsdelivr.net/gh/aristapanell-cell/AriataPanel@main/config.json/telegram/ALL/100.json) |
| ۱۵۰ کانفیگ | [دانلود](https://cdn.jsdelivr.net/gh/aristapanell-cell/AriataPanel@main/config.json/telegram/ALL/150.json) |
| ۲۰۰ کانفیگ | [دانلود](https://cdn.jsdelivr.net/gh/aristapanell-cell/AriataPanel@main/config.json/telegram/ALL/200.json) |
| ۲۵۰ کانفیگ | [دانلود](https://cdn.jsdelivr.net/gh/aristapanell-cell/AriataPanel@main/config.json/telegram/ALL/250.json) |
| ۳۰۰ کانفیگ | [دانلود](https://cdn.jsdelivr.net/gh/aristapanell-cell/AriataPanel@main/config.json/telegram/ALL/300.json) |
| ۴۰۰ کانفیگ | [دانلود](https://cdn.jsdelivr.net/gh/aristapanell-cell/AriataPanel@main/config.json/telegram/ALL/400.json) |
| ۵۰۰ کانفیگ | [دانلود](https://cdn.jsdelivr.net/gh/aristapanell-cell/AriataPanel@main/config.json/telegram/ALL/500.json) |
| تمامی کانفیگ‌ها | [دانلود](https://cdn.jsdelivr.net/gh/aristapanell-cell/AriataPanel@main/config.json/telegram/ALL/ALL.json) |

#### 📌 گیت‌هاب

| تعداد | لینک دانلود |
|-------|------------|
| ۵۰ کانفیگ | [دانلود](https://cdn.jsdelivr.net/gh/aristapanell-cell/AriataPanel@main/config.json/github/ALL/50.json) |
| ۱۰۰ کانفیگ | [دانلود](https://cdn.jsdelivr.net/gh/aristapanell-cell/AriataPanel@main/config.json/github/ALL/100.json) |
| ۱۵۰ کانفیگ | [دانلود](https://cdn.jsdelivr.net/gh/aristapanell-cell/AriataPanel@main/config.json/github/ALL/150.json) |
| ۲۰۰ کانفیگ | [دانلود](https://cdn.jsdelivr.net/gh/aristapanell-cell/AriataPanel@main/config.json/github/ALL/200.json) |
| ۲۵۰ کانفیگ | [دانلود](https://cdn.jsdelivr.net/gh/aristapanell-cell/AriataPanel@main/config.json/github/ALL/250.json) |
| ۳۰۰ کانفیگ | [دانلود](https://cdn.jsdelivr.net/gh/aristapanell-cell/AriataPanel@main/config.json/github/ALL/300.json) |
| ۴۰۰ کانفیگ | [دانلود](https://cdn.jsdelivr.net/gh/aristapanell-cell/AriataPanel@main/config.json/github/ALL/400.json) |
| ۵۰۰ کانفیگ | [دانلود](https://cdn.jsdelivr.net/gh/aristapanell-cell/AriataPanel@main/config.json/github/ALL/500.json) |
| تمامی کانفیگ‌ها | [دانلود](https://cdn.jsdelivr.net/gh/aristapanell-cell/AriataPanel@main/config.json/github/ALL/ALL.json) |

#### 📌 ترکیبی (تلگرام + گیت‌هاب)

| تعداد | لینک دانلود |
|-------|------------|
| ۵۰ کانفیگ | [دانلود](https://cdn.jsdelivr.net/gh/aristapanell-cell/AriataPanel@main/config.json/combined/ALL/50.json) |
| ۱۰۰ کانفیگ | [دانلود](https://cdn.jsdelivr.net/gh/aristapanell-cell/AriataPanel@main/config.json/combined/ALL/100.json) |
| ۱۵۰ کانفیگ | [دانلود](https://cdn.jsdelivr.net/gh/aristapanell-cell/AriataPanel@main/config.json/combined/ALL/150.json) |
| ۲۰۰ کانفیگ | [دانلود](https://cdn.jsdelivr.net/gh/aristapanell-cell/AriataPanel@main/config.json/combined/ALL/200.json) |
| ۲۵۰ کانفیگ | [دانلود](https://cdn.jsdelivr.net/gh/aristapanell-cell/AriataPanel@main/config.json/combined/ALL/250.json) |
| ۳۰۰ کانفیگ | [دانلود](https://cdn.jsdelivr.net/gh/aristapanell-cell/AriataPanel@main/config.json/combined/ALL/300.json) |
| ۴۰۰ کانفیگ | [دانلود](https://cdn.jsdelivr.net/gh/aristapanell-cell/AriataPanel@main/config.json/combined/ALL/400.json) |
| ۵۰۰ کانفیگ | [دانلود](https://cdn.jsdelivr.net/gh/aristapanell-cell/AriataPanel@main/config.json/combined/ALL/500.json) |
| تمامی کانفیگ‌ها | [دانلود](https://cdn.jsdelivr.net/gh/aristapanell-cell/AriataPanel@main/config.json/combined/ALL/ALL.json) |

---

### 🔹 ClashMeta

#### 📌 تلگرام

| تعداد | لینک دانلود |
|-------|------------|
| ۵۰ کانفیگ | [دانلود](https://cdn.jsdelivr.net/gh/aristapanell-cell/AriataPanel@main/config.yaml/telegram/ALL/50.yaml) |
| ۱۰۰ کانفیگ | [دانلود](https://cdn.jsdelivr.net/gh/aristapanell-cell/AriataPanel@main/config.yaml/telegram/ALL/100.yaml) |
| ۱۵۰ کانفیگ | [دانلود](https://cdn.jsdelivr.net/gh/aristapanell-cell/AriataPanel@main/config.yaml/telegram/ALL/150.yaml) |
| ۲۰۰ کانفیگ | [دانلود](https://cdn.jsdelivr.net/gh/aristapanell-cell/AriataPanel@main/config.yaml/telegram/ALL/200.yaml) |
| ۲۵۰ کانفیگ | [دانلود](https://cdn.jsdelivr.net/gh/aristapanell-cell/AriataPanel@main/config.yaml/telegram/ALL/250.yaml) |
| ۳۰۰ کانفیگ | [دانلود](https://cdn.jsdelivr.net/gh/aristapanell-cell/AriataPanel@main/config.yaml/telegram/ALL/300.yaml) |
| ۴۰۰ کانفیگ | [دانلود](https://cdn.jsdelivr.net/gh/aristapanell-cell/AriataPanel@main/config.yaml/telegram/ALL/400.yaml) |
| ۵۰۰ کانفیگ | [دانلود](https://cdn.jsdelivr.net/gh/aristapanell-cell/AriataPanel@main/config.yaml/telegram/ALL/500.yaml) |
| تمامی کانفیگ‌ها | [دانلود](https://cdn.jsdelivr.net/gh/aristapanell-cell/AriataPanel@main/config.yaml/telegram/ALL/ALL.yaml) |

#### 📌 گیت‌هاب

| تعداد | لینک دانلود |
|-------|------------|
| ۵۰ کانفیگ | [دانلود](https://cdn.jsdelivr.net/gh/aristapanell-cell/AriataPanel@main/config.yaml/github/ALL/50.yaml) |
| ۱۰۰ کانفیگ | [دانلود](https://cdn.jsdelivr.net/gh/aristapanell-cell/AriataPanel@main/config.yaml/github/ALL/100.yaml) |
| ۱۵۰ کانفیگ | [دانلود](https://cdn.jsdelivr.net/gh/aristapanell-cell/AriataPanel@main/config.yaml/github/ALL/150.yaml) |
| ۲۰۰ کانفیگ | [دانلود](https://cdn.jsdelivr.net/gh/aristapanell-cell/AriataPanel@main/config.yaml/github/ALL/200.yaml) |
| ۲۵۰ کانفیگ | [دانلود](https://cdn.jsdelivr.net/gh/aristapanell-cell/AriataPanel@main/config.yaml/github/ALL/250.yaml) |
| ۳۰۰ کانفیگ | [دانلود](https://cdn.jsdelivr.net/gh/aristapanell-cell/AriataPanel@main/config.yaml/github/ALL/300.yaml) |
| ۴۰۰ کانفیگ | [دانلود](https://cdn.jsdelivr.net/gh/aristapanell-cell/AriataPanel@main/config.yaml/github/ALL/400.yaml) |
| ۵۰۰ کانفیگ | [دانلود](https://cdn.jsdelivr.net/gh/aristapanell-cell/AriataPanel@main/config.yaml/github/ALL/500.yaml) |
| تمامی کانفیگ‌ها | [دانلود](https://cdn.jsdelivr.net/gh/aristapanell-cell/AriataPanel@main/config.yaml/github/ALL/ALL.yaml) |

#### 📌 ترکیبی (تلگرام + گیت‌هاب)

| تعداد | لینک دانلود |
|-------|------------|
| ۵۰ کانفیگ | [دانلود](https://cdn.jsdelivr.net/gh/aristapanell-cell/AriataPanel@main/config.yaml/combined/ALL/50.yaml) |
| ۱۰۰ کانفیگ | [دانلود](https://cdn.jsdelivr.net/gh/aristapanell-cell/AriataPanel@main/config.yaml/combined/ALL/100.yaml) |
| ۱۵۰ کانفیگ | [دانلود](https://cdn.jsdelivr.net/gh/aristapanell-cell/AriataPanel@main/config.yaml/combined/ALL/150.yaml) |
| ۲۰۰ کانفیگ | [دانلود](https://cdn.jsdelivr.net/gh/aristapanell-cell/AriataPanel@main/config.yaml/combined/ALL/200.yaml) |
| ۲۵۰ کانفیگ | [دانلود](https://cdn.jsdelivr.net/gh/aristapanell-cell/AriataPanel@main/config.yaml/combined/ALL/250.yaml) |
| ۳۰۰ کانفیگ | [دانلود](https://cdn.jsdelivr.net/gh/aristapanell-cell/AriataPanel@main/config.yaml/combined/ALL/300.yaml) |
| ۴۰۰ کانفیگ | [دانلود](https://cdn.jsdelivr.net/gh/aristapanell-cell/AriataPanel@main/config.yaml/combined/ALL/400.yaml) |
| ۵۰۰ کانفیگ | [دانلود](https://cdn.jsdelivr.net/gh/aristapanell-cell/AriataPanel@main/config.yaml/combined/ALL/500.yaml) |
| تمامی کانفیگ‌ها | [دانلود](https://cdn.jsdelivr.net/gh/aristapanell-cell/AriataPanel@main/config.yaml/combined/ALL/ALL.yaml) |

---
## 📱 کلاینت‌های پشتیبانی‌شده

| نام کلاینت | سیستم‌عامل | لینک دانلود |
|-----------|-----------|------------|
| **V2rayNG** | Android | [دانلود](https://github.com/2dust/v2rayNG/releases) |
| **Hiddify** | Android / iOS / Windows / macOS / Linux | [دانلود](https://github.com/hiddify/hiddify-app/releases) |
| **NekoBox** | Android | [دانلود](https://github.com/MatsuriDayo/NekoBoxForAndroid/releases) |
| **SingBox** | Android / iOS / Windows / macOS / Linux | [دانلود](https://github.com/SagerNet/sing-box/releases) |
| **ClashMeta** | Android / iOS / Windows / macOS / Linux | [دانلود](https://github.com/MetaCubeX/Clash.Meta/releases) |
| **v2rayN** | Windows | [دانلود](https://github.com/2dust/v2rayN/releases) |
| **Nekoray** | Windows / macOS / Linux | [دانلود](https://github.com/MatsuriDayo/nekoray/releases) |
| **Streisand** | Windows / macOS / Linux | [دانلود](https://github.com/SagerNet/Streisand/releases) |
| **Shadowrocket** | iOS | [دانلود](https://apps.apple.com/app/shadowrocket/id932747118) |
| **FairVPN** | iOS / macOS | [دانلود](https://apps.apple.com/app/fairvpn/id1533888676) |
| **V2Box** | iOS | [دانلود](https://apps.apple.com/app/v2box-v2ray-client/id6446814690) |
| **FoXray** | iOS | [دانلود](https://apps.apple.com/app/foxray/id6448898396) |

---

❤️ ساخته شده توسط تیم آریستا (🇲‌🇲‌🇩‌) ❤️

</div>
