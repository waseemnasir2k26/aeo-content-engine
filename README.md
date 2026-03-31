<div align="center">

# AEO Content Engine v7.0

### AI-Powered Content Pipeline for Answer Engine Optimization

**Automated weekly content generation using GPT-4.1 + Gemini 2.5 Flash — optimized for AI answer engines (ChatGPT, Google AI Overviews, Perplexity).**

`n8n Workflow` `GPT-4.1` `Gemini 2.5 Flash` `AEO` `SEO` `Content Automation`

[![Import to n8n](https://img.shields.io/badge/Import_to_n8n-EA4B71?style=for-the-badge&logo=n8n&logoColor=white)](#quick-start)
[![License: MIT](https://img.shields.io/badge/License-MIT-green?style=for-the-badge)](LICENSE)

</div>

---

## What Is This?

A fully automated n8n workflow that generates **AEO-optimized content** every week — articles, newsletters, and video scripts — using a two-model AI pipeline. Built for agencies and content teams who want to rank in both traditional search AND AI answer engines.

**AEO (Answer Engine Optimization)** is the practice of optimizing content so AI systems like ChatGPT, Google AI Overviews, and Perplexity cite your content as a source. This workflow bakes AEO best practices directly into the content generation pipeline.

---

## How It Works

```
┌─────────────┐     ┌──────────────────┐     ┌─────────────────┐     ┌──────────────────┐
│  PHASE 1    │     │  PHASE 2         │     │  PHASE 3        │     │  PHASE 4         │
│  Keywords   │────▶│  Deep Research   │────▶│  Content Gen    │────▶│  Email Delivery  │
│             │     │                  │     │                 │     │                  │
│ Autocomplete│     │ 8 RSS Feeds      │     │ GPT-4.1 Article │     │ 📧 AEO Article   │
│ Serper SERP │     │ Gemini 2.5 Flash │     │ GPT-4.1 AEO Edit│     │ 📧 Newsletter    │
│ GPT-4.1     │     │ Trend Analysis   │     │ GPT-4.1 News    │     │ 📧 Video Scripts │
│ Strategy    │     │ Story Ranking    │     │ GPT-4.1 Scripts │     │ 📧 Instructions  │
└─────────────┘     └──────────────────┘     └─────────────────┘     └──────────────────┘
```

### Phase 1: Keyword Research (FREE APIs)
- **Google Autocomplete** — real trending searches (no API key needed)
- **Serper.dev** — SERP data + People Also Ask questions (2,500 free searches)
- **GPT-4.1** — analyzes data → outputs keyword strategy with AEO angles

### Phase 2: Deep Research
- Fetches **8+ RSS feeds** from industry sources
- **Gemini 2.5 Flash** analyzes all stories, ranks by relevance, extracts data points
- Only includes stories with specific facts (company names, dollar amounts, dates)

### Phase 3: Content Generation (GPT-4.1)
- **AEO Article** (800-1000 words) — direct-answer opening, question-format headings, FAQ section
- **AEO Editor Pass** — scores article on 5 criteria, makes targeted optimizations
- **Newsletter Digest** — 8-12 categorized stories with branded HTML
- **Video Scripts** — short-form (60s for Reels/TikTok) + long-form (5min for YouTube)

### Phase 4: Email Delivery (4 Branded Emails)
1. **AEO Article** — full article + `.html` and `.doc` attachments for easy CMS upload
2. **Newsletter Digest** — categorized stories with inline styling
3. **Video Scripts** — ready-to-record scripts with visual cues
4. **Instructions** — step-by-step publishing guide (record videos → upload article → send newsletter)

---

## Key Features

| Feature | Description |
|---------|-------------|
| **Two-Model Pipeline** | GPT-4.1 for strategy + writing, Gemini 2.5 Flash for research |
| **AEO Optimization** | Direct-answer openings, PAA-based headings, FAQ sections |
| **AEO Scoring** | 5-criteria scoring (0-100) with specific optimization notes |
| **Content Deduplication** | Tracks 52 weeks of history — never repeats topics, keywords, or stories |
| **Article Structure Rotation** | 3 formats cycle automatically (deep-dive, problem-solution, case-study) |
| **Buzzword Quality Gate** | Flags corporate jargon (leverage, synergy, cutting-edge, etc.) |
| **Date Enforcement** | Rejects outdated 2024/2025 content — current year only |
| **CMS-Ready Attachments** | `.html` file for copy/paste into any CMS, `.doc` for Word editing |
| **Client Instructions Email** | Step-by-step guide so clients know exactly what to do each week |
| **Branded Email Templates** | Customizable colors, logos, fonts — professional email output |
| **FREE Keyword Research** | Google Autocomplete + Serper.dev free tier = $0/month for keywords |

---

## Quick Start

### 1. Import the Workflow

1. Open your n8n instance
2. Go to **Workflows** → **Import from File**
3. Select `AEO-Content-Engine-v7.0.json`

### 2. Set Up Credentials (3 required + 1 for email)

| Credential | Where to Get | Cost |
|-----------|-------------|------|
| **Serper.dev API Key** | [serper.dev](https://serper.dev) → Sign up (no credit card) | FREE (2,500 searches) |
| **OpenAI API Key** | [platform.openai.com](https://platform.openai.com) → API Keys | Pay-per-use (~$0.50-1/run) |
| **Google Gemini API Key** | [ai.google.dev](https://ai.google.dev) → Get API Key | FREE tier available |
| **SMTP (Gmail)** | Google Account → Security → App Passwords | FREE |

<details>
<summary><b>📋 Detailed Credential Setup</b></summary>

#### Serper.dev (FREE — 2,500 searches)
1. Go to serper.dev → Sign up (no credit card needed)
2. Copy your API key from the dashboard
3. In n8n: **Credentials** → **New** → **Header Auth**
4. Name: `X-API-KEY` | Value: paste your key
5. Save as "Serper.dev API Key"
6. Assign to the `Serper - SERP + PAA` node

#### OpenAI API (GPT-4.1)
1. Go to platform.openai.com → API Keys
2. Create a new API key
3. In n8n: **Credentials** → **New** → **OpenAI API**
4. Paste your API key → Save
5. Assign to all 5 GPT nodes

#### Google Gemini API
1. Go to ai.google.dev → Get API Key
2. Create key in Google Cloud project
3. In n8n: **Credentials** → **New** → **Google PaLM API**
4. Paste your API key → Save
5. Assign to both Gemini nodes

#### SMTP (Gmail App Password)
1. Enable 2FA on your Google Account
2. Google Account → Security → App Passwords
3. Generate an App Password for 'Mail'
4. In n8n: **Credentials** → **New** → **SMTP**
5. Host: `smtp.gmail.com` | Port: `465` | SSL: Yes
6. User: your Gmail | Pass: app password

</details>

### 3. Customize for Your Client

Open the **Client Configuration** node and update:

```json
{
  "industry": "Your Industry",
  "targetAudience": "Your Target Audience",
  "brandName": "Your Brand Weekly Digest",
  "tone": "Your writing tone description",
  "keywords": "keyword1, keyword2, keyword3",
  "recipientEmail": "client@example.com",
  "senderEmail": "sender@example.com",
  "logoUrl": "https://your-logo.com/logo.png",
  "brandColor": "#6366f1",
  "websiteUrl": "https://your-website.com/",
  "articleBaseUrl": "https://your-website.com/blog/"
}
```

Then update the **RSS Feed Sources** node with your industry's RSS feeds.

### 4. Test & Activate

1. Click **Test Workflow** to run once
2. Check your email for 4 branded emails
3. If everything looks good → toggle **Active**

---

## What the Client Receives (4 Emails)

### Email 1: AEO Article
Full article optimized for AI answer engines. Includes AEO score, optimization notes, and both `.html` + `.doc` file attachments for easy CMS upload.

### Email 2: Newsletter Digest
8-12 curated industry stories grouped by category with branded styling. Ready to paste into any email CRM.

### Email 3: Video Scripts
Two scripts ready to record:
- **Short-form** (under 60 seconds) for Reels, TikTok, YouTube Shorts
- **Long-form** (~5 minutes) for YouTube with timestamps and B-roll suggestions

### Email 4: Instructions
Step-by-step publishing guide:
1. Record videos using [Teleprompter App](https://apps.apple.com/us/app/teleprompter/id941620509)
2. Upload article to CMS (copy/paste from .html file)
3. Add article link to newsletter
4. Send newsletter via CRM

---

## Upgrade Options

The workflow uses **free APIs by default**. When ready to scale:

| Upgrade | Replaces | Cost | Benefit |
|---------|----------|------|---------|
| DataForSEO | Autocomplete + Serper | ~$0.002/query | Exact search volume, keyword difficulty, CPC |
| SerpAPI | Serper | $75/mo | Google Trends data |
| SEMrush | All keyword nodes | $500/mo | Industry-leading keyword database |
| Google Search Console | Add alongside (don't replace) | FREE | Real clicks, impressions, CTR tracking |

---

## Architecture

```
Weekly Trigger (Monday 9 AM)
    │
    ▼
Client Configuration ──▶ Prepare Keywords (rotation + dedup)
    │
    ▼
Google Autocomplete ──▶ Autocomplete Questions ──▶ Serper SERP+PAA
    │
    ▼
Merge Keyword Data ──▶ GPT-4.1 Keyword Strategy ──▶ Parse Strategy
    │
    ├──▶ RSS Feed Sources ──▶ Loop Feeds ──▶ CSV ──▶ Gemini Upload
    │       │
    │       ▼
    │    Gemini 2.5 Flash Deep Research ──▶ Parse Research
    │
    ▼
GPT-4.1 Write Article ──▶ GPT-4.1 AEO Editor ──▶ Finalize Article
    │
    ├──▶ GPT-4.1 Newsletter ──▶ Clean Newsletter
    │
    ├──▶ GPT-4.1 Video Scripts ──▶ Clean Scripts
    │
    ▼
Build 4 Branded Emails ──▶ Send Emails (SMTP) ──▶ Save Content History
```

---

## Deduplication System

The workflow automatically prevents content repetition:

- **Keyword rotation** — avoids last 8 used primary keywords
- **Story filtering** — removes recently featured URLs and titles (4-week window)
- **Angle exclusion** — GPT is instructed to avoid previously covered angles
- **Title tracking** — never repeats an article title
- **History retention** — keeps 52 weeks (1 year) of content history
- **Storage** — n8n Workflow Static Data (built-in, no external DB needed)

To reset history: run the `RESET History (Manual)` node by itself.

---

## Cost Per Run

| Service | Cost |
|---------|------|
| Google Autocomplete | FREE |
| Serper.dev | FREE (2,500/mo) |
| GPT-4.1 (5 calls) | ~$0.30-0.80 |
| Gemini 2.5 Flash | ~$0.01-0.05 |
| Gmail SMTP | FREE |
| **Total per week** | **~$0.30-0.85** |

---

## Built By

**[Skynet Labs](https://www.skynetjoe.com)** — AI Automation Agency

Built for agency clients who need automated, high-quality content that ranks in both traditional search and AI answer engines.

---

## License

MIT — use it, modify it, build on it.
