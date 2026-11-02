# AEO Content Engine

**An n8n workflow that writes a weekly answer-engine-optimized article, a newsletter digest and two video scripts, then emails them to you for review.**

![License: MIT](https://img.shields.io/badge/License-MIT-green) ![n8n](https://img.shields.io/badge/built%20for-n8n-EA4B71)

Publishing content that AI answer engines can quote is slow by hand: keyword research, source gathering, drafting, an editing pass, formatting. This workflow runs that chain once a week and hands you drafts.

## What it does

- Pulls keyword ideas from Google Autocomplete and Serper.dev (SERP and People Also Ask).
- Reads RSS feeds you choose and has Gemini 2.5 Flash rank the stories and pull out concrete facts.
- Has GPT-4.1 write an 800-1000 word article with a direct-answer opening, question headings and an FAQ, then run an editor pass that scores it.
- Writes a newsletter digest and two video scripts (about 60 seconds and about 5 minutes).
- Emails you four messages: article (with `.html` and `.doc` attachments), newsletter, scripts and a publishing checklist.
- Keeps 52 weeks of history in n8n workflow static data so topics, keywords and stories do not repeat.

## Quickstart

1. In n8n: **Workflows > Import from File** and choose `AEO-Content-Engine-v7.0.json`.
2. Create credentials: Serper.dev (Header Auth, header `X-API-KEY`), OpenAI, Google Gemini (PaLM) and SMTP.
3. Open the **Client Configuration** node and set industry, audience, brand name, tone, keywords, recipient and sender email, logo URL and site URLs.
4. Edit the **RSS Feed Sources** node to match your industry.
5. Click **Test Workflow**, check the four emails, then toggle the workflow **Active** (it triggers Monday 9 AM).

`SKYNETJOE-AEO-ENGINE-v1.0.json` is the earlier variant, kept for reference.

## Cost

Rough per-run figure from the author's own usage: about $0.30-0.85, nearly all of it GPT-4.1 calls. Autocomplete, the Serper free tier and Gemini's free tier cover the rest. Your usage will differ.

## For you if

You run content for an agency or a small business, you already use n8n, and you want drafts to review, not an auto-publisher.

## Status and limits

- Nothing is published for you. Output is email only; a human edits and posts.
- The AEO score comes from the model's own editor prompt. Treat it as a checklist, not a measurement.
- Models and API terms change; re-test after updating nodes.
- Last reviewed October 2026.

## Built by SkynetLabs

Built by [SkynetLabs](https://skynetjoe.com). Questions: waseem@skynetjoe.com

Need this wired into your business? SkynetLabs builds voice agents, n8n back offices and sites that convert → https://skynetjoe.com
