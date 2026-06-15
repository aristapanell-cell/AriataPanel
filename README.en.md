<div align="center">

# AristaPanel

[![فارسی](https://img.shields.io/badge/فارسی-292e33?style=for-the-badge)](README.md)
[![English](https://img.shields.io/badge/English-292e33?style=for-the-badge)](README.en.md)
[![Telegram](https://img.shields.io/badge/@aristapanel-229ED9?style=for-the-badge&logo=telegram&logoColor=white)](https://t.me/aristapanel)
[![Web Panel](https://img.shields.io/badge/Web_Panel-F38020?style=for-the-badge&logo=cloudflare&logoColor=white)](https://arista-panel.arista-panel.workers.dev/)

---

Automatic extraction, validation, categorization and aggregation system for proxy configurations collected from public Telegram channels and GitHub repositories.

</div>

---

## System Architecture

AristaPanel is a fully automated pipeline executed every 6 hours. Inputs include 500+ Telegram channels and 10+ GitHub repositories. The final output is stored as categorized and tiered text files inside the repository.

### Components

1. **telegram_extractor.py**  
   Scrapes public Telegram channels using the t.me/s/... format, extracts text content, detects proxy patterns via regex, and validates configuration structures (UUID, port range, encoding format). Channels with no new posts for more than 48 hours are temporarily suspended for 7 days. Channels failing three consecutive checks are moved to a 24-hour dead cache.

2. **github_extractor.py**  
   Fetches raw files directly from multiple sources including raw.githubusercontent.com, cdn.jsdelivr.net and gitverse.ru. Supports vmess://, vless://, trojan://, ss://, hysteria2:// and tuic:// formats. Automatically normalizes malformed ss:// links.

3. **combine_configs.py**  
   Merges outputs from both extractors, removes duplicates using MD5 hashing, and generates tiered structures with a 10-entry overlap between consecutive tiers. Available tiers: 50, 100, 150, 200, 250, 300, 400, 500 and ALL.

4. **GitHub Actions (main.yml)**  
   Scheduled using cron */6 * * * *, applies a random delay of 60–360 seconds to reduce rate-limit risks, and commits/pushes only when changes are detected.

---

## Dead Channel Management

The system automatically tracks channel status:

| Status | Condition | Action | Duration |
|----------|----------|----------|----------|
| Temporary Suspension | Last post > 48 hours | Stop scraping | 7 days |
| Dead Cache | 3 consecutive failures | Stop scraping | 24 hours |
| Permanent Block | No activity after suspension | Remove permanently | Permanent |

Status files are stored in:

- dead_cache.json
- permanent_blacklist.json
- temp_suspend.json
- last_seen.json

---

## Output Structure

The following files are generated after each run:

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
│   └── same structure
└── combined/
    └── merged outputs with source counts in headers

Each tier contains a 10-configuration overlap with the previous tier. For example, the 100-tier file includes the final 10 configurations from the 50-tier file plus 90 new configurations.

---

## Configuration Validation

Before storing any configuration, the system validates:

- vmess: required fields v, ps, add, port, id, aid + UUID validation + valid port range (1-65535)
- vless/trojan: presence of @ and # characters
- ss: valid Base64 encoding + decoded separator (:) + valid port
- Other protocols: protocol pattern validation and malicious character filtering

Invalid configurations are discarded and reported in execution logs.

---

## Telegram Channel

Subscription links, MTProto proxies, Cloudflare clean IP lists generated from large-scale scans, and daily updated configurations are available exclusively through the Telegram channel.

Subscription links are not published in this GitHub repository.

https://t.me/aristapanel

---

## Public Panel

For output customization, protocol filtering, personalized subscriptions and configuration optimization, you can use the public panel. The panel is powered by Cloudflare Workers and is completely free.

https://arista-panel.arista-panel.workers.dev/

---

<div align="center">

Made by Arista Team (🇲‌🇲‌🇩‌)❤️

</div>
