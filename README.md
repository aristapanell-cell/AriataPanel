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

<details>
<summary>📱 <b>V2rayNG • Hiddify • NekoBox • ...</b></summary>

<br/>

| منبع | ۵۰ | ۱۰۰ | ۱۵۰ | ۲۰۰ | ۲۵۰ | ۳۰۰ | ۴۰۰ | ۵۰۰ | ALL |
|:-----|:---:|:----:|:----:|:----:|:----:|:----:|:----:|:----:|:---:|
| **تلگرام** | [📥](https://raw.githubusercontent.com/aristapanell-cell/AriataPanel/refs/heads/main/configs.txt/telegram/ALL/50.txt) | [📥](https://raw.githubusercontent.com/aristapanell-cell/AriataPanel/refs/heads/main/configs.txt/telegram/ALL/100.txt) | [📥](https://raw.githubusercontent.com/aristapanell-cell/AriataPanel/refs/heads/main/configs.txt/telegram/ALL/150.txt) | [📥](https://raw.githubusercontent.com/aristapanell-cell/AriataPanel/refs/heads/main/configs.txt/telegram/ALL/200.txt) | [📥](https://raw.githubusercontent.com/aristapanell-cell/AriataPanel/refs/heads/main/configs.txt/telegram/ALL/250.txt) | [📥](https://raw.githubusercontent.com/aristapanell-cell/AriataPanel/refs/heads/main/configs.txt/telegram/ALL/300.txt) | [📥](https://raw.githubusercontent.com/aristapanell-cell/AriataPanel/refs/heads/main/configs.txt/telegram/ALL/400.txt) | [📥](https://raw.githubusercontent.com/aristapanell-cell/AriataPanel/refs/heads/main/configs.txt/telegram/ALL/500.txt) | [📥](https://raw.githubusercontent.com/aristapanell-cell/AriataPanel/refs/heads/main/configs.txt/telegram/ALL/ALL.txt) |
| **گیت‌هاب** | [📥](https://raw.githubusercontent.com/aristapanell-cell/AriataPanel/refs/heads/main/configs.txt/github/ALL/50.txt) | [📥](https://raw.githubusercontent.com/aristapanell-cell/AriataPanel/refs/heads/main/configs.txt/github/ALL/100.txt) | [📥](https://raw.githubusercontent.com/aristapanell-cell/AriataPanel/refs/heads/main/configs.txt/github/ALL/150.txt) | [📥](https://raw.githubusercontent.com/aristapanell-cell/AriataPanel/refs/heads/main/configs.txt/github/ALL/200.txt) | [📥](https://raw.githubusercontent.com/aristapanell-cell/AriataPanel/refs/heads/main/configs.txt/github/ALL/250.txt) | [📥](https://raw.githubusercontent.com/aristapanell-cell/AriataPanel/refs/heads/main/configs.txt/github/ALL/300.txt) | [📥](https://raw.githubusercontent.com/aristapanell-cell/AriataPanel/refs/heads/main/configs.txt/github/ALL/400.txt) | [📥](https://raw.githubusercontent.com/aristapanell-cell/AriataPanel/refs/heads/main/configs.txt/github/ALL/500.txt) | [📥](https://raw.githubusercontent.com/aristapanell-cell/AriataPanel/refs/heads/main/configs.txt/github/ALL/ALL.txt) |
| **ترکیبی** | [📥](https://raw.githubusercontent.com/aristapanell-cell/AriataPanel/refs/heads/main/configs.txt/combined/ALL/50.txt) | [📥](https://raw.githubusercontent.com/aristapanell-cell/AriataPanel/refs/heads/main/configs.txt/combined/ALL/100.txt) | [📥](https://raw.githubusercontent.com/aristapanell-cell/AriataPanel/refs/heads/main/configs.txt/combined/ALL/150.txt) | [📥](https://raw.githubusercontent.com/aristapanell-cell/AriataPanel/refs/heads/main/configs.txt/combined/ALL/200.txt) | [📥](https://raw.githubusercontent.com/aristapanell-cell/AriataPanel/refs/heads/main/configs.txt/combined/ALL/250.txt) | [📥](https://raw.githubusercontent.com/aristapanell-cell/AriataPanel/refs/heads/main/configs.txt/combined/ALL/300.txt) | [📥](https://raw.githubusercontent.com/aristapanell-cell/AriataPanel/refs/heads/main/configs.txt/combined/ALL/400.txt) | [📥](https://raw.githubusercontent.com/aristapanell-cell/AriataPanel/refs/heads/main/configs.txt/combined/ALL/500.txt) | [📥](https://raw.githubusercontent.com/aristapanell-cell/AriataPanel/refs/heads/main/configs.txt/combined/ALL/ALL.txt) |

</details>

<details>
<summary>🔷 <b>SingBox</b></summary>

<br/>

| منبع | ۵۰ | ۱۰۰ | ۱۵۰ | ۲۰۰ | ۲۵۰ | ۳۰۰ | ۴۰۰ | ۵۰۰ | ALL |
|:-----|:---:|:----:|:----:|:----:|:----:|:----:|:----:|:----:|:---:|
| **تلگرام** | [📥](https://raw.githubusercontent.com/aristapanell-cell/AriataPanel/refs/heads/main/config.json/telegram/ALL/50.json) | [📥](https://raw.githubusercontent.com/aristapanell-cell/AriataPanel/refs/heads/main/config.json/telegram/ALL/100.json) | [📥](https://raw.githubusercontent.com/aristapanell-cell/AriataPanel/refs/heads/main/config.json/telegram/ALL/150.json) | [📥](https://raw.githubusercontent.com/aristapanell-cell/AriataPanel/refs/heads/main/config.json/telegram/ALL/200.json) | [📥](https://raw.githubusercontent.com/aristapanell-cell/AriataPanel/refs/heads/main/config.json/telegram/ALL/250.json) | [📥](https://raw.githubusercontent.com/aristapanell-cell/AriataPanel/refs/heads/main/config.json/telegram/ALL/300.json) | [📥](https://raw.githubusercontent.com/aristapanell-cell/AriataPanel/refs/heads/main/config.json/telegram/ALL/400.json) | [📥](https://raw.githubusercontent.com/aristapanell-cell/AriataPanel/refs/heads/main/config.json/telegram/ALL/500.json) | [📥](https://raw.githubusercontent.com/aristapanell-cell/AriataPanel/refs/heads/main/config.json/telegram/ALL/ALL.json) |
| **گیت‌هاب** | [📥](https://raw.githubusercontent.com/aristapanell-cell/AriataPanel/refs/heads/main/config.json/github/ALL/50.json) | [📥](https://raw.githubusercontent.com/aristapanell-cell/AriataPanel/refs/heads/main/config.json/github/ALL/100.json) | [📥](https://raw.githubusercontent.com/aristapanell-cell/AriataPanel/refs/heads/main/config.json/github/ALL/150.json) | [📥](https://raw.githubusercontent.com/aristapanell-cell/AriataPanel/refs/heads/main/config.json/github/ALL/200.json) | [📥](https://raw.githubusercontent.com/aristapanell-cell/AriataPanel/refs/heads/main/config.json/github/ALL/250.json) | [📥](https://raw.githubusercontent.com/aristapanell-cell/AriataPanel/refs/heads/main/config.json/github/ALL/300.json) | [📥](https://raw.githubusercontent.com/aristapanell-cell/AriataPanel/refs/heads/main/config.json/github/ALL/400.json) | [📥](https://raw.githubusercontent.com/aristapanell-cell/AriataPanel/refs/heads/main/config.json/github/ALL/500.json) | [📥](https://raw.githubusercontent.com/aristapanell-cell/AriataPanel/refs/heads/main/config.json/github/ALL/ALL.json) |
| **ترکیبی** | [📥](https://raw.githubusercontent.com/aristapanell-cell/AriataPanel/refs/heads/main/config.json/combined/ALL/50.json) | [📥](https://raw.githubusercontent.com/aristapanell-cell/AriataPanel/refs/heads/main/config.json/combined/ALL/100.json) | [📥](https://raw.githubusercontent.com/aristapanell-cell/AriataPanel/refs/heads/main/config.json/combined/ALL/150.json) | [📥](https://raw.githubusercontent.com/aristapanell-cell/AriataPanel/refs/heads/main/config.json/combined/ALL/200.json) | [📥](https://raw.githubusercontent.com/aristapanell-cell/AriataPanel/refs/heads/main/config.json/combined/ALL/250.json) | [📥](https://raw.githubusercontent.com/aristapanell-cell/AriataPanel/refs/heads/main/config.json/combined/ALL/300.json) | [📥](https://raw.githubusercontent.com/aristapanell-cell/AriataPanel/refs/heads/main/config.json/combined/ALL/400.json) | [📥](https://raw.githubusercontent.com/aristapanell-cell/AriataPanel/refs/heads/main/config.json/combined/ALL/500.json) | [📥](https://raw.githubusercontent.com/aristapanell-cell/AriataPanel/refs/heads/main/config.json/combined/ALL/ALL.json) |

</details>

<details>
<summary>🔶 <b>ClashMeta</b></summary>

<br/>

| منبع | ۵۰ | ۱۰۰ | ۱۵۰ | ۲۰۰ | ۲۵۰ | ۳۰۰ | ۴۰۰ | ۵۰۰ | ALL |
|:-----|:---:|:----:|:----:|:----:|:----:|:----:|:----:|:----:|:---:|
| **تلگرام** | [📥](https://raw.githubusercontent.com/aristapanell-cell/AriataPanel/refs/heads/main/config.yaml/telegram/ALL/50.yaml) | [📥](https://raw.githubusercontent.com/aristapanell-cell/AriataPanel/refs/heads/main/config.yaml/telegram/ALL/100.yaml) | [📥](https://raw.githubusercontent.com/aristapanell-cell/AriataPanel/refs/heads/main/config.yaml/telegram/ALL/150.yaml) | [📥](https://raw.githubusercontent.com/aristapanell-cell/AriataPanel/refs/heads/main/config.yaml/telegram/ALL/200.yaml) | [📥](https://raw.githubusercontent.com/aristapanell-cell/AriataPanel/refs/heads/main/config.yaml/telegram/ALL/250.yaml) | [📥](https://raw.githubusercontent.com/aristapanell-cell/AriataPanel/refs/heads/main/config.yaml/telegram/ALL/300.yaml) | [📥](https://raw.githubusercontent.com/aristapanell-cell/AriataPanel/refs/heads/main/config.yaml/telegram/ALL/400.yaml) | [📥](https://raw.githubusercontent.com/aristapanell-cell/AriataPanel/refs/heads/main/config.yaml/telegram/ALL/500.yaml) | [📥](https://raw.githubusercontent.com/aristapanell-cell/AriataPanel/refs/heads/main/config.yaml/telegram/ALL/ALL.yaml) |
| **گیت‌هاب** | [📥](https://raw.githubusercontent.com/aristapanell-cell/AriataPanel/refs/heads/main/config.yaml/github/ALL/50.yaml) | [📥](https://raw.githubusercontent.com/aristapanell-cell/AriataPanel/refs/heads/main/config.yaml/github/ALL/100.yaml) | [📥](https://raw.githubusercontent.com/aristapanell-cell/AriataPanel/refs/heads/main/config.yaml/github/ALL/150.yaml) | [📥](https://raw.githubusercontent.com/aristapanell-cell/AriataPanel/refs/heads/main/config.yaml/github/ALL/200.yaml) | [📥](https://raw.githubusercontent.com/aristapanell-cell/AriataPanel/refs/heads/main/config.yaml/github/ALL/250.yaml) | [📥](https://raw.githubusercontent.com/aristapanell-cell/AriataPanel/refs/heads/main/config.yaml/github/ALL/300.yaml) | [📥](https://raw.githubusercontent.com/aristapanell-cell/AriataPanel/refs/heads/main/config.yaml/github/ALL/400.yaml) | [📥](https://raw.githubusercontent.com/aristapanell-cell/AriataPanel/refs/heads/main/config.yaml/github/ALL/500.yaml) | [📥](https://raw.githubusercontent.com/aristapanell-cell/AriataPanel/refs/heads/main/config.yaml/github/ALL/ALL.yaml) |
| **ترکیبی** | [📥](https://raw.githubusercontent.com/aristapanell-cell/AriataPanel/refs/heads/main/config.yaml/combined/ALL/50.yaml) | [📥](https://raw.githubusercontent.com/aristapanell-cell/AriataPanel/refs/heads/main/config.yaml/combined/ALL/100.yaml) | [📥](https://raw.githubusercontent.com/aristapanell-cell/AriataPanel/refs/heads/main/config.yaml/combined/ALL/150.yaml) | [📥](https://raw.githubusercontent.com/aristapanell-cell/AriataPanel/refs/heads/main/config.yaml/combined/ALL/200.yaml) | [📥](https://raw.githubusercontent.com/aristapanell-cell/AriataPanel/refs/heads/main/config.yaml/combined/ALL/250.yaml) | [📥](https://raw.githubusercontent.com/aristapanell-cell/AriataPanel/refs/heads/main/config.yaml/combined/ALL/300.yaml) | [📥](https://raw.githubusercontent.com/aristapanell-cell/AriataPanel/refs/heads/main/config.yaml/combined/ALL/400.yaml) | [📥](https://raw.githubusercontent.com/aristapanell-cell/AriataPanel/refs/heads/main/config.yaml/combined/ALL/500.yaml) | [📥](https://raw.githubusercontent.com/aristapanell-cell/AriataPanel/refs/heads/main/config.yaml/combined/ALL/ALL.yaml) |

</details>

---

## 📱 کلاینت‌های پشتیبانی‌شده

| نام کلاینت | سیستم‌عامل | لینک دانلود |
|:-----------|:-----------|:-----------:|
| **V2rayNG** | Android | [📥](https://github.com/2dust/v2rayNG/releases) |
| **Hiddify** | Android • iOS • Windows • macOS • Linux | [📥](https://github.com/hiddify/hiddify-app/releases) |
| **NekoBox** | Android | [📥](https://github.com/MatsuriDayo/NekoBoxForAndroid/releases) |
| **SingBox** | Android • iOS • Windows • macOS • Linux | [📥](https://github.com/SagerNet/sing-box/releases) |
| **ClashMeta** | Android • iOS • Windows • macOS • Linux | [📥](https://github.com/MetaCubeX/Clash.Meta/releases) |
| **v2rayN** | Windows | [📥](https://github.com/2dust/v2rayN/releases) |
| **Nekoray** | Windows • macOS • Linux | [📥](https://github.com/MatsuriDayo/nekoray/releases) |
| **Streisand** | Windows • macOS • Linux | [📥](https://github.com/SagerNet/Streisand/releases) |
| **Shadowrocket** | iOS | [📥](https://apps.apple.com/app/shadowrocket/id932747118) |
| **FairVPN** | iOS • macOS | [📥](https://apps.apple.com/app/fairvpn/id1533888676) |
| **V2Box** | iOS | [📥](https://apps.apple.com/app/v2box-v2ray-client/id6446814690) |
| **FoXray** | iOS | [📥](https://apps.apple.com/app/foxray/id6448898396) |

---

<div align="center">

# 📡 بانک اطلاعات IPهای برتر

### ⚡ آخرین نتایج اسکن به‌صورت زنده در دسترس است

<br>

<a href="https://raw.githubusercontent.com/aristapanell-cell/ARISTA-MATRIX-PIPELINE/main/output/best_ips.txt">
    <img src="https://img.shields.io/badge/⚡_BEST_IPS-LIVE-00C853?style=for-the-badge&logo=github&logoColor=white&labelColor=111827" alt="BEST IPS">
</a>

<br><br>

⭐ **مشاهده لیست کامل IPهای رتبه‌بندی‌شده**  
🚀 **Score • TTFB • Protocol • CDN • Domain • Country • City • Provider**

</div>

---

<div align="center">

<table border="0" cellpadding="20" style="background: linear-gradient(135deg, #1a1a2e, #16213e); border-radius: 20px; border: 2px solid #e94560; margin: 0 auto;">
  <tr>
    <td align="center" style="padding: 25px 40px;">
      <span style="font-size: 1.8em; color: #e94560;">❤️</span>
      <span style="font-size: 1.5em; color: #ffffff; font-weight: bold;"> ساخته شده توسط تیم آریستا </span>
      <span style="font-size: 1.8em; color: #e94560;">❤️</span>
      <br>
      <span style="font-size: 1.2em; color: #ffd700;">🇲‌🇲‌🇩‌</span>
    </td>
  </tr>
</table>

<br>

## ⭐ حمایت

اگر این پروژه برای شما مفید بود، لطفاً با ⭐ در GitHub از ما حمایت کنید.

</div>
c
