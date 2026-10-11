# Changelog

All notable changes to this project are documented in this file.

## [2026.10] - 2026-10-12

- October 2026 review of aeo-content-engine, a public repo distributing the AEO Content Engine v7.0 n8n workflow (plus SKYNETJOE-AEO-ENGINE-v1.0) for Answer Engine Optimization content; MIT licensed.
- Status: unchanged since the April 2026 content commits; the repo is two exportable workflow JSON files, a long README and two strategy documents, not an application.
- Reviewed this month: README external links checked (all reachable except platform.openai.com, which returns 403 to scripted requests, and three `your-website.com` / `your-logo.com` example placeholders that are intentional). The existing Hire Me section now points at the current Fiverr, Upwork and Calendly links.
- Known gaps: no automated validation of the workflow JSON; model references (GPT-4.1, Gemini 2.5 Flash) and per-run cost figures date from the original build and are not re-benchmarked. No workflow, prompt or logic changes in this release.

## [2026.09] - 2026-09-16

- Maintenance review of aeo-content-engine — a public repo distributing the AEO Content Engine v7.0 n8n workflow for Answer Engine Optimization content generation.
- Status: not an application — the repo ships two exportable n8n workflow JSON files (`AEO-Content-Engine-v7.0.json`, `SKYNETJOE-AEO-ENGINE-v1.0.json`), a long README documenting the four-phase pipeline (keyword research, deep research over RSS feeds, GPT-4.1/Gemini content generation, email delivery), plus `AEO-DEEP-RESEARCH-STRATEGY.md` and `UPSELL-PROPOSAL.md`. MIT licensed.
- Reviewed September 2026: README Status section added and a CHANGELOG created; the repo is versioned as v2026.09. No workflow JSON, prompt or documentation logic was changed.
- Known gaps: no CHANGELOG before this release; no automated validation of the workflow JSON; the README's model references (GPT-4.1, Gemini 2.5 Flash) and per-run cost figures date from the original build and have not been re-benchmarked; last functional commit was April 2026.
