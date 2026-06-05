# AEO Content Engine — ONE-STEP Activation Checklist

> Status: **DORMANT — 4 credentials pending.** Workflow JSON validated (n8n-mcp: `valid: true`, 0 errors). Every credential slot currently holds the placeholder `id: "YOUR_CREDENTIAL_ID"`. Wire the 4 creds below, test-fire once, toggle Active. One sitting, ~20 minutes.

**Deploy target:** `AEO-Content-Engine-v7.0.json` (37 nodes, full two-model pipeline — GPT-4.1 + Gemini 2.5 Flash). This is the primary engine.
**Variant (optional):** `SKYNETJOE-AEO-ENGINE-v1.0.json` (20 nodes, GPT-only, LinkedIn post instead of Gemini research). Same 4 credential families; its nodes ship with **no credentials attached at all**, so it needs the same wiring if you activate it instead.

---

## The 4 Pending Credentials

| # | n8n Credential Type | Nodes that use it | Where to get it | Cost |
|---|---------------------|-------------------|-----------------|------|
| 1 | **Header Auth** (`httpHeaderAuth`) — Name: `X-API-KEY`, Value: your Serper key | `Serper - SERP + PAA` (1 node) | [serper.dev](https://serper.dev) → Sign up (no card) → copy key | FREE (2,500 searches) |
| 2 | **OpenAI API** (`openAiApi`) | `GPT-4.1 - Keyword Strategy`, `GPT-4.1 - Write Article`, `GPT-4.1 - AEO Editor`, `GPT-4.1 - Newsletter`, `GPT-4.1 - Video Scripts` (5 nodes) | [platform.openai.com](https://platform.openai.com) → API Keys → create key | ~$0.30-0.80/run |
| 3 | **Google Gemini (PaLM) API** (`googlePalmApi`) | `Upload to Gemini`, `Gemini - Deep Research` (2 nodes) | [ai.google.dev](https://ai.google.dev) → Get API Key | FREE tier |
| 4 | **SMTP** (`smtp`) — Gmail App Password | `Send Emails` (1 node) | Google Account → Security → 2FA → App Passwords → "Mail" | FREE |

---

## STEP 1 — Wire the 4 credentials in n8n

Open the workflow in n8n cloud (import `AEO-Content-Engine-v7.0.json` first if not already present: **Workflows → Import from File**).

1. **Serper (Header Auth)** — Credentials → New → **Header Auth**. Name field = `X-API-KEY`, Value = your Serper key. Save as "Serper.dev API Key". Open the `Serper - SERP + PAA` node → assign this credential (replaces placeholder `Header Auth account`).
2. **OpenAI** — Credentials → New → **OpenAI API**. Paste key → Save. Open EACH of the 5 GPT-4.1 nodes → assign it (replaces placeholder `OpenAi account`).
3. **Gemini** — Credentials → New → **Google PaLM API**. Paste key → Save. Open both `Upload to Gemini` and `Gemini - Deep Research` → assign it (replaces placeholder `Google Gemini(PaLM) Api account`).
4. **SMTP** — Credentials → New → **SMTP**. Host `smtp.gmail.com`, Port `465`, SSL on, User = your Gmail, Pass = the App Password. Save. Open `Send Emails` → assign it (replaces placeholder `SMTP account`).

> All credential references currently read `id: "YOUR_CREDENTIAL_ID"` — n8n will show each as "credential not found" until reassigned. Every credential-bearing node must show a real credential before testing.

## STEP 2 — Fill the Client Configuration node (required, has placeholders)

Open the **Client Configuration** node and replace the demo values:

```json
{
  "industry": "<client industry>",
  "targetAudience": "<who reads it>",
  "brandName": "<Brand> Weekly Digest",
  "keywords": "kw1, kw2, kw3, kw4, kw5",
  "recipientEmail": "client@example.com",   // currently your-client@example.com
  "senderEmail": "you@yourdomain.com",       // MUST match the Gmail used for SMTP
  "logoUrl": "https://.../logo.png",
  "brandColor": "#6366f1",
  "websiteUrl": "https://client.com/",
  "articleBaseUrl": "https://client.com/blog/"
}
```

Then open **RSS Feed Sources** and replace the four `https://example.com/industry-feed-N/...` URLs with the client's real industry RSS feeds.

> Gotcha: `senderEmail` must be the same Gmail address whose App Password you used in the SMTP credential, or Gmail will reject the send.

## STEP 3 — Validate (already done; re-run if you edit)

Pre-validated with n8n-mcp `validate_workflow`: **valid: true, 0 errors, 14 non-blocking warnings** (outdated typeVersions + a "consider onError on Send Emails" note — none block activation). No structural fixes required. If you change nodes, re-run validation.

## STEP 4 — Test-fire once

1. Click **Test Workflow** (manual run — the Weekly Trigger does not fire on test).
2. Watch each node go green. Highest-risk nodes: `Serper`, the 5 GPT nodes, the 2 Gemini nodes, `Send Emails`.
3. Check the recipient inbox for **4 branded emails**: AEO Article (with `.html` + `.doc` attachments), Newsletter Digest, Video Scripts, Instructions.
4. If `Send Emails` fails → 90% of the time it is the SMTP App Password or a `senderEmail` mismatch (Step 2 gotcha).

## STEP 5 — Activate

Toggle **Active** (top-right). The **Weekly Trigger** fires every **Monday 9:00 AM** (n8n instance timezone). Confirm the instance timezone is correct in n8n Settings so 9 AM lands where you expect.

---

## Post-activation notes
- **Dedup is automatic** — content history lives in n8n Workflow Static Data (52-week retention). To wipe it, run the `RESET History (Manual)` node by itself.
- **Cost guard:** ~$0.30-0.85/run. OpenAI is the only metered cost; Serper/Gemini/Gmail are free-tier.
- **Per-client scaling:** duplicate the workflow, swap the Client Configuration + RSS Feed Sources nodes — credentials are reusable across copies.
- **Optional hardening (not required to activate):** bump GPT nodes to typeVersion 2.3, HTTP nodes to 4.4, Gemini nodes to 1.2, and add `onError` to `Send Emails`.
