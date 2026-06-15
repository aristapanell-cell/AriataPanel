<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Arista VPN Config Aggregator</title>
    <style>
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }

        body {
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, 'Helvetica Neue', sans-serif;
            background: linear-gradient(135deg, #0a0f1e 0%, #0c1222 100%);
            color: #e4e6eb;
            line-height: 1.6;
            padding: 2rem;
        }

        .container {
            max-width: 1200px;
            margin: 0 auto;
        }

        /* Language Switcher */
        .lang-switch {
            display: flex;
            justify-content: flex-end;
            gap: 1rem;
            margin-bottom: 2rem;
        }

        .lang-btn {
            background: transparent;
            border: 2px solid #3b82f6;
            color: #3b82f6;
            padding: 0.5rem 1.5rem;
            border-radius: 40px;
            font-weight: 600;
            cursor: pointer;
            transition: all 0.3s ease;
            font-size: 0.9rem;
        }

        .lang-btn.active {
            background: #3b82f6;
            color: white;
            border-color: #3b82f6;
        }

        .lang-btn:hover:not(.active) {
            background: rgba(59, 130, 246, 0.2);
        }

        /* Header */
        .header {
            text-align: center;
            margin-bottom: 3rem;
        }

        .logo {
            font-size: 3rem;
            margin-bottom: 1rem;
        }

        h1 {
            font-size: 2.5rem;
            background: linear-gradient(135deg, #3b82f6, #a855f7);
            -webkit-background-clip: text;
            background-clip: text;
            color: transparent;
            margin-bottom: 0.5rem;
        }

        .badge-container {
            display: flex;
            justify-content: center;
            gap: 1rem;
            flex-wrap: wrap;
            margin: 1.5rem 0;
        }

        .badge {
            background: rgba(59, 130, 246, 0.2);
            padding: 0.3rem 0.8rem;
            border-radius: 20px;
            font-size: 0.8rem;
            color: #60a5fa;
        }

        /* Cards */
        .card {
            background: rgba(15, 25, 45, 0.7);
            backdrop-filter: blur(10px);
            border: 1px solid rgba(59, 130, 246, 0.2);
            border-radius: 20px;
            padding: 1.8rem;
            margin-bottom: 2rem;
            transition: transform 0.2s, border-color 0.2s;
        }

        .card:hover {
            border-color: rgba(59, 130, 246, 0.5);
        }

        .card h2 {
            color: #60a5fa;
            margin-bottom: 1.2rem;
            font-size: 1.6rem;
            display: flex;
            align-items: center;
            gap: 0.7rem;
        }

        .card h3 {
            color: #c084fc;
            margin: 1.2rem 0 0.8rem 0;
            font-size: 1.2rem;
        }

        /* Grid */
        .feature-grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(280px, 1fr));
            gap: 1rem;
            margin-top: 1rem;
        }

        .feature-item {
            background: rgba(0, 0, 0, 0.3);
            padding: 1rem;
            border-radius: 12px;
            border-left: 3px solid #3b82f6;
        }

        /* Stats */
        .stats-grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(150px, 1fr));
            gap: 1rem;
            text-align: center;
        }

        .stat {
            background: rgba(0, 0, 0, 0.3);
            padding: 1rem;
            border-radius: 12px;
        }

        .stat-number {
            font-size: 2rem;
            font-weight: bold;
            color: #3b82f6;
        }

        /* Code block */
        pre {
            background: #0a0e1a;
            padding: 1rem;
            border-radius: 12px;
            overflow-x: auto;
            font-size: 0.85rem;
            border: 1px solid #1e2a4a;
        }

        code {
            font-family: 'Fira Code', 'Courier New', monospace;
        }

        /* Buttons */
        .btn {
            display: inline-block;
            background: #3b82f6;
            color: white;
            padding: 0.75rem 1.5rem;
            border-radius: 40px;
            text-decoration: none;
            font-weight: 600;
            transition: all 0.3s;
            margin-top: 1rem;
        }

        .btn:hover {
            background: #2563eb;
            transform: translateY(-2px);
        }

        .btn-outline {
            background: transparent;
            border: 2px solid #3b82f6;
            color: #3b82f6;
        }

        .btn-outline:hover {
            background: #3b82f6;
            color: white;
        }

        /* Table */
        table {
            width: 100%;
            border-collapse: collapse;
            margin: 1rem 0;
        }

        th, td {
            padding: 0.75rem;
            text-align: left;
            border-bottom: 1px solid #1e2a4a;
        }

        th {
            color: #60a5fa;
        }

        /* Footer */
        .footer {
            text-align: center;
            padding: 2rem;
            margin-top: 2rem;
            border-top: 1px solid #1e2a4a;
            color: #6b7280;
        }

        /* Language content containers */
        .lang-content {
            display: none;
        }

        .lang-content.active {
            display: block;
        }

        hr {
            border-color: #1e2a4a;
            margin: 1.5rem 0;
        }

        @media (max-width: 768px) {
            body {
                padding: 1rem;
            }
            h1 {
                font-size: 1.8rem;
            }
        }
    </style>
</head>
<body>
    <div class="container">
        <!-- Language Switcher -->
        <div class="lang-switch">
            <button class="lang-btn active" data-lang="en">🇬🇧 English</button>
            <button class="lang-btn" data-lang="fa">🇮🇷 فارسی</button>
        </div>

        <!-- ==================== ENGLISH CONTENT ==================== -->
        <div id="lang-en" class="lang-content active">
            <div class="header">
                <div class="logo">🚀</div>
                <h1>Arista VPN Config Aggregator</h1>
                <p>Professional & Automated VPN Configuration Aggregation System</p>
                <div class="badge-container">
                    <span class="badge">MIT License</span>
                    <span class="badge">GitHub Actions</span>
                    <span class="badge">Python 3.14</span>
                    <span class="badge">Every 6h Update</span>
                </div>
            </div>

            <!-- About -->
            <div class="card">
                <h2>📖 About The Project</h2>
                <p><strong>Arista Config Aggregator</strong> is a fully automated, enterprise-grade system that collects, validates, categorizes, and deduplicates VPN configurations from <strong>500+ Telegram channels</strong> and <strong>10+ GitHub repositories</strong>. The system runs every 6 hours via GitHub Actions, ensuring you always have access to fresh, working configurations.</p>
            </div>

            <!-- How It Works -->
            <div class="card">
                <h2>⚙️ How It Works</h2>
                <div class="feature-grid">
                    <div class="feature-item">
                        <strong>🤖 Telegram Extractor</strong><br>
                        500+ channels, dead channel detection (2d no post → 7d suspension), permanent blacklist, 15 latest configs per channel.
                    </div>
                    <div class="feature-item">
                        <strong>🐙 GitHub Extractor</strong><br>
                        10+ curated sources, raw files, CDN mirrors, GitVerse support.
                    </div>
                    <div class="feature-item">
                        <strong>🔄 Config Combiner</strong><br>
                        MD5 deduplication, protocol categorization (vmess/vless/trojan/ss/hysteria2/hysteria/tuic/wireguard).
                    </div>
                    <div class="feature-item">
                        <strong>📊 Tiered Output</strong><br>
                        50/100/150/200/250/300/400/500/ALL configs, 10% overlap between tiers.
                    </div>
                    <div class="feature-item">
                        <strong>🧹 Validation</strong><br>
                        Port range checks, UUID validation, Shadowsocks standardization, VMess JSON verification.
                    </div>
                    <div class="feature-item">
                        <strong>💀 Dead Channel Management</strong><br>
                        Auto-detection, 7-day temporary suspension, permanent blacklist after 7d inactivity.
                    </div>
                </div>
            </div>

            <!-- Output Structure -->
            <div class="card">
                <h2>📊 Output Structure</h2>
                <pre><code>configs/
├── telegram/           # From 500+ Telegram channels
│   ├── vmess/
│   ├── vless/
│   ├── trojan/
│   └── ... (50/100/150... tier files)
├── github/            # From GitHub sources
│   └── ... (same tiered structure)
└── combined/          # Merged & deduplicated
    └── ... (complete tiered structure)</code></pre>
            </div>

            <!-- Subscription & Telegram Channel -->
            <div class="card">
                <h2>🔗 Subscription & Community</h2>
                <div style="background: rgba(220, 38, 38, 0.15); border-left: 4px solid #ef4444; padding: 1rem; border-radius: 8px; margin-bottom: 1.5rem;">
                    ⚠️ <strong>Important:</strong> Direct subscription links are NOT provided on GitHub for security and stability reasons.
                </div>
                
                <h3>📡 Join Our Telegram Channel: <span style="color: #3b82f6;">@aristapanel</span></h3>
                
                <table>
                    <thead>
                        <tr><th>Service</th><th>Description</th></tr>
                    </thead>
                    <tbody>
                        <tr><td><strong>Subscription Links</strong></td><td>Direct subscription URLs for this aggregation system</td></tr>
                        <tr><td><strong>Telegram Proxies</strong></td><td>MTProto & SOCKS5 proxies for Telegram access</td></tr>
                        <tr><td><strong>Clean IPs</strong></td><td>Scanned from hundreds of millions of IPs - optimized for streaming</td></tr>
                        <tr><td><strong>Daily Updates</strong></td><td>Fresh configurations every 6 hours automatically</td></tr>
                        <tr><td><strong>Premium Support</strong></td><td>Direct support for configuration issues</td></tr>
                    </tbody>
                </table>

                <a href="https://t.me/aristapanel" class="btn">🔗 Join @aristapanel on Telegram</a>
            </div>

            <!-- Public Panel -->
            <div class="card">
                <h2>🌐 Public Control Panel</h2>
                <p>Access our <strong>Cloudflare Workers-based public panel</strong> for personal configuration optimization:</p>
                <div style="background: #0a0e1a; padding: 1rem; border-radius: 12px; margin: 1rem 0; word-break: break-all;">
                    🔗 <code style="color: #60a5fa;">https://arista-panel.arista-panel.workers.dev/</code>
                </div>
                <div class="feature-grid">
                    <div class="feature-item">✅ Personalize your configurations</div>
                    <div class="feature-item">✅ Filter by protocol and region</div>
                    <div class="feature-item">✅ Generate custom subscription links</div>
                    <div class="feature-item">✅ Optimize for your specific use case</div>
                </div>
                <a href="https://arista-panel.arista-panel.workers.dev/" class="btn btn-outline">🎮 Open Control Panel →</a>
            </div>

            <!-- Technical Specs -->
            <div class="card">
                <h2>🛠️ Technical Specifications</h2>
                <div class="stats-grid">
                    <div class="stat"><div class="stat-number">6h</div><div>Update Frequency</div></div>
                    <div class="stat"><div class="stat-number">45m</div><div>Max Runtime</div></div>
                    <div class="stat"><div class="stat-number">500+</div><div>Channels</div></div>
                    <div class="stat"><div class="stat-number">10+</div><div>GitHub Sources</div></div>
                </div>
                <ul style="margin-top: 1rem; margin-left: 1.5rem;">
                    <li>Smart delays between requests to avoid rate limiting</li>
                    <li>Persistent JSON-based caching for dead channels</li>
                    <li>Random delay: 60-360 seconds before processing</li>
                    <li>Python 3.14 | requests | beautifulsoup4</li>
                </ul>
            </div>

            <!-- Statistics -->
            <div class="card">
                <h2>📈 Statistics (per update cycle)</h2>
                <div class="stats-grid">
                    <div class="stat"><div class="stat-number">500+</div><div>Channels Processed</div></div>
                    <div class="stat"><div class="stat-number">~350</div><div>Active Channels</div></div>
                    <div class="stat"><div class="stat-number">2K-5K</div><div>Raw Configs</div></div>
                    <div class="stat"><div class="stat-number">500-1500</div><div>Unique Configs</div></div>
                    <div class="stat"><div class="stat-number">80+</div><div>Tiered Files</div></div>
                    <div class="stat"><div class="stat-number">10%</div><div>Tier Overlap</div></div>
                </div>
            </div>

            <!-- Quick Start -->
            <div class="card">
                <h2>🚀 Quick Start (Development)</h2>
                <pre><code>git clone https://github.com/yourusername/yourrepo.git
cd yourrepo
pip install requests beautifulsoup4
python telegram_extractor.py
python github_extractor.py
python combine_configs.py</code></pre>
            </div>

            <!-- Footer -->
            <div class="footer">
                <p>Made with ❤️ by Arista Team</p>
                <p>MIT License • <a href="#" style="color: #60a5fa;">GitHub Repository</a></p>
            </div>
        </div>

        <!-- ==================== PERSIAN CONTENT ==================== -->
        <div id="lang-fa" class="lang-content" dir="rtl">
            <div class="header">
                <div class="logo">🚀</div>
                <h1>تجمیع‌کننده کانفیگ VPN آریستا</h1>
                <p>سیستم حرفه‌ای و خودکار جمع‌آوری کانفیگ VPN</p>
                <div class="badge-container">
                    <span class="badge">مجوز MIT</span>
                    <span class="badge">گیت‌هاب اکشنز</span>
                    <span class="badge">پایتون ۳.۱۴</span>
                    <span class="badge">بروزرسانی هر ۶ ساعت</span>
                </div>
            </div>

            <!-- About -->
            <div class="card">
                <h2>📖 درباره پروژه</h2>
                <p><strong>تجمیع‌کننده کانفیگ آریستا</strong> یک سیستم کاملاً خودکار و در سطح سازمانی است که کانفیگ‌های VPN را از <strong>بیش از ۵۰۰ کانال تلگرام</strong> و <strong>۱۰+ مخزن گیت‌هاب</strong> جمع‌آوری، اعتبارسنجی، دسته‌بندی و حذف تکراری می‌کند. این سیستم هر ۶ ساعت یکبار از طریق GitHub Actions اجرا می‌شود.</p>
            </div>

            <!-- How It Works -->
            <div class="card">
                <h2>⚙️ نحوه عملکرد</h2>
                <div class="feature-grid">
                    <div class="feature-item">
                        <strong>🤖 استخراج‌کننده تلگرام</strong><br>
                        بیش از ۵۰۰ کانال، تشخیص کانال مرده (۲ روز بدون پست ← تعلیق ۷ روزه)، لیست سیاه دائمی، ۱۵ کانفیگ آخر هر کانال.
                    </div>
                    <div class="feature-item">
                        <strong>🐙 استخراج‌کننده گیت‌هاب</strong><br>
                        ۱۰+ منبع، فایل‌های خام، آینه CDN، پشتیبانی GitVerse.
                    </div>
                    <div class="feature-item">
                        <strong>🔄 ترکیب‌کننده</strong><br>
                        حذف تکراری با MD5، دسته‌بندی پروتکل (vmess/vless/trojan/ss/hysteria2/hysteria/tuic/wireguard).
                    </div>
                    <div class="feature-item">
                        <strong>📊 خروجی طبقه‌بندی</strong><br>
                        ۵۰/۱۰۰/۱۵۰/۲۰۰/۲۵۰/۳۰۰/۴۰۰/۵۰۰/ALL، ۱۰٪ همپوشانی بین طبقات.
                    </div>
                    <div class="feature-item">
                        <strong>🧹 اعتبارسنجی</strong><br>
                        بررسی محدوده پورت، اعتبارسنجی UUID، استانداردسازی Shadowsocks، تأیید JSON VMess.
                    </div>
                    <div class="feature-item">
                        <strong>💀 مدیریت کانال‌های مرده</strong><br>
                        تشخیص خودکار، تعلیق موقت ۷ روزه، لیست سیاه دائمی پس از ۷ روز عدم فعالیت.
                    </div>
                </div>
            </div>

            <!-- Output Structure -->
            <div class="card">
                <h2>📊 ساختار خروجی</h2>
                <pre><code>configs/
├── telegram/           # از بیش از ۵۰۰ کانال تلگرام
│   ├── vmess/
│   ├── vless/
│   ├── trojan/
│   └── ... (فایل‌های طبقه‌بندی ۵۰/۱۰۰/۱۵۰...)
├── github/            # از منابع گیت‌هاب
│   └── ... (ساختار طبقه‌بندی مشابه)
└── combined/          # ادغام و حذف تکراری
    └── ... (ساختار طبقه‌بندی کامل)</code></pre>
            </div>

            <!-- Subscription & Telegram Channel -->
            <div class="card">
                <h2>🔗 سابسکرایب و جامعه</h2>
                <div style="background: rgba(220, 38, 38, 0.15); border-right: 4px solid #ef4444; padding: 1rem; border-radius: 8px; margin-bottom: 1.5rem;">
                    ⚠️ <strong>مهم:</strong> لینک‌های مستقیم سابسکرایب به دلایل امنیتی و پایداری در گیت‌هاب قرار داده نمی‌شوند.
                </div>
                
                <h3>📡 به کانال تلگرام ما بپیوندید: <span style="color: #3b82f6;">@aristapanel</span></h3>
                
                <table>
                    <thead><tr><th>سرویس</th><th>توضیحات</th></tr></thead>
                    <tbody>
                        <tr><td><strong>لینک‌های سابسکرایب</strong></td><td>آدرس‌های مستقیم سابسکرایب این سیستم</td></tr>
                        <tr><td><strong>پروکسی‌های تلگرام</strong></td><td>پروکسی MTProto و SOCKS5 برای دسترسی به تلگرام</td></tr>
                        <tr><td><strong>آی‌پی‌های تمیز</strong></td><td>اسکن شده از صدها میلیون آی‌پی - بهینه برای استریم</td></tr>
                        <tr><td><strong>به‌روزرسانی روزانه</strong></td><td>کانفیگ‌های تازه هر ۶ ساعت به صورت خودکار</td></tr>
                        <tr><td><strong>پشتیبانی ویژه</strong></td><td>پشتیبانی مستقیم برای مشکلات کانفیگ</td></tr>
                    </tbody>
                </table>

                <a href="https://t.me/aristapanel" class="btn">🔗 عضویت در @aristapanel در تلگرام</a>
            </div>

            <!-- Public Panel -->
            <div class="card">
                <h2>🌐 پنل کنترل عمومی</h2>
                <p>دسترسی به <strong>پنل عمومی مبتنی بر Cloudflare Workers</strong> برای بهینه‌سازی شخصی کانفیگ‌ها:</p>
                <div style="background: #0a0e1a; padding: 1rem; border-radius: 12px; margin: 1rem 0; word-break: break-all;">
                    🔗 <code style="color: #60a5fa;">https://arista-panel.arista-panel.workers.dev/</code>
                </div>
                <div class="feature-grid">
                    <div class="feature-item">✅ شخصی‌سازی کانفیگ‌های شما</div>
                    <div class="feature-item">✅ فیلتر بر اساس پروتکل و منطقه</div>
                    <div class="feature-item">✅ تولید لینک‌های سابسکرایب سفارشی</div>
                    <div class="feature-item">✅ بهینه‌سازی برای استفاده خاص شما</div>
                </div>
                <a href="https://arista-panel.arista-panel.workers.dev/" class="btn btn-outline">🎮 باز کردن پنل کنترل →</a>
            </div>

            <!-- Technical Specs -->
            <div class="card">
                <h2>🛠️ مشخصات فنی</h2>
                <div class="stats-grid">
                    <div class="stat"><div class="stat-number">۶ ساعت</div><div>فرکانس بروزرسانی</div></div>
                    <div class="stat"><div class="stat-number">۴۵ دقیقه</div><div>حداکثر زمان اجرا</div></div>
                    <div class="stat"><div class="stat-number">۵۰۰+</div><div>کانال</div></div>
                    <div class="stat"><div class="stat-number">۱۰+</div><div>منابع گیت‌هاب</div></div>
                </div>
                <ul style="margin-top: 1rem; margin-right: 1.5rem;">
                    <li>تأخیر هوشمند بین درخواست‌ها برای جلوگیری از محدودیت نرخ</li>
                    <li>کش پایدار مبتنی بر JSON برای کانال‌های مرده</li>
                    <li>تأخیر تصادفی: ۶۰-۳۶۰ ثانیه قبل از پردازش</li>
                    <li>پایتون ۳.۱۴ | requests | beautifulsoup4</li>
                </ul>
            </div>

            <!-- Statistics -->
            <div class="card">
                <h2>📈 آمار (در هر چرخه بروزرسانی)</h2>
                <div class="stats-grid">
                    <div class="stat"><div class="stat-number">۵۰۰+</div><div>کانال پردازش شده</div></div>
                    <div class="stat"><div class="stat-number">~۳۵۰</div><div>کانال فعال</div></div>
                    <div class="stat"><div class="stat-number">۲-۵ هزار</div><div>کانفیگ خام</div></div>
                    <div class="stat"><div class="stat-number">۵۰۰-۱۵۰۰</div><div>کانفیگ یکتا</div></div>
                    <div class="stat"><div class="stat-number">۸۰+</div><div>فایل طبقه‌بندی</div></div>
                    <div class="stat"><div class="stat-number">۱۰٪</div><div>همپوشانی طبقات</div></div>
                </div>
            </div>

            <!-- Quick Start -->
            <div class="card">
                <h2>🚀 شروع سریع (توسعه)</h2>
                <pre><code>git clone https://github.com/yourusername/yourrepo.git
cd yourrepo
pip install requests beautifulsoup4
python telegram_extractor.py
python github_extractor.py
python combine_configs.py</code></pre>
            </div>

            <!-- Footer -->
            <div class="footer">
                <p>ساخته شده با ❤️ توسط تیم آریستا</p>
                <p>مجوز MIT • <a href="#" style="color: #60a5fa;">مخزن گیت‌هاب</a></p>
            </div>
        </div>
    </div>

    <script>
        // Language switching functionality
        const langBtns = document.querySelectorAll('.lang-btn');
        const enContent = document.getElementById('lang-en');
        const faContent = document.getElementById('lang-fa');

        function setLanguage(lang) {
            // Update button active states
            langBtns.forEach(btn => {
                if (btn.getAttribute('data-lang') === lang) {
                    btn.classList.add('active');
                } else {
                    btn.classList.remove('active');
                }
            });

            // Show/hide content
            if (lang === 'en') {
                enContent.classList.add('active');
                faContent.classList.remove('active');
                document.documentElement.lang = 'en';
                document.documentElement.dir = 'ltr';
            } else {
                enContent.classList.remove('active');
                faContent.classList.add('active');
                document.documentElement.lang = 'fa';
                document.documentElement.dir = 'rtl';
            }

            // Save preference
            localStorage.setItem('arista_lang', lang);
        }

        // Event listeners
        langBtns.forEach(btn => {
            btn.addEventListener('click', () => {
                const lang = btn.getAttribute('data-lang');
                setLanguage(lang);
            });
        });

        // Load saved preference
        const savedLang = localStorage.getItem('arista_lang');
        if (savedLang && (savedLang === 'en' || savedLang === 'fa')) {
            setLanguage(savedLang);
        } else {
            setLanguage('en'); // Default English
        }
    </script>
</body>
</html>
