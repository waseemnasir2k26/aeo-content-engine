"""
build_v2.py — SkynetJoe AEO Content Engine v2.0 Builder

Generates TWO n8n workflow JSON files:
  1. SKYNETJOE-DAILY-DIGEST-v2.0.json  — Daily AI + Travel Digest  (~15 nodes)
  2. SKYNETJOE-WEEKLY-AEO-v2.0.json    — Weekly AEO Engine, 5-agent split (~50 nodes)

Architecture:
  - Daily Digest: Schedule -> Config -> RSS loop -> GPT curate -> Email
  - Weekly AEO:   5 independent Schedule Triggers (Mon-Fri), each running its own
                  agent chain.  State shared via $getWorkflowStaticData('global').pipeline.
                  Mon=Keywords, Tue=Research, Wed=Article, Thu=Newsletter, Fri=Scripts+Brand.

Run:  python build_v2.py
"""

import json
import uuid
import os
import textwrap

# ---------------------------------------------------------------------------
# Output directory = same folder as this script
# ---------------------------------------------------------------------------
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
DAILY_OUT = os.path.join(SCRIPT_DIR, "SKYNETJOE-DAILY-DIGEST-v2.0.json")
WEEKLY_OUT = os.path.join(SCRIPT_DIR, "SKYNETJOE-WEEKLY-AEO-v2.0.json")

# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def uid():
    """Generate a fresh UUID-v4 string."""
    return str(uuid.uuid4())


def schedule_trigger(name, pos, cron_expr):
    """Schedule Trigger node using a raw cron expression."""
    return {
        "parameters": {
            "rule": {
                "interval": [
                    {
                        "field": "cronExpression",
                        "expression": cron_expr
                    }
                ]
            }
        },
        "id": uid(),
        "name": name,
        "type": "n8n-nodes-base.scheduleTrigger",
        "typeVersion": 1.2,
        "position": pos,
    }


def manual_trigger(name, pos):
    """Manual Trigger node."""
    return {
        "parameters": {},
        "id": uid(),
        "name": name,
        "type": "n8n-nodes-base.manualTrigger",
        "typeVersion": 1,
        "position": pos,
    }


def set_node(name, pos, string_values=None, number_values=None):
    """Set node (v3.4) with string and/or number values."""
    values = {}
    if string_values:
        values["string"] = [{"name": k, "value": v} for k, v in string_values.items()]
    if number_values:
        values["number"] = [{"name": k, "value": v} for k, v in number_values.items()]
    return {
        "parameters": {"values": values},
        "id": uid(),
        "name": name,
        "type": "n8n-nodes-base.set",
        "typeVersion": 3.4,
        "position": pos,
    }


def code_node(name, pos, js_code):
    """Code (JavaScript) node."""
    return {
        "parameters": {"jsCode": js_code},
        "id": uid(),
        "name": name,
        "type": "n8n-nodes-base.code",
        "typeVersion": 2,
        "position": pos,
    }


def http_get(name, pos, url_expr, response_format="text", query_params=None, creds=None):
    """HTTP Request node — GET."""
    params = {
        "url": url_expr,
        "options": {"response": {"response": {"neverError": True}}},
    }
    if response_format == "json":
        params["options"]["response"]["response"]["responseFormat"] = "json"
    if query_params:
        params["queryParameters"] = {
            "parameters": [{"name": k, "value": v} for k, v in query_params.items()]
        }
    node = {
        "parameters": params,
        "id": uid(),
        "name": name,
        "type": "n8n-nodes-base.httpRequest",
        "typeVersion": 4.2,
        "position": pos,
    }
    if creds:
        node["credentials"] = creds
    return node


def http_post(name, pos, url, body_expr, creds=None, content_type="application/json",
              auth_type=None, node_cred_type=None):
    """HTTP Request node — POST with JSON body."""
    params = {
        "url": url,
        "method": "POST",
        "sendBody": True,
        "specifyBody": "json",
        "jsonBody": body_expr,
        "options": {"response": {"response": {"neverError": True}}},
    }
    if auth_type == "predefined" and node_cred_type:
        params["authentication"] = "predefinedCredentialType"
        params["nodeCredentialType"] = node_cred_type
    node = {
        "parameters": params,
        "id": uid(),
        "name": name,
        "type": "n8n-nodes-base.httpRequest",
        "typeVersion": 4.2,
        "position": pos,
    }
    if creds:
        node["credentials"] = creds
    return node


def http_post_raw_body(name, pos, url, body_params, creds=None,
                       auth_type=None, node_cred_type=None):
    """HTTP Request node — POST with key/value body parameters."""
    params = {
        "url": url,
        "method": "POST",
        "sendBody": True,
        "bodyParameters": {
            "parameters": [{"name": k, "value": v} for k, v in body_params.items()]
        },
        "options": {"response": {"response": {"neverError": True}}},
    }
    if auth_type == "predefined" and node_cred_type:
        params["authentication"] = "predefinedCredentialType"
        params["nodeCredentialType"] = node_cred_type
    node = {
        "parameters": params,
        "id": uid(),
        "name": name,
        "type": "n8n-nodes-base.httpRequest",
        "typeVersion": 4.2,
        "position": pos,
    }
    if creds:
        node["credentials"] = creds
    return node


def split_in_batches(name, pos, batch_size=5):
    """SplitInBatches node."""
    return {
        "parameters": {"batchSize": batch_size, "options": {}},
        "id": uid(),
        "name": name,
        "type": "n8n-nodes-base.splitInBatches",
        "typeVersion": 3,
        "position": pos,
    }


def openai_node(name, pos, system_prompt, user_prompt, temp=0.7, max_tokens=2048,
                model="gpt-4.1"):
    """OpenAI (LangChain) chat node."""
    return {
        "parameters": {
            "modelId": {"__rl": True, "value": model, "mode": "id"},
            "messages": {
                "values": [
                    {"content": system_prompt, "role": "system"},
                    {"content": user_prompt},
                ]
            },
            "options": {
                "temperature": temp,
                "maxTokens": max_tokens,
            },
        },
        "id": uid(),
        "name": name,
        "type": "@n8n/n8n-nodes-langchain.openAi",
        "typeVersion": 1.8,
        "position": pos,
        "credentials": {
            "openAiApi": {
                "id": "REPLACE_WITH_YOUR_OPENAI_CREDENTIAL_ID",
                "name": "OpenAI API",
            }
        },
    }


def email_send(name, pos, to_expr, from_expr, subject_expr, html_expr):
    """Email Send (SMTP) node."""
    return {
        "parameters": {
            "fromEmail": from_expr,
            "toEmail": to_expr,
            "subject": subject_expr,
            "emailFormat": "html",
            "html": html_expr,
            "options": {},
        },
        "id": uid(),
        "name": name,
        "type": "n8n-nodes-base.emailSend",
        "typeVersion": 2.1,
        "position": pos,
        "credentials": {
            "smtp": {
                "id": "REPLACE_WITH_YOUR_SMTP_CREDENTIAL_ID",
                "name": "SMTP",
            }
        },
    }


def connect(*chain):
    """Build connections dict from a linear chain of node names.
    Accepts a list of node-name strings. Parallel branches are expressed
    as a list-of-lists (see build_connections for the advanced version)."""
    conns = {}
    for i in range(len(chain) - 1):
        src = chain[i]
        tgt = chain[i + 1]
        if isinstance(tgt, list):
            # Parallel targets
            conns[src] = {"main": [[{"node": t, "type": "main", "index": 0} for t in tgt]]}
        else:
            conns[src] = {"main": [[{"node": tgt, "type": "main", "index": 0}]]}
    return conns


def merge_connections(*dicts):
    """Merge multiple connection dicts, handling duplicate source keys."""
    merged = {}
    for d in dicts:
        for src, val in d.items():
            if src not in merged:
                merged[src] = val
            else:
                # Append to existing main outputs
                for out_list in val["main"]:
                    merged[src]["main"][0].extend(out_list)
    return merged


def build_workflow(name, nodes, connections):
    """Assemble a full n8n workflow JSON structure."""
    return {
        "name": name,
        "nodes": nodes,
        "connections": connections,
        "active": False,
        "settings": {"executionOrder": "v1"},
        "versionId": uid(),
        "meta": {"templateCredsSetupCompleted": True, "instanceId": uid()},
        "id": uid(),
        "tags": [],
    }


# ============================================================================
#  RSS FEED LIST  (20 curated feeds)
# ============================================================================

RSS_FEEDS = [
    # AI / Tech (10)
    {"url": "https://techcrunch.com/category/artificial-intelligence/feed/", "category": "AI", "name": "TechCrunch AI"},
    {"url": "https://www.theverge.com/rss/ai-artificial-intelligence/index.xml", "category": "AI", "name": "The Verge AI"},
    {"url": "https://feeds.feedburner.com/venturebeat/SZYF", "category": "AI", "name": "VentureBeat"},
    {"url": "https://www.technologyreview.com/topic/artificial-intelligence/feed", "category": "AI", "name": "MIT Tech Review"},
    {"url": "https://arstechnica.com/feed/", "category": "AI", "name": "Ars Technica"},
    {"url": "https://blog.n8n.io/rss/", "category": "AI", "name": "n8n Blog"},
    {"url": "https://openai.com/blog/rss.xml", "category": "AI", "name": "OpenAI Blog"},
    {"url": "https://www.marktechpost.com/feed/", "category": "AI", "name": "MarkTechPost"},
    {"url": "https://hnrss.org/best", "category": "AI", "name": "HN Best"},
    {"url": "https://www.artificialintelligence-news.com/feed/", "category": "AI", "name": "AI News"},
    # Travel (5)
    {"url": "https://www.nomadicmatt.com/travel-blog/feed/", "category": "Travel", "name": "Nomadic Matt"},
    {"url": "https://thepointsguy.com/feed/", "category": "Travel", "name": "The Points Guy"},
    {"url": "https://www.skyscanner.net/news/feed/", "category": "Travel", "name": "Skyscanner"},
    {"url": "https://www.travelandleisure.com/feeds/all", "category": "Travel", "name": "Travel+Leisure"},
    {"url": "https://nomadlist.com/feed", "category": "Travel", "name": "NomadList"},
    # Business (5)
    {"url": "https://smallbiztrends.com/feed", "category": "Business", "name": "Small Biz Trends"},
    {"url": "https://www.indiehackers.com/feed.xml", "category": "Business", "name": "Indie Hackers"},
    {"url": "https://review.firstround.com/feed.xml", "category": "Business", "name": "First Round Review"},
    {"url": "https://www.saastr.com/feed/", "category": "Business", "name": "SaaStr"},
    {"url": "https://hbr.org/feed", "category": "Business", "name": "HBR"},
]

RSS_FEEDS_JSON = json.dumps(RSS_FEEDS)

# ============================================================================
#  SKYNETJOE CONFIG VALUES  (shared across both workflows)
# ============================================================================

SKYNETJOE_CONFIG = {
    "brandName": "SkynetJoe",
    "founderName": "Waseem Nasir",
    "industry": "AI Automation Agency",
    "targetAudience": "Small Business Owners, Entrepreneurs, Freelancers",
    "tone": "Sharp, data-driven, practitioner voice. No corporate buzzwords.",
    "brandColor": "#13b973",
    "secondaryColor": "#8B5CF6",
    "websiteUrl": "https://www.skynetjoe.com",
    "recipientEmail": "waseemhome8@gmail.com",
    "senderEmail": "waseem@skynetjoe.com",
    "travelContext": "Currently traveling ASEAN (Bali, Indonesia). Running AI agency remotely.",
}

WEEKLY_EXTRA_CONFIG = {
    "keywords": "AI automation for small business, AI employee, n8n automation, chatbot development, AI workflow automation, business process automation, AI implementation guide, AI cost for SMB, AI vs hiring, custom AI solutions, AI agency services, web development with AI, social media automation, digital nomad AI business, remote CEO lifestyle, AI tools for entrepreneurs, Bali coworking for tech founders, ASEAN startup scene, travel while running business, location independent agency",
    "travelKeywords": "digital nomad Bali, remote work Indonesia, coworking Canggu, CEO lifestyle abroad, running agency while traveling, ASEAN business, Bali cost of living, digital nomad visa Indonesia",
    "articleBaseUrl": "https://www.skynetjoe.com/blog/",
    "logoUrl": "",
    "linkedinProfile": "https://www.linkedin.com/in/waseemnasir/",
}


# ############################################################################
#                        WORKFLOW 1  —  DAILY DIGEST
# ############################################################################

def build_daily_digest():
    """Build the Daily AI + Travel Digest workflow (~15 nodes)."""
    nodes = []
    connections = {}

    # --- 1. Schedule Trigger (daily 7 AM WITA = 23:00 UTC) ---
    n_sched = schedule_trigger("Schedule - Daily 7AM", [220, 300], "0 23 * * *")
    nodes.append(n_sched)

    # --- 2. SkynetJoe Config ---
    n_config = set_node("SkynetJoe Config", [460, 300], string_values=SKYNETJOE_CONFIG)
    nodes.append(n_config)

    # --- 3. RSS Feed URLs ---
    rss_code = textwrap.dedent(f"""\
    // Output 20 RSS feed objects for the SplitInBatches loop
    const feeds = {RSS_FEEDS_JSON};
    return feeds.map(f => ({{ json: f }}));
    """)
    n_rss = code_node("RSS Feed URLs", [700, 300], rss_code)
    nodes.append(n_rss)

    # --- 4. Split Feeds ---
    n_split = split_in_batches("Split Feeds", [940, 300], batch_size=5)
    nodes.append(n_split)

    # --- 5. Fetch Feed ---
    n_fetch = http_get("Fetch Feed", [1180, 300], "={{ $json.url }}")
    nodes.append(n_fetch)

    # --- 6. Merge Feed Data ---
    merge_code = textwrap.dedent("""\
    // Consolidate all RSS responses into a single stories array.
    // Each batch item carries the HTTP response text + original feed metadata.
    const items = $input.all();
    const stories = [];
    const failedFeeds = [];
    const now = Date.now();
    const HOURS_48 = 48 * 60 * 60 * 1000;

    for (const item of items) {
      const feedName = item.json.name || 'Unknown';
      const feedCategory = item.json.category || 'AI';
      const raw = item.json.data || item.json.body || '';
      if (!raw || typeof raw !== 'string' || raw.length < 100) {
        failedFeeds.push(feedName);
        continue;
      }
      // Simple XML item extraction (works for RSS 2.0 and Atom)
      const itemRegex = /<item[\\s>][\\s\\S]*?<\\/item>|<entry[\\s>][\\s\\S]*?<\\/entry>/gi;
      const matches = raw.match(itemRegex) || [];
      for (const m of matches) {
        const title = (m.match(/<title[^>]*>(?:<!\\[CDATA\\[)?(.*?)(?:\\]\\]>)?<\\/title>/s) || [])[1] || '';
        const link = (m.match(/<link[^>]*href="([^"]*)"/) || m.match(/<link[^>]*>(.*?)<\\/link>/) || [])[1] || '';
        const desc = (m.match(/<description[^>]*>(?:<!\\[CDATA\\[)?(.*?)(?:\\]\\]>)?<\\/description>/s) ||
                      m.match(/<summary[^>]*>(?:<!\\[CDATA\\[)?(.*?)(?:\\]\\]>)?<\\/summary>/s) || [])[1] || '';
        const pubDate = (m.match(/<pubDate[^>]*>(.*?)<\\/pubDate>/) ||
                         m.match(/<published[^>]*>(.*?)<\\/published>/) ||
                         m.match(/<updated[^>]*>(.*?)<\\/updated>/) || [])[1] || '';
        const ts = pubDate ? new Date(pubDate).getTime() : 0;
        if (ts && (now - ts) > HOURS_48) continue;  // skip old stories
        const cleanDesc = desc.replace(/<[^>]*>/g, '').substring(0, 300);
        stories.push({ title: title.trim(), link: link.trim(), description: cleanDesc.trim(), pubDate, source: feedName, category: feedCategory });
      }
    }

    // Deduplicate by URL
    const seen = new Set();
    const unique = stories.filter(s => {
      if (!s.link || seen.has(s.link)) return false;
      seen.add(s.link);
      return true;
    });

    // Sort by recency (newest first), take top 30
    unique.sort((a, b) => new Date(b.pubDate) - new Date(a.pubDate));
    const top30 = unique.slice(0, 30);

    return [{ json: { stories: top30, totalFetched: items.length, failed: failedFeeds, storyCount: top30.length } }];
    """)
    n_merge = code_node("Merge Feed Data", [1420, 300], merge_code)
    nodes.append(n_merge)

    # --- 7. GPT Curate Daily Digest ---
    system_prompt = (
        "=You are the editorial AI for SkynetJoe, an AI automation agency run by Waseem Nasir. "
        "Waseem is currently traveling in ASEAN (Bali, Indonesia) while running his agency remotely."
    )
    user_prompt = textwrap.dedent("""\
    =Here are today's stories from 20 RSS feeds across AI/Tech, Travel, and Business:

    {{ JSON.stringify($json.stories, null, 2) }}

    Your tasks:
    1. Pick the TOP 5 most relevant stories for SkynetJoe's audience (small business owners, entrepreneurs wanting AI automation). At least 1 must be travel/nomad related.
    2. For each story, write: a) One-line hook (bold, attention-grabbing) b) 2-3 sentence summary with a specific stat or insight c) Source attribution with link
    3. Generate a TRAVEL HACK OF THE DAY: a practical, specific tip for digital nomads in ASEAN/Bali. Rotate through categories: visa tips, coworking reviews, cost hacks, internet/SIM, food, safety, culture, transportation, accommodation, apps.
    4. Write a LinkedIn-ready text post (150-200 words) based on the #1 story. Bold opening, 1 stat, practitioner voice, ends with question. No emojis. 3 hashtags.
    5. Check against previously featured stories (provided below) and do NOT repeat any.

    Previously featured (last 7 days): {{ JSON.stringify($getWorkflowStaticData('global').digestHistory || []) }}

    Return ONLY valid JSON:
    {
      "topStories": [{"title": "", "hook": "", "summary": "", "source": "", "url": "", "category": ""}],
      "travelHack": {"category": "", "title": "", "tip": "", "proTip": ""},
      "linkedinPost": "",
      "digestSubject": ""
    }
    """)
    n_gpt = openai_node("GPT Curate Daily Digest", [1660, 300], system_prompt, user_prompt,
                         temp=0.6, max_tokens=2048)
    nodes.append(n_gpt)

    # --- 8. Parse Digest ---
    parse_code = textwrap.dedent("""\
    // Parse GPT JSON response for the daily digest
    const items = $input.all();
    function extractText(r) {
      if (!r) return '';
      if (typeof r === 'string') return r;
      if (r.text) return r.text;
      if (r.message?.content) return r.message.content;
      if (r.output) return typeof r.output === 'string' ? r.output : JSON.stringify(r.output);
      return JSON.stringify(r);
    }
    const raw = extractText(items[0]?.json);
    let digest;
    try {
      const cleaned = raw.replace(/```json\\n?/g, '').replace(/```\\n?/g, '').trim();
      digest = JSON.parse(cleaned);
    } catch(e) {
      const jsonMatch = raw.match(/\\{[\\s\\S]*\\}/);
      try { digest = JSON.parse(jsonMatch[0]); } catch(e2) {
        digest = { topStories: [], travelHack: {}, linkedinPost: '', digestSubject: 'SkynetJoe Daily AI Digest' };
      }
    }
    return [{ json: digest }];
    """)
    n_parse = code_node("Parse Digest", [1900, 300], parse_code)
    nodes.append(n_parse)

    # --- 9. Build Digest Email ---
    build_email_code = textwrap.dedent("""\
    // Build branded HTML email for the daily digest
    const digest = $input.first().json;
    const config = $('SkynetJoe Config').first().json;
    const brandColor = config.brandColor || '#13b973';
    const secondaryColor = config.secondaryColor || '#8B5CF6';
    const websiteUrl = config.websiteUrl || 'https://www.skynetjoe.com';
    const founderName = config.founderName || 'Waseem Nasir';
    const today = new Date().toLocaleDateString('en-US', { weekday: 'long', year: 'numeric', month: 'long', day: 'numeric' });

    const categoryColors = { AI: '#3b82f6', Travel: '#10b981', Business: '#f59e0b' };

    // Story cards
    let storyCards = '';
    for (const s of (digest.topStories || [])) {
      const catColor = categoryColors[s.category] || brandColor;
      storyCards += `
      <div style="background:#1a1a2e;border-radius:10px;padding:20px;margin-bottom:16px;border-left:4px solid ${catColor};">
        <span style="display:inline-block;background:${catColor};color:#fff;font-size:10px;padding:3px 8px;border-radius:4px;text-transform:uppercase;letter-spacing:1px;margin-bottom:10px;">${s.category || 'AI'}</span>
        <h3 style="color:#fff;margin:0 0 8px;font-size:16px;line-height:1.4;">${s.hook || s.title}</h3>
        <p style="color:#ccc;margin:0 0 10px;font-size:14px;line-height:1.6;">${s.summary}</p>
        <a href="${s.url}" style="color:${brandColor};font-size:13px;text-decoration:none;">Read more at ${s.source} &rarr;</a>
      </div>`;
    }

    // Travel hack
    const hack = digest.travelHack || {};
    const travelSection = hack.title ? `
    <div style="background:#0d2818;border-radius:10px;padding:20px;margin:24px 0;border:1px solid ${brandColor};">
      <p style="font-size:12px;text-transform:uppercase;letter-spacing:2px;color:${brandColor};margin:0 0 8px;">TRAVEL HACK OF THE DAY &mdash; ${hack.category || 'Bali'}</p>
      <h3 style="color:#fff;margin:0 0 10px;font-size:18px;">${hack.title}</h3>
      <p style="color:#ccc;margin:0 0 10px;font-size:14px;line-height:1.6;">${hack.tip}</p>
      ${hack.proTip ? `<p style="color:${brandColor};margin:0;font-size:13px;"><strong>Pro tip:</strong> ${hack.proTip}</p>` : ''}
    </div>` : '';

    // LinkedIn post
    const linkedinSection = digest.linkedinPost ? `
    <div style="margin:24px 0;">
      <p style="font-size:12px;text-transform:uppercase;letter-spacing:2px;color:${secondaryColor};margin:0 0 12px;">LINKEDIN POST (COPY-READY)</p>
      <div style="background:#111;border-radius:8px;padding:20px;border:1px solid #333;font-family:monospace;white-space:pre-wrap;color:#e0e0e0;font-size:13px;line-height:1.7;">${digest.linkedinPost}</div>
    </div>` : '';

    const html = `<!DOCTYPE html>
    <html>
    <head><meta charset="utf-8"><meta name="viewport" content="width=device-width"></head>
    <body style="margin:0;padding:0;background:#0a0a0a;font-family:-apple-system,BlinkMacSystemFont,'Segoe UI',Roboto,sans-serif;">
    <table width="100%" cellpadding="0" cellspacing="0" style="max-width:640px;margin:0 auto;">
      <tr><td style="background:linear-gradient(135deg,${secondaryColor},${brandColor});padding:32px 24px;text-align:center;">
        <h1 style="color:#fff;margin:0 0 4px;font-size:24px;">SkynetJoe Daily AI + Travel Digest</h1>
        <p style="color:rgba(255,255,255,0.7);margin:0;font-size:13px;">${today} &bull; by ${founderName}</p>
      </td></tr>
      <tr><td style="background:#0f0f1a;padding:28px 24px;color:#e0e0e0;">
        ${storyCards}
        ${travelSection}
        ${linkedinSection}
      </td></tr>
      <tr><td style="background:#0a0a0a;padding:20px 24px;text-align:center;">
        <p style="color:#666;font-size:12px;margin:0;">SkynetJoe &bull; AI Automation Agency &bull; <a href="${websiteUrl}" style="color:${brandColor};">${websiteUrl.replace('https://','')}</a></p>
      </td></tr>
    </table>
    </body></html>`;

    return [{ json: { html, subject: digest.digestSubject || 'SkynetJoe Daily AI + Travel Digest', recipientEmail: config.recipientEmail, senderEmail: config.senderEmail } }];
    """)
    n_build_email = code_node("Build Digest Email", [2140, 300], build_email_code)
    nodes.append(n_build_email)

    # --- 10. Send Digest Email ---
    n_send = email_send("Send Digest Email", [2380, 300],
                        "={{ $json.recipientEmail }}",
                        "={{ $json.senderEmail }}",
                        "={{ $json.subject }}",
                        "={{ $json.html }}")
    nodes.append(n_send)

    # --- 11. Save Daily History ---
    save_code = textwrap.dedent("""\
    // Save digest history for deduplication
    const staticData = $getWorkflowStaticData('global');
    if (!staticData.digestHistory) staticData.digestHistory = [];

    const digest = $('Parse Digest').first().json;
    const entry = {
      date: new Date().toISOString().split('T')[0],
      storyUrls: (digest.topStories || []).map(s => s.url),
      travelCategory: digest.travelHack?.category || '',
    };
    staticData.digestHistory.push(entry);

    // Keep last 30 days
    if (staticData.digestHistory.length > 30) {
      staticData.digestHistory = staticData.digestHistory.slice(-30);
    }

    return [{ json: { status: 'Daily history saved', entries: staticData.digestHistory.length } }];
    """)
    n_save = code_node("Save Daily History", [2620, 300], save_code)
    nodes.append(n_save)

    # --- Connections ---
    # Linear: Schedule -> Config -> RSS -> Split -> Fetch -> (loop back to Split)
    # Split (done) -> Merge -> GPT -> Parse -> Build Email -> Send -> Save
    connections = {
        "Schedule - Daily 7AM": {"main": [[{"node": "SkynetJoe Config", "type": "main", "index": 0}]]},
        "SkynetJoe Config": {"main": [[{"node": "RSS Feed URLs", "type": "main", "index": 0}]]},
        "RSS Feed URLs": {"main": [[{"node": "Split Feeds", "type": "main", "index": 0}]]},
        "Split Feeds": {"main": [
            [{"node": "Fetch Feed", "type": "main", "index": 0}],   # batch output
            [{"node": "Merge Feed Data", "type": "main", "index": 0}],  # done output
        ]},
        "Fetch Feed": {"main": [[{"node": "Split Feeds", "type": "main", "index": 0}]]},
        "Merge Feed Data": {"main": [[{"node": "GPT Curate Daily Digest", "type": "main", "index": 0}]]},
        "GPT Curate Daily Digest": {"main": [[{"node": "Parse Digest", "type": "main", "index": 0}]]},
        "Parse Digest": {"main": [[{"node": "Build Digest Email", "type": "main", "index": 0}]]},
        "Build Digest Email": {"main": [[{"node": "Send Digest Email", "type": "main", "index": 0}]]},
        "Send Digest Email": {"main": [[{"node": "Save Daily History", "type": "main", "index": 0}]]},
    }

    return build_workflow("SkynetJoe Daily AI + Travel Digest v2.0", nodes, connections)


# ############################################################################
#                        WORKFLOW 2  —  WEEKLY AEO ENGINE
# ############################################################################

# --- Reusable code fragments ---

LOAD_STATE_TEMPLATE = """\
// Load pipeline state from workflow static data
const staticData = $getWorkflowStaticData('global');
const pipeline = staticData.pipeline || {{}};
const required = {required_keys};
const missing = required.filter(k => !pipeline[k]);
if (missing.length > 0) {{
  throw new Error('Pipeline state missing: ' + missing.join(', ') + '. Run earlier agent(s) first.');
}}
return [{{ json: pipeline }}];
"""

SAVE_STATE_TEMPLATE = """\
// Save pipeline state for downstream agents
const staticData = $getWorkflowStaticData('global');
if (!staticData.pipeline) staticData.pipeline = {{}};
{assignments}
staticData.pipeline.__lastUpdated = new Date().toISOString();
staticData.pipeline.__lastStage = '{stage}';
return [{{ json: {{ status: '{stage} agent complete' }} }}];
"""

def make_load_state(name, pos, required_keys):
    code = LOAD_STATE_TEMPLATE.format(required_keys=json.dumps(required_keys))
    return code_node(name, pos, code)

def make_save_state(name, pos, stage, assignment_lines):
    code = SAVE_STATE_TEMPLATE.format(
        assignments="\n".join(assignment_lines),
        stage=stage,
    )
    return code_node(name, pos, code)


def build_weekly_aeo():
    """Build the Weekly AEO Engine workflow (~50 nodes, 5-agent split)."""
    nodes = []
    connections = {}

    # Layout constants
    Y_MON = 300
    Y_TUE = 900
    Y_WED = 1500
    Y_THU = 2100
    Y_FRI = 2700
    Y_UTIL = 3300
    X_START = 220
    X_STEP = 260

    def x(col):
        return X_START + col * X_STEP

    # ======================================================================
    #  MONDAY AGENT  — Keyword Strategy
    # ======================================================================

    # M1. Schedule Monday 9 AM WITA (= 1 AM UTC)
    m1 = schedule_trigger("Schedule - Monday 9AM", [x(0), Y_MON], "0 1 * * 1")
    nodes.append(m1)

    # M2. Client Configuration
    all_config = {**SKYNETJOE_CONFIG, **WEEKLY_EXTRA_CONFIG}
    m2 = set_node("Client Configuration", [x(1), Y_MON], string_values=all_config)
    nodes.append(m2)

    # M3. Prepare Keywords
    prepare_kw_code = textwrap.dedent("""\
    const staticData = $getWorkflowStaticData('global');
    if (!staticData.contentHistory) staticData.contentHistory = [];
    const history = staticData.contentHistory;

    const config = $input.first().json;
    const allKeywords = config.keywords.split(', ');
    const travelKw = config.travelKeywords.split(', ');
    const combinedKeywords = [...allKeywords, ...travelKw];

    const usedKeywords = history.slice(-8).map(h => h.primaryKeyword);
    const usedTitles = history.slice(-4).map(h => h.articleTitle);
    const usedAngles = history.slice(-4).map(h => h.articleAngle);

    const available = combinedKeywords.filter(k => !usedKeywords.includes(k));
    const pool = available.length > 0 ? available : combinedKeywords;
    const primaryKeyword = pool[Math.floor(Math.random() * pool.length)];

    const isTravelTopic = travelKw.includes(primaryKeyword);

    const variants = ['trends 2026', 'for SMB', 'cost', 'vs alternatives', 'best practices', 'ROI', 'case study', 'how-to'];
    const variant = variants[history.length % variants.length];
    const expandedKeyword = `${primaryKeyword} ${variant}`;

    const prefixes = ['what is', 'how to', 'why', 'best', 'top', 'how much does', 'is it worth'];
    const prefix = prefixes[history.length % prefixes.length];
    const questionQuery = `${prefix} ${primaryKeyword}`;

    const structures = ['deep-dive', 'problem-solution', 'case-study'];
    const usedStructures = history.slice(-3).map(h => h.articleStructure);
    let articleStructure = structures.find(s => !usedStructures.includes(s)) || structures[0];

    return [{
      json: {
        primaryKeyword,
        expandedKeyword,
        questionQuery,
        articleStructure,
        isTravelTopic,
        keywordList: pool.slice(0, 10),
        usedTitles,
        usedAngles,
        runNumber: history.length + 1
      }
    }];
    """)
    m3 = code_node("Prepare Keywords", [x(2), Y_MON], prepare_kw_code)
    nodes.append(m3)

    # M4. Autocomplete Keywords
    m4 = http_get("Autocomplete Keywords", [x(3), Y_MON - 120],
                  "https://suggestqueries.google.com/complete/search",
                  query_params={"client": "firefox", "q": "={{ $json.expandedKeyword }}"})
    nodes.append(m4)

    # M5. Autocomplete Questions
    m5 = http_get("Autocomplete Questions", [x(3), Y_MON],
                  "https://suggestqueries.google.com/complete/search",
                  query_params={"client": "firefox", "q": "={{ $json.questionQuery }}"})
    nodes.append(m5)

    # M6. Serper SERP Search
    m6 = http_post_raw_body("Serper SERP Search", [x(3), Y_MON + 120],
                            "https://google.serper.dev/search",
                            body_params={"q": "={{ $('Prepare Keywords').first().json.primaryKeyword }}", "num": "10"},
                            auth_type="predefined", node_cred_type="serperApi",
                            creds={"serperApi": {"id": "REPLACE_WITH_YOUR_SERPER_CREDENTIAL_ID", "name": "Serper API"}})
    nodes.append(m6)

    # M7. Merge Keyword Data
    merge_kw_code = textwrap.dedent("""\
    // Merge autocomplete + Serper results
    const items = $input.all();

    let autoKeywords = [], autoQuestions = [];
    try {
      const kwRaw = items[0]?.json;
      if (kwRaw?.data) {
        const parsed = typeof kwRaw.data === 'string' ? JSON.parse(kwRaw.data) : kwRaw.data;
        autoKeywords = Array.isArray(parsed) && parsed[1] ? parsed[1] : [];
      }
    } catch(e) {}
    try {
      const qRaw = items[1]?.json;
      if (qRaw?.data) {
        const parsed = typeof qRaw.data === 'string' ? JSON.parse(qRaw.data) : qRaw.data;
        autoQuestions = Array.isArray(parsed) && parsed[1] ? parsed[1] : [];
      }
    } catch(e) {}

    let serp = {};
    try { serp = items[2]?.json || {}; } catch(e) {}

    const paa = (serp.peopleAlsoAsk || []).map(p => p.question);
    const relatedSearches = (serp.relatedSearches || []).map(r => r.query);
    const organicTitles = (serp.organic || []).slice(0, 5).map(o => `${o.title} - ${o.link}`);
    const featuredSnippet = serp.answerBox ? `${serp.answerBox.title}: ${serp.answerBox.snippet}` : 'None';

    const prep = $('Prepare Keywords').first().json;

    return [{
      json: {
        primaryKeyword: prep.primaryKeyword,
        questionQuery: prep.questionQuery,
        articleStructure: prep.articleStructure,
        isTravelTopic: prep.isTravelTopic,
        autocompleteSuggestions: (Array.isArray(autoKeywords) ? autoKeywords : []).join('\\n'),
        questionSuggestions: (Array.isArray(autoQuestions) ? autoQuestions : []).join('\\n'),
        paaQuestions: paa.join('\\n'),
        relatedSearches: relatedSearches.join('\\n'),
        organicTitles: organicTitles.join('\\n'),
        featuredSnippets: featuredSnippet,
        usedTitles: (prep.usedTitles || []).join('\\n'),
        usedAngles: (prep.usedAngles || []).join('\\n'),
      }
    }];
    """)
    m7 = code_node("Merge Keyword Data", [x(4), Y_MON], merge_kw_code)
    nodes.append(m7)

    # M8. GPT Keyword Strategy
    m8_sys = (
        "=You are an SEO/AEO strategist for SkynetJoe, an AI automation agency. "
        "The founder Waseem Nasir is currently traveling ASEAN (Bali). "
        "Content should position him as a practitioner-founder, not an influencer."
    )
    m8_user = textwrap.dedent("""\
    =Primary keyword: {{ $json.primaryKeyword }}
    Question query: {{ $json.questionQuery }}
    Article structure: {{ $json.articleStructure }}
    Is travel topic: {{ $json.isTravelTopic }}

    Autocomplete suggestions: {{ $json.autocompleteSuggestions }}
    Question suggestions: {{ $json.questionSuggestions }}
    People Also Ask: {{ $json.paaQuestions }}
    Related searches: {{ $json.relatedSearches }}
    Top organic titles: {{ $json.organicTitles }}
    Featured snippets: {{ $json.featuredSnippets }}

    Previously used titles (avoid): {{ $json.usedTitles }}

    SkynetJoe services: AI Employee setup, n8n automation, chatbot development, web development, social media automation, content engines, workflow consulting

    Generate a content strategy as JSON:
    {
      "primaryKeyword": "",
      "secondaryKeywords": ["", "", ""],
      "longTailKeywords": ["", ""],
      "targetQuestions": ["", "", ""],
      "seoTitle": "(under 65 chars, include 2026)",
      "articleAngle": "(unique perspective)",
      "contentBrief": "(2-3 sentences)",
      "travelAngle": "(how to weave in nomad/travel perspective)",
      "aeoStrategy": {
        "directAnswer": "(2-sentence answer AI engines should extract)",
        "schemaTypes": ["Article", "FAQPage"],
        "comparisonOpportunity": ""
      },
      "competitorInsights": "",
      "linkedinAngle": "",
      "brandCollabOpportunity": "(which brands could be mentioned/tagged)"
    }
    """)
    m8 = openai_node("GPT Keyword Strategy", [x(5), Y_MON], m8_sys, m8_user,
                     temp=0.6, max_tokens=2048)
    nodes.append(m8)

    # M9. Parse Strategy
    parse_strat_code = textwrap.dedent("""\
    // Parse GPT strategy response
    const items = $input.all();
    function extractText(r) {
      if (!r) return '';
      if (typeof r === 'string') return r;
      if (r.text) return r.text;
      if (r.message?.content) return r.message.content;
      if (r.output) return typeof r.output === 'string' ? r.output : JSON.stringify(r.output);
      return JSON.stringify(r);
    }
    const raw = extractText(items[0]?.json);
    let strategy;
    try {
      const cleaned = raw.replace(/```json\\n?/g, '').replace(/```\\n?/g, '').trim();
      strategy = JSON.parse(cleaned);
    } catch(e) {
      const jsonMatch = raw.match(/\\{[\\s\\S]*\\}/);
      if (jsonMatch) {
        try { strategy = JSON.parse(jsonMatch[0]); } catch(e2) {
          strategy = {
            primaryKeyword: 'AI automation', seoTitle: 'AI Automation Guide 2026',
            articleAngle: 'practitioner guide', contentBrief: 'Guide to AI automation',
            travelAngle: 'Written from Bali', targetQuestions: ['What is AI automation?'],
            secondaryKeywords: [], longTailKeywords: [],
            aeoStrategy: { directAnswer: '', schemaTypes: ['Article'], comparisonOpportunity: '' },
            competitorInsights: '', linkedinAngle: '', brandCollabOpportunity: ''
          };
        }
      }
    }
    return [{ json: strategy }];
    """)
    m9 = code_node("Parse Strategy", [x(6), Y_MON], parse_strat_code)
    nodes.append(m9)

    # M10. Save State Monday
    m10 = code_node("Save State - Monday", [x(7), Y_MON], textwrap.dedent("""\
    const staticData = $getWorkflowStaticData('global');
    if (!staticData.pipeline) staticData.pipeline = {};
    staticData.pipeline.clientConfig = $('Client Configuration').first().json;
    staticData.pipeline.prepKeywords = $('Prepare Keywords').first().json;
    staticData.pipeline.keywordData = $('Merge Keyword Data').first().json;
    staticData.pipeline.strategy = $('Parse Strategy').first().json;
    staticData.pipeline.__lastUpdated = new Date().toISOString();
    staticData.pipeline.__lastStage = 'monday';
    const s = staticData.pipeline.strategy;
    return [{ json: { status: 'Monday agent complete', keyword: staticData.pipeline.prepKeywords.primaryKeyword, title: s.seoTitle } }];
    """))
    nodes.append(m10)

    # Monday connections
    connections.update({
        "Schedule - Monday 9AM": {"main": [[{"node": "Client Configuration", "type": "main", "index": 0}]]},
        "Client Configuration": {"main": [[{"node": "Prepare Keywords", "type": "main", "index": 0}]]},
        "Prepare Keywords": {"main": [[
            {"node": "Autocomplete Keywords", "type": "main", "index": 0},
            {"node": "Autocomplete Questions", "type": "main", "index": 0},
            {"node": "Serper SERP Search", "type": "main", "index": 0},
        ]]},
        "Autocomplete Keywords": {"main": [[{"node": "Merge Keyword Data", "type": "main", "index": 0}]]},
        "Autocomplete Questions": {"main": [[{"node": "Merge Keyword Data", "type": "main", "index": 0}]]},
        "Serper SERP Search": {"main": [[{"node": "Merge Keyword Data", "type": "main", "index": 0}]]},
        "Merge Keyword Data": {"main": [[{"node": "GPT Keyword Strategy", "type": "main", "index": 0}]]},
        "GPT Keyword Strategy": {"main": [[{"node": "Parse Strategy", "type": "main", "index": 0}]]},
        "Parse Strategy": {"main": [[{"node": "Save State - Monday", "type": "main", "index": 0}]]},
    })

    # ======================================================================
    #  TUESDAY AGENT  — Deep Research
    # ======================================================================

    t1 = schedule_trigger("Schedule - Tuesday 9AM", [x(0), Y_TUE], "0 1 * * 2")
    nodes.append(t1)

    t2 = make_load_state("Load State - Tuesday", [x(1), Y_TUE], ["strategy", "prepKeywords", "clientConfig"])
    nodes.append(t2)

    # T3. RSS Sources
    rss_sources_code = textwrap.dedent(f"""\
    // Output 20 RSS feed objects for the loop
    const feeds = {RSS_FEEDS_JSON};
    return feeds.map(f => ({{ json: f }}));
    """)
    t3 = code_node("RSS Sources", [x(2), Y_TUE], rss_sources_code)
    nodes.append(t3)

    # T4. Split RSS Batches
    t4 = split_in_batches("Split RSS Batches", [x(3), Y_TUE], batch_size=5)
    nodes.append(t4)

    # T5. Fetch RSS Feed
    t5 = http_get("Fetch RSS Feed", [x(4), Y_TUE], "={{ $json.url }}")
    nodes.append(t5)

    # T7. Convert to Research Input
    convert_code = textwrap.dedent("""\
    // Extract stories from all fetched RSS feeds, filter to last 7 days
    const items = $input.all();
    const stories = [];
    const now = Date.now();
    const WEEK_MS = 7 * 24 * 60 * 60 * 1000;

    // Dedup against content history
    const staticData = $getWorkflowStaticData('global');
    const history = staticData.contentHistory || [];
    const usedUrls = new Set(history.slice(-4).flatMap(h => h.storyUrls || []));

    for (const item of items) {
      const feedName = item.json.name || 'Unknown';
      const feedCategory = item.json.category || 'AI';
      const raw = item.json.data || item.json.body || '';
      if (!raw || typeof raw !== 'string' || raw.length < 50) continue;

      const itemRegex = /<item[\\s>][\\s\\S]*?<\\/item>|<entry[\\s>][\\s\\S]*?<\\/entry>/gi;
      const matches = raw.match(itemRegex) || [];
      for (const m of matches) {
        const title = (m.match(/<title[^>]*>(?:<!\\[CDATA\\[)?(.*?)(?:\\]\\]>)?<\\/title>/s) || [])[1] || '';
        const link = (m.match(/<link[^>]*href="([^"]*)"/) || m.match(/<link[^>]*>(.*?)<\\/link>/) || [])[1] || '';
        const desc = (m.match(/<description[^>]*>(?:<!\\[CDATA\\[)?(.*?)(?:\\]\\]>)?<\\/description>/s) ||
                      m.match(/<summary[^>]*>(?:<!\\[CDATA\\[)?(.*?)(?:\\]\\]>)?<\\/summary>/s) || [])[1] || '';
        const pubDate = (m.match(/<pubDate[^>]*>(.*?)<\\/pubDate>/) ||
                         m.match(/<published[^>]*>(.*?)<\\/published>/) || [])[1] || '';
        const ts = pubDate ? new Date(pubDate).getTime() : 0;
        if (ts && (now - ts) > WEEK_MS) continue;
        if (link && usedUrls.has(link)) continue;
        const cleanDesc = desc.replace(/<[^>]*>/g, '').substring(0, 200);
        stories.push({ title: title.trim(), link: link.trim(), description: cleanDesc.trim(), pubDate, source: feedName, category: feedCategory });
      }
    }

    // Deduplicate
    const seen = new Set();
    const unique = stories.filter(s => {
      if (!s.link || seen.has(s.link)) return false;
      seen.add(s.link);
      return true;
    });
    unique.sort((a, b) => new Date(b.pubDate) - new Date(a.pubDate));
    const top50 = unique.slice(0, 50);

    // Format as CSV text for Gemini
    let csv = 'rank,title,source,category,url,description\\n';
    top50.forEach((s, i) => {
      csv += `${i+1},"${s.title.replace(/"/g, '""')}","${s.source}","${s.category}","${s.link}","${s.description.replace(/"/g, '""')}"\\n`;
    });

    return [{ json: { csvData: csv, storyCount: top50.length, stories: top50 } }];
    """)
    t7 = code_node("Convert to Research Input", [x(5), Y_TUE], convert_code)
    nodes.append(t7)

    # T8. Gemini Deep Research
    gemini_prompt = textwrap.dedent("""\
    You are a research analyst for SkynetJoe (AI automation agency). Analyze these RSS stories and rank them by relevance.

    Primary keyword this week: {{primaryKeyword}}
    Travel angle: {{travelAngle}}

    Stories (CSV):
    {{csvData}}

    Return ONLY valid JSON:
    {
      "rankedStories": [
        {"rank": 1, "title": "", "url": "", "source": "", "summary": "", "relevanceScore": 85, "keywordAlignment": "", "aeoAngle": "", "category": "AI|Travel|Business"}
      ],
      "topStory": {"title": "", "url": "", "whyTop": ""},
      "travelStories": [],
      "trendInsight": "one-paragraph trend analysis",
      "newsletterStories": []
    }
    """)
    # Build the Gemini body as an n8n expression
    gemini_body_expr = textwrap.dedent("""\
    ={
      "contents": [{
        "parts": [{
          "text": "You are a research analyst for SkynetJoe (AI automation agency). Analyze these RSS stories and rank them by relevance.\\n\\nPrimary keyword this week: " + $('Load State - Tuesday').first().json.strategy.primaryKeyword + "\\nTravel angle: " + ($('Load State - Tuesday').first().json.strategy.travelAngle || 'digital nomad perspective') + "\\n\\nStories (CSV):\\n" + $json.csvData + "\\n\\nReturn ONLY valid JSON:\\n{\\n  \\"rankedStories\\": [{\\n    \\"rank\\": 1, \\"title\\": \\"\\", \\"url\\": \\"\\", \\"source\\": \\"\\", \\"summary\\": \\"\\", \\"relevanceScore\\": 85, \\"keywordAlignment\\": \\"\\", \\"aeoAngle\\": \\"\\", \\"category\\": \\"AI|Travel|Business\\"\\n  }],\\n  \\"topStory\\": {\\"title\\": \\"\\", \\"url\\": \\"\\", \\"whyTop\\": \\"\\"},\\n  \\"travelStories\\": [],\\n  \\"trendInsight\\": \\"one-paragraph trend analysis\\",\\n  \\"newsletterStories\\": []\\n}"
        }]
      }],
      "generationConfig": {
        "temperature": 0.5,
        "maxOutputTokens": 4096
      }
    }
    """).strip()

    t8 = {
        "parameters": {
            "url": "https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-flash:generateContent?key=REPLACE_WITH_GEMINI_API_KEY",
            "method": "POST",
            "sendBody": True,
            "specifyBody": "json",
            "jsonBody": gemini_body_expr,
            "options": {"response": {"response": {"neverError": True}}},
        },
        "id": uid(),
        "name": "Gemini Deep Research",
        "type": "n8n-nodes-base.httpRequest",
        "typeVersion": 4.2,
        "position": [x(6), Y_TUE],
    }
    nodes.append(t8)

    # T9. Parse Research
    parse_research_code = textwrap.dedent("""\
    // Parse Gemini response
    const items = $input.all();
    const raw = items[0]?.json;
    let text = '';
    try {
      text = raw?.candidates?.[0]?.content?.parts?.[0]?.text || JSON.stringify(raw);
    } catch(e) { text = JSON.stringify(raw); }

    let research;
    try {
      const cleaned = text.replace(/```json\\n?/g, '').replace(/```\\n?/g, '').trim();
      research = JSON.parse(cleaned);
    } catch(e) {
      const jsonMatch = text.match(/\\{[\\s\\S]*\\}/);
      try { research = JSON.parse(jsonMatch[0]); } catch(e2) {
        research = { rankedStories: [], topStory: { title: 'N/A', url: '', whyTop: '' }, travelStories: [], trendInsight: '', newsletterStories: [] };
      }
    }
    return [{ json: research }];
    """)
    t9 = code_node("Parse Research", [x(7), Y_TUE], parse_research_code)
    nodes.append(t9)

    # T10. Save State Tuesday
    t10 = code_node("Save State - Tuesday", [x(8), Y_TUE], textwrap.dedent("""\
    const staticData = $getWorkflowStaticData('global');
    const research = $('Parse Research').first().json;
    staticData.pipeline.research = research;
    staticData.pipeline.__lastUpdated = new Date().toISOString();
    staticData.pipeline.__lastStage = 'tuesday';
    return [{ json: { status: 'Tuesday agent complete', topStory: research.topStory?.title, storyCount: research.rankedStories?.length } }];
    """))
    nodes.append(t10)

    # Tuesday connections
    connections.update({
        "Schedule - Tuesday 9AM": {"main": [[{"node": "Load State - Tuesday", "type": "main", "index": 0}]]},
        "Load State - Tuesday": {"main": [[{"node": "RSS Sources", "type": "main", "index": 0}]]},
        "RSS Sources": {"main": [[{"node": "Split RSS Batches", "type": "main", "index": 0}]]},
        "Split RSS Batches": {"main": [
            [{"node": "Fetch RSS Feed", "type": "main", "index": 0}],
            [{"node": "Convert to Research Input", "type": "main", "index": 0}],
        ]},
        "Fetch RSS Feed": {"main": [[{"node": "Split RSS Batches", "type": "main", "index": 0}]]},
        "Convert to Research Input": {"main": [[{"node": "Gemini Deep Research", "type": "main", "index": 0}]]},
        "Gemini Deep Research": {"main": [[{"node": "Parse Research", "type": "main", "index": 0}]]},
        "Parse Research": {"main": [[{"node": "Save State - Tuesday", "type": "main", "index": 0}]]},
    })

    # ======================================================================
    #  WEDNESDAY AGENT  — Article Writer
    # ======================================================================

    w1 = schedule_trigger("Schedule - Wednesday 9AM", [x(0), Y_WED], "0 1 * * 3")
    nodes.append(w1)

    w2 = make_load_state("Load State - Wednesday", [x(1), Y_WED], ["strategy", "prepKeywords", "clientConfig", "research"])
    nodes.append(w2)

    # W3. GPT Write Article
    w3_sys = (
        "=You are a senior content writer for SkynetJoe. Write AEO-optimized articles "
        "that position Waseem Nasir as a practitioner-founder who builds AI automation "
        "while traveling the world."
    )
    w3_user = textwrap.dedent("""\
    =Write an AEO-optimized article based on this strategy:

    Title: {{ $('Load State - Wednesday').first().json.strategy.seoTitle }}
    Primary keyword: {{ $('Load State - Wednesday').first().json.strategy.primaryKeyword }}
    Secondary keywords: {{ JSON.stringify($('Load State - Wednesday').first().json.strategy.secondaryKeywords) }}
    Article structure: {{ $('Load State - Wednesday').first().json.prepKeywords.articleStructure }}
    Content brief: {{ $('Load State - Wednesday').first().json.strategy.contentBrief }}
    Travel angle: {{ $('Load State - Wednesday').first().json.strategy.travelAngle }}
    Target questions: {{ JSON.stringify($('Load State - Wednesday').first().json.strategy.targetQuestions) }}
    AEO direct answer: {{ $('Load State - Wednesday').first().json.strategy.aeoStrategy.directAnswer }}
    Top research story: {{ JSON.stringify($('Load State - Wednesday').first().json.research.topStory) }}
    Trend insight: {{ $('Load State - Wednesday').first().json.research.trendInsight }}

    RULES:
    - 800-1200 words
    - Every H2/H3 is a real question people search
    - Open every section with 1-2 sentence direct answer (for AI extraction)
    - At least 1 stat per section (real, sourced)
    - Include comparison table where relevant
    - Bulleted lists for key points
    - FAQ section: 3-5 Q&A from PAA data
    - Author: Waseem Nasir, Founder of SkynetJoe
    - Include 1-2 internal links to skynetjoe.com service pages
    - If travel topic: weave in Bali/ASEAN angle naturally
    - If AI topic: include "Nomad CEO perspective" sidebar or paragraph
    - NO buzzwords: leverage, synergy, cutting-edge, game-changing, revolutionize, robust, comprehensive, innovative, transformative
    - NO dates before 2026

    Output format:
    HTML_CONTENT_HERE
    |||META|||
    {"title": "", "slug": "", "excerpt": "", "wordCount": 0, "primaryKeyword": "", "aeoScore": 0, "schemaTypes": [], "travelRelevance": "high|medium|low"}
    """)
    w3 = openai_node("GPT Write Article", [x(2), Y_WED], w3_sys, w3_user,
                     temp=0.7, max_tokens=4096)
    nodes.append(w3)

    # W4. Extract Article
    extract_code = textwrap.dedent("""\
    // Extract article HTML and metadata from GPT response
    const items = $input.all();
    function extractText(r) {
      if (!r) return '';
      if (typeof r === 'string') return r;
      if (r.text) return r.text;
      if (r.message?.content) return r.message.content;
      if (r.output) return typeof r.output === 'string' ? r.output : JSON.stringify(r.output);
      return JSON.stringify(r);
    }
    const raw = extractText(items[0]?.json);
    const parts = raw.split('|||META|||');
    let articleHtml = (parts[0] || '').replace(/```html\\n?/g, '').replace(/```\\n?/g, '').trim();
    let metadata = {};
    try {
      const metaRaw = (parts[1] || '').replace(/```json\\n?/g, '').replace(/```\\n?/g, '').trim();
      const jsonMatch = metaRaw.match(/\\{[\\s\\S]*\\}/);
      if (jsonMatch) metadata = JSON.parse(jsonMatch[0]);
    } catch(e) {
      metadata = { title: 'AEO Article', slug: 'article-' + Date.now(), excerpt: '', wordCount: articleHtml.split(/\\s+/).length, primaryKeyword: '', aeoScore: 0, schemaTypes: ['Article'] };
    }
    return [{ json: { articleHtml, metadata } }];
    """)
    w4 = code_node("Extract Article", [x(3), Y_WED], extract_code)
    nodes.append(w4)

    # W5. GPT AEO Editor
    w5_sys = "=You are an AEO Editor. Score and optimize articles for Answer Engine Optimization."
    w5_user = textwrap.dedent("""\
    =Score the following article on 5 criteria (0-20 each, 100 total):
    1. Direct Answer quality (AI extractability)
    2. Data Richness (real numbers, stats, dates)
    3. Question Headings (match AI search surfaces)
    4. Keyword Integration (natural, not stuffed)
    5. FAQ Quality (specific, quotable answers)

    Make surgical edits. Remove buzzwords. Fix vague headings. Ensure first paragraph is AI-extractable.

    ARTICLE HTML:
    {{ $json.articleHtml }}

    Return the optimized HTML followed by |||META||| and JSON:
    {"aeoScore": 85, "scores": {"directAnswers": 18, "dataRichness": 17, "questionHeadings": 16, "keywordIntegration": 17, "faqQuality": 17}, "optimizations": ["list of changes made"]}
    """)
    w5 = openai_node("GPT AEO Editor", [x(4), Y_WED], w5_sys, w5_user,
                     temp=0.5, max_tokens=4096)
    nodes.append(w5)

    # W6. Finalize Article
    finalize_code = textwrap.dedent("""\
    // Finalize article with quality checks
    const items = $input.all();
    function extractText(r) {
      if (!r) return '';
      if (typeof r === 'string') return r;
      if (r.text) return r.text;
      if (r.message?.content) return r.message.content;
      if (r.output) return typeof r.output === 'string' ? r.output : JSON.stringify(r.output);
      return JSON.stringify(r);
    }
    const raw = extractText(items[0]?.json);
    const parts = raw.split('|||META|||');
    let articleHtml = (parts[0] || '').replace(/```html\\n?/g, '').replace(/```\\n?/g, '').trim();
    let editorMeta = {};
    try {
      const metaRaw = (parts[1] || '').replace(/```json\\n?/g, '').replace(/```\\n?/g, '').trim();
      const jsonMatch = metaRaw.match(/\\{[\\s\\S]*\\}/);
      if (jsonMatch) editorMeta = JSON.parse(jsonMatch[0]);
    } catch(e) { editorMeta = { aeoScore: 70, scores: {}, optimizations: [] }; }

    // Quality checks
    const buzzwords = ['leverage', 'synergy', 'cutting-edge', 'game-changer', 'revolutionize', 'disrupt', 'paradigm', 'holistic', 'robust solution', 'comprehensive', 'innovative', 'transformative'];
    const foundBuzzwords = buzzwords.filter(b => articleHtml.toLowerCase().includes(b));
    const oldDates = articleHtml.match(/\\b(2023|2024|2025)\\b/g) || [];

    const pipeline = $getWorkflowStaticData('global').pipeline || {};
    const config = pipeline.clientConfig || {};
    const origMeta = $('Extract Article').first().json.metadata || {};
    const slug = origMeta.slug || editorMeta.slug || 'article-' + Date.now();
    const articleUrl = (config.articleBaseUrl || 'https://www.skynetjoe.com/blog/') + slug;

    return [{
      json: {
        articleHtml, articleUrl, slug,
        aeoScore: editorMeta.aeoScore || 70,
        scores: editorMeta.scores || {},
        optimizations: editorMeta.optimizations || [],
        qualityWarnings: { buzzwordsFound: foundBuzzwords, oldDatesFound: oldDates },
        metadata: { ...origMeta, ...editorMeta, slug, articleUrl },
      }
    }];
    """)
    w6 = code_node("Finalize Article", [x(5), Y_WED], finalize_code)
    nodes.append(w6)

    # W7. GPT LinkedIn Post
    w7_sys = (
        "=You are Waseem Nasir, founder of SkynetJoe (www.skynetjoe.com), "
        "an AI automation agency. Currently in Bali, running the agency remotely."
    )
    w7_user = textwrap.dedent("""\
    =Write a LinkedIn post based on this article.

    Article title: {{ $json.metadata.title }}
    Key insight: {{ $json.metadata.excerpt }}
    Travel context: Currently in Bali, running SkynetJoe remotely.

    RULES:
    - 150-250 words
    - Bold opening claim or stat
    - 1-2 specific facts
    - Reference specific tool/company/tech
    - Weave in travel angle: "I'm writing this from [Bali cafe/coworking/villa]..." -- subtle, not braggy
    - End with question or actionable takeaway
    - No emojis, no corporate buzzwords
    - Line breaks for LinkedIn formatting
    - 3-5 hashtags at end
    - If relevant, tag a brand (Notion, n8n, OpenAI, etc.)

    Return ONLY the post text.
    """)
    w7 = openai_node("GPT LinkedIn Post", [x(6), Y_WED], w7_sys, w7_user,
                     temp=0.7, max_tokens=1024)
    nodes.append(w7)

    # W8. Save State Wednesday
    w8 = code_node("Save State - Wednesday", [x(7), Y_WED], textwrap.dedent("""\
    const staticData = $getWorkflowStaticData('global');
    function extractText(r) {
      if (!r) return '';
      if (typeof r === 'string') return r;
      if (r.text) return r.text;
      if (r.message?.content) return r.message.content;
      if (r.output) return typeof r.output === 'string' ? r.output : JSON.stringify(r.output);
      return JSON.stringify(r);
    }
    staticData.pipeline.article = $('Finalize Article').first().json;
    staticData.pipeline.linkedinPost = extractText($('GPT LinkedIn Post').first().json).replace(/```/g, '');
    staticData.pipeline.__lastUpdated = new Date().toISOString();
    staticData.pipeline.__lastStage = 'wednesday';
    return [{ json: { status: 'Wednesday agent complete', title: staticData.pipeline.article?.metadata?.title } }];
    """))
    nodes.append(w8)

    # W9. Build Email - Article
    build_art_email_code = textwrap.dedent("""\
    // Build branded email with article preview + LinkedIn post
    const pipeline = $getWorkflowStaticData('global').pipeline || {};
    const config = pipeline.clientConfig || {};
    const article = pipeline.article || {};
    const linkedinPost = pipeline.linkedinPost || '';
    const meta = article.metadata || {};
    const brandColor = config.brandColor || '#13b973';
    const secondaryColor = config.secondaryColor || '#8B5CF6';
    const websiteUrl = config.websiteUrl || 'https://www.skynetjoe.com';
    const date = new Date().toLocaleDateString('en-US', { weekday: 'long', year: 'numeric', month: 'long', day: 'numeric' });

    const html = `<!DOCTYPE html><html><head><meta charset="utf-8"><meta name="viewport" content="width=device-width"></head>
    <body style="margin:0;padding:0;background:#0a0a0a;font-family:-apple-system,BlinkMacSystemFont,'Segoe UI',Roboto,sans-serif;">
    <table width="100%" cellpadding="0" cellspacing="0" style="max-width:680px;margin:0 auto;">
      <tr><td style="background:linear-gradient(135deg,${secondaryColor},${brandColor});padding:32px 24px;text-align:center;">
        <h1 style="color:#fff;margin:0 0 4px;font-size:22px;">SkynetJoe AEO Article</h1>
        <p style="color:rgba(255,255,255,0.7);margin:0;font-size:13px;">${date}</p>
      </td></tr>
      <tr><td style="background:#111;padding:28px 24px;color:#e0e0e0;">
        <p style="font-size:11px;text-transform:uppercase;letter-spacing:2px;color:${brandColor};margin:0 0 12px;">THIS WEEK'S ARTICLE</p>
        <h2 style="color:#fff;margin:0 0 8px;font-size:20px;">${meta.title || 'AEO Article'}</h2>
        <p style="color:#aaa;margin:0 0 4px;font-size:13px;">AEO Score: ${article.aeoScore || 'N/A'}/100 | Keyword: ${meta.primaryKeyword || 'N/A'}</p>
        <p style="color:#aaa;margin:0 0 20px;font-size:13px;">URL: <a href="${article.articleUrl || '#'}" style="color:${brandColor};">${article.articleUrl || 'pending'}</a></p>
        <hr style="border-color:#333;">
        <div style="line-height:1.8;font-size:15px;color:#ddd;">${article.articleHtml || '<p>Article not available</p>'}</div>

        <div style="margin-top:28px;">
          <p style="font-size:11px;text-transform:uppercase;letter-spacing:2px;color:${secondaryColor};margin:0 0 12px;">LINKEDIN POST (COPY-READY)</p>
          <div style="background:#1a1a2e;border-radius:8px;padding:20px;border:1px solid #333;white-space:pre-wrap;font-family:monospace;color:#e0e0e0;font-size:13px;line-height:1.7;">${linkedinPost}</div>
        </div>
      </td></tr>
      <tr><td style="background:#0a0a0a;padding:20px 24px;text-align:center;">
        <p style="color:#666;font-size:12px;margin:0;">SkynetJoe AEO Engine v2.0 | <a href="${websiteUrl}" style="color:${brandColor};">${websiteUrl.replace('https://','')}</a></p>
      </td></tr>
    </table></body></html>`;

    return [{ json: {
      html, subject: 'SkynetJoe AEO Article: ' + (meta.title || 'This Week'),
      recipientEmail: config.recipientEmail || 'waseemhome8@gmail.com',
      senderEmail: config.senderEmail || 'waseem@skynetjoe.com'
    }}];
    """)
    w9 = code_node("Build Email - Article", [x(8), Y_WED], build_art_email_code)
    nodes.append(w9)

    # W10. Send Email - Article
    w10 = email_send("Send Email - Article", [x(9), Y_WED],
                     "={{ $json.recipientEmail }}",
                     "={{ $json.senderEmail }}",
                     "={{ $json.subject }}",
                     "={{ $json.html }}")
    nodes.append(w10)

    # Wednesday connections
    connections.update({
        "Schedule - Wednesday 9AM": {"main": [[{"node": "Load State - Wednesday", "type": "main", "index": 0}]]},
        "Load State - Wednesday": {"main": [[{"node": "GPT Write Article", "type": "main", "index": 0}]]},
        "GPT Write Article": {"main": [[{"node": "Extract Article", "type": "main", "index": 0}]]},
        "Extract Article": {"main": [[{"node": "GPT AEO Editor", "type": "main", "index": 0}]]},
        "GPT AEO Editor": {"main": [[{"node": "Finalize Article", "type": "main", "index": 0}]]},
        "Finalize Article": {"main": [[
            {"node": "GPT LinkedIn Post", "type": "main", "index": 0},
        ]]},
        "GPT LinkedIn Post": {"main": [[{"node": "Save State - Wednesday", "type": "main", "index": 0}]]},
        "Save State - Wednesday": {"main": [[{"node": "Build Email - Article", "type": "main", "index": 0}]]},
        "Build Email - Article": {"main": [[{"node": "Send Email - Article", "type": "main", "index": 0}]]},
    })

    # ======================================================================
    #  THURSDAY AGENT  — Newsletter + Nomad CEO Corner
    # ======================================================================

    th1 = schedule_trigger("Schedule - Thursday 9AM", [x(0), Y_THU], "0 1 * * 4")
    nodes.append(th1)

    th2 = make_load_state("Load State - Thursday", [x(1), Y_THU],
                          ["strategy", "clientConfig", "research", "article", "linkedinPost"])
    nodes.append(th2)

    # Th3. GPT Newsletter
    th3_sys = (
        "=You are the newsletter editor for SkynetJoe. Create engaging, dark-themed HTML newsletters. "
        "The founder Waseem Nasir is traveling ASEAN (Bali) while running his AI agency."
    )
    th3_user = textwrap.dedent("""\
    =Create a weekly newsletter for SkynetJoe's audience.

    This week's article: {{ $('Load State - Thursday').first().json.article.metadata.title }} ({{ $('Load State - Thursday').first().json.article.articleUrl }})
    Research stories: {{ JSON.stringify($('Load State - Thursday').first().json.research.newsletterStories || []) }}
    Travel stories: {{ JSON.stringify($('Load State - Thursday').first().json.research.travelStories || []) }}
    Trend insight: {{ $('Load State - Thursday').first().json.research.trendInsight }}

    Newsletter structure:
    1. **Editorial intro** (2-3 sentences on this week's AI trends)
    2. **Featured Article** (highlight this week's article with excerpt + link) -- use green #13b973
    3. **AI & Tech News** (4-6 stories, grouped by category)
    4. **Nomad CEO Corner** (NEW SECTION -- 2-3 stories about remote work, digital nomad life, ASEAN business. This is Waseem's personal section sharing insights from traveling.)
    5. **Business & Growth** (2-3 stories)
    6. **One Thing I Learned This Week** (personal reflection from Waseem -- 2-3 sentences about something he learned while working from Bali/ASEAN)

    Each story: bold linked title, 2-3 line summary, source attribution.
    Use inline CSS. Dark theme cards (#1a1a2e bg, #e0e0e0 text). Category badges (colored, uppercase).
    Featured article highlighted in #13b973 green.
    Real URLs from research data.
    Output clean HTML only, no markdown.
    """)
    th3 = openai_node("GPT Newsletter", [x(2), Y_THU], th3_sys, th3_user,
                      temp=0.7, max_tokens=3072)
    nodes.append(th3)

    # Th4. Clean Newsletter
    clean_nl_code = textwrap.dedent("""\
    // Clean newsletter HTML
    const items = $input.all();
    function extractText(r) {
      if (!r) return '';
      if (typeof r === 'string') return r;
      if (r.text) return r.text;
      if (r.message?.content) return r.message.content;
      if (r.output) return typeof r.output === 'string' ? r.output : JSON.stringify(r.output);
      return JSON.stringify(r);
    }
    let html = extractText(items[0]?.json);
    // Strip markdown code fences
    html = html.replace(/```html\\n?/g, '').replace(/```\\n?/g, '').trim();
    // Convert any remaining markdown bold to HTML
    html = html.replace(/\\*\\*(.*?)\\*\\*/g, '<strong>$1</strong>');
    return [{ json: { newsletterHtml: html } }];
    """)
    th4 = code_node("Clean Newsletter", [x(3), Y_THU], clean_nl_code)
    nodes.append(th4)

    # Th5. Save State Thursday
    th5 = code_node("Save State - Thursday", [x(4), Y_THU], textwrap.dedent("""\
    const staticData = $getWorkflowStaticData('global');
    staticData.pipeline.newsletter = $('Clean Newsletter').first().json;
    staticData.pipeline.__lastUpdated = new Date().toISOString();
    staticData.pipeline.__lastStage = 'thursday';
    return [{ json: { status: 'Thursday agent complete' } }];
    """))
    nodes.append(th5)

    # Th6. Build Email - Newsletter
    build_nl_email_code = textwrap.dedent("""\
    // Build branded newsletter email
    const pipeline = $getWorkflowStaticData('global').pipeline || {};
    const config = pipeline.clientConfig || {};
    const newsletter = pipeline.newsletter || {};
    const brandColor = config.brandColor || '#13b973';
    const secondaryColor = config.secondaryColor || '#8B5CF6';
    const websiteUrl = config.websiteUrl || 'https://www.skynetjoe.com';
    const date = new Date().toLocaleDateString('en-US', { weekday: 'long', year: 'numeric', month: 'long', day: 'numeric' });
    const dateShort = new Date().toLocaleDateString('en-US', { year: 'numeric', month: 'long', day: 'numeric' });

    const html = `<!DOCTYPE html><html><head><meta charset="utf-8"><meta name="viewport" content="width=device-width"></head>
    <body style="margin:0;padding:0;background:#0a0a0a;font-family:-apple-system,BlinkMacSystemFont,'Segoe UI',Roboto,sans-serif;">
    <table width="100%" cellpadding="0" cellspacing="0" style="max-width:680px;margin:0 auto;">
      <tr><td style="background:linear-gradient(135deg,${secondaryColor},${brandColor});padding:32px 24px;text-align:center;">
        <h1 style="color:#fff;margin:0 0 4px;font-size:22px;">SkynetJoe Weekly Digest</h1>
        <p style="color:rgba(255,255,255,0.7);margin:0;font-size:13px;">${date} | AI + Travel + Business</p>
      </td></tr>
      <tr><td style="background:#0f0f1a;padding:28px 24px;color:#e0e0e0;">
        ${newsletter.newsletterHtml || '<p>Newsletter content not available this week.</p>'}
      </td></tr>
      <tr><td style="background:#0a0a0a;padding:20px 24px;text-align:center;">
        <p style="color:#666;font-size:12px;margin:0;">SkynetJoe Weekly Digest | <a href="${websiteUrl}" style="color:${brandColor};">${websiteUrl.replace('https://','')}</a></p>
      </td></tr>
    </table></body></html>`;

    return [{ json: {
      html, subject: 'SkynetJoe Weekly Digest - ' + dateShort,
      recipientEmail: config.recipientEmail || 'waseemhome8@gmail.com',
      senderEmail: config.senderEmail || 'waseem@skynetjoe.com'
    }}];
    """)
    th6 = code_node("Build Email - Newsletter", [x(5), Y_THU], build_nl_email_code)
    nodes.append(th6)

    # Th7. Send Email - Newsletter
    th7 = email_send("Send Email - Newsletter", [x(6), Y_THU],
                     "={{ $json.recipientEmail }}",
                     "={{ $json.senderEmail }}",
                     "={{ $json.subject }}",
                     "={{ $json.html }}")
    nodes.append(th7)

    # Thursday connections
    connections.update({
        "Schedule - Thursday 9AM": {"main": [[{"node": "Load State - Thursday", "type": "main", "index": 0}]]},
        "Load State - Thursday": {"main": [[{"node": "GPT Newsletter", "type": "main", "index": 0}]]},
        "GPT Newsletter": {"main": [[{"node": "Clean Newsletter", "type": "main", "index": 0}]]},
        "Clean Newsletter": {"main": [[{"node": "Save State - Thursday", "type": "main", "index": 0}]]},
        "Save State - Thursday": {"main": [[{"node": "Build Email - Newsletter", "type": "main", "index": 0}]]},
        "Build Email - Newsletter": {"main": [[{"node": "Send Email - Newsletter", "type": "main", "index": 0}]]},
    })

    # ======================================================================
    #  FRIDAY AGENT  — Video Scripts + Brand Collab
    # ======================================================================

    f1 = schedule_trigger("Schedule - Friday 9AM", [x(0), Y_FRI], "0 1 * * 5")
    nodes.append(f1)

    f2 = make_load_state("Load State - Friday", [x(1), Y_FRI],
                         ["strategy", "clientConfig", "research", "article", "linkedinPost"])
    nodes.append(f2)

    # F3. GPT Video Scripts
    f3_sys = (
        "=You are a video script writer for Waseem Nasir / SkynetJoe. "
        "Waseem is currently filming from Bali, Indonesia."
    )
    f3_user = textwrap.dedent("""\
    =Create TWO video scripts for Waseem Nasir / SkynetJoe.

    This week's topic: {{ $('Load State - Friday').first().json.strategy.primaryKeyword }}
    Article: {{ $('Load State - Friday').first().json.article.metadata.title }}
    Travel context: Filming from Bali, Indonesia

    SCRIPT 1 -- SHORT-FORM (under 60 seconds):
    - For: Instagram Reel, TikTok, YouTube Shorts
    - Hook in first 3 seconds (pattern interrupt)
    - 1 key insight or stat
    - Visual directions in [brackets] -- include Bali B-roll suggestions (rice terraces, coworking space, beach, villa workspace)
    - CTA: "Follow for more AI + travel tips" or "Link in bio"
    - Tone: Casual, energetic, "I'm literally filming this from a Bali cafe"

    SCRIPT 2 -- LONG-FORM (3-5 minutes):
    - For: YouTube
    - Hook (30s): Start with Bali establishing shot + "I'm running a $X agency from this..."
    - 3-4 talking points with analysis
    - B-roll suggestions in [brackets]
    - Include at least one "what I learned from doing this in Bali" moment
    - Subscribe CTA + website plug
    - Timestamps

    Output both scripts with clear labels and timing cues.
    """)
    f3 = openai_node("GPT Video Scripts", [x(2), Y_FRI], f3_sys, f3_user,
                     temp=0.7, max_tokens=2048)
    nodes.append(f3)

    # F4. GPT Brand Collab Pitch
    f4_sys = (
        "=You are a brand partnership strategist for Waseem Nasir / SkynetJoe. "
        "Generate pitch emails for brand collaborations."
    )
    f4_user = textwrap.dedent("""\
    =Generate a BRAND COLLABORATION PITCH OF THE WEEK for Waseem Nasir / SkynetJoe.

    This week's content topic: {{ $('Load State - Friday').first().json.strategy.primaryKeyword }}
    Brand collab opportunity: {{ $('Load State - Friday').first().json.strategy.brandCollabOpportunity || 'AI/SaaS tool relevant to this week topic' }}

    Based on this week's content, identify the BEST brand to pitch and write:

    1. **Target Brand**: Name + why they're a fit
    2. **Pitch Email** (3-4 paragraphs):
       - Opening: Reference their product + how Waseem uses it
       - Value prop: Waseem's audience (SMB owners, entrepreneurs), unique angle (AI founder traveling ASEAN)
       - Collaboration idea: Specific content piece (review, tutorial, "I used [product] in Bali for 30 days")
       - CTA: 15-min call or DM
    3. **Pitch Metrics** to include: follower counts, engagement rates, audience demographics

    Target brand categories to rotate through: VPN (NordVPN/Surfshark), eSIM (Airalo/Holafly), travel insurance (SafetyWing), SaaS (Notion/Canva), luggage (Away/Nomatic), banking (Wise/Revolut), coworking (Hubud/Outpost), hosting (Hostinger), AI tools (n8n/Make)

    Format as clean HTML with copy-ready sections.
    """)
    f4 = openai_node("GPT Brand Collab Pitch", [x(2), Y_FRI + 120], f4_sys, f4_user,
                     temp=0.7, max_tokens=1024)
    nodes.append(f4)

    # F5. Clean Scripts
    clean_scripts_code = textwrap.dedent("""\
    // Clean video scripts and brand pitch output
    const items = $input.all();
    function extractText(r) {
      if (!r) return '';
      if (typeof r === 'string') return r;
      if (r.text) return r.text;
      if (r.message?.content) return r.message.content;
      if (r.output) return typeof r.output === 'string' ? r.output : JSON.stringify(r.output);
      return JSON.stringify(r);
    }
    let scripts = extractText(items[0]?.json).replace(/```/g, '');
    let brandPitch = '';
    try { brandPitch = extractText(items[1]?.json).replace(/```html\\n?/g, '').replace(/```/g, ''); } catch(e) {}
    return [{ json: { videoScripts: scripts, brandPitch } }];
    """)
    f5 = code_node("Clean Scripts", [x(3), Y_FRI], clean_scripts_code)
    nodes.append(f5)

    # F6. Save Content History
    save_history_code = textwrap.dedent("""\
    // Save this week's content to history for deduplication
    const staticData = $getWorkflowStaticData('global');
    if (!staticData.contentHistory) staticData.contentHistory = [];

    const pipeline = staticData.pipeline || {};
    staticData.contentHistory.push({
      timestamp: new Date().toISOString(),
      week: new Date().toISOString().split('T')[0],
      primaryKeyword: pipeline.prepKeywords?.primaryKeyword,
      secondaryKeywords: pipeline.strategy?.secondaryKeywords,
      articleTitle: pipeline.article?.metadata?.title,
      articleSlug: pipeline.article?.metadata?.slug,
      articleAngle: pipeline.strategy?.articleAngle,
      articleStructure: pipeline.prepKeywords?.articleStructure,
      topStoryTitle: pipeline.research?.topStory?.title,
      topStoryUrl: pipeline.research?.topStory?.url,
      storyUrls: (pipeline.research?.rankedStories || []).map(s => s.url),
      aeoScore: pipeline.article?.metadata?.aeoScore || pipeline.article?.aeoScore,
      travelRelevance: pipeline.article?.metadata?.travelRelevance,
      brandPitched: '',
      runNumber: pipeline.prepKeywords?.runNumber,
    });

    // Keep last 52 entries (1 year)
    if (staticData.contentHistory.length > 52) {
      staticData.contentHistory = staticData.contentHistory.slice(-52);
    }

    return [{ json: { status: 'History saved', totalEntries: staticData.contentHistory.length } }];
    """)
    f6 = code_node("Save Content History", [x(4), Y_FRI], save_history_code)
    nodes.append(f6)

    # F7. Save State Friday
    f7 = code_node("Save State - Friday", [x(5), Y_FRI], textwrap.dedent("""\
    const staticData = $getWorkflowStaticData('global');
    const scripts = $('Clean Scripts').first().json;
    staticData.pipeline.videoScripts = scripts.videoScripts;
    staticData.pipeline.brandPitch = scripts.brandPitch;
    staticData.pipeline.__lastUpdated = new Date().toISOString();
    staticData.pipeline.__lastStage = 'friday';
    return [{ json: { status: 'Friday agent complete' } }];
    """))
    nodes.append(f7)

    # F8. Build Emails - Friday (Scripts + Actions)
    build_fri_email_code = textwrap.dedent("""\
    // Build Friday emails: Video Scripts + Weekly Action Steps + Brand Pitch
    const pipeline = $getWorkflowStaticData('global').pipeline || {};
    const config = pipeline.clientConfig || {};
    const brandColor = config.brandColor || '#13b973';
    const secondaryColor = config.secondaryColor || '#8B5CF6';
    const websiteUrl = config.websiteUrl || 'https://www.skynetjoe.com';
    const videoScripts = pipeline.videoScripts || '';
    const brandPitch = pipeline.brandPitch || '';
    const article = pipeline.article || {};
    const meta = article.metadata || {};
    const date = new Date().toLocaleDateString('en-US', { weekday: 'long', year: 'numeric', month: 'long', day: 'numeric' });

    // Email 1: Video Scripts
    const scriptsHtml = `<!DOCTYPE html><html><head><meta charset="utf-8"><meta name="viewport" content="width=device-width"></head>
    <body style="margin:0;padding:0;background:#0a0a0a;font-family:-apple-system,BlinkMacSystemFont,'Segoe UI',Roboto,sans-serif;">
    <table width="100%" cellpadding="0" cellspacing="0" style="max-width:680px;margin:0 auto;">
      <tr><td style="background:linear-gradient(135deg,${secondaryColor},${brandColor});padding:32px 24px;text-align:center;">
        <h1 style="color:#fff;margin:0 0 4px;font-size:22px;">SkynetJoe Video Scripts</h1>
        <p style="color:rgba(255,255,255,0.7);margin:0;font-size:13px;">${date}</p>
      </td></tr>
      <tr><td style="background:#111;padding:28px 24px;color:#e0e0e0;">
        <p style="font-size:11px;text-transform:uppercase;letter-spacing:2px;color:${brandColor};margin:0 0 16px;">VIDEO SCRIPTS</p>
        <p style="color:#aaa;margin:0 0 16px;font-size:13px;">Short-form (Reel/TikTok/Short) + Long-form (YouTube). Bali B-roll suggestions included.</p>
        <div style="white-space:pre-wrap;font-size:14px;line-height:1.7;color:#ddd;">${videoScripts}</div>
      </td></tr>
      <tr><td style="background:#0a0a0a;padding:20px 24px;text-align:center;">
        <p style="color:#666;font-size:12px;margin:0;">SkynetJoe AEO Engine v2.0</p>
      </td></tr>
    </table></body></html>`;

    // Email 2: Action Steps + Brand Pitch
    const actionsHtml = `<!DOCTYPE html><html><head><meta charset="utf-8"><meta name="viewport" content="width=device-width"></head>
    <body style="margin:0;padding:0;background:#0a0a0a;font-family:-apple-system,BlinkMacSystemFont,'Segoe UI',Roboto,sans-serif;">
    <table width="100%" cellpadding="0" cellspacing="0" style="max-width:680px;margin:0 auto;">
      <tr><td style="background:linear-gradient(135deg,${secondaryColor},${brandColor});padding:32px 24px;text-align:center;">
        <h1 style="color:#fff;margin:0 0 4px;font-size:22px;">Weekly Action Steps</h1>
        <p style="color:rgba(255,255,255,0.7);margin:0;font-size:13px;">${date} | Your publishing checklist</p>
      </td></tr>
      <tr><td style="background:#111;padding:28px 24px;color:#e0e0e0;">
        <div style="background:#1a1a2e;border-radius:10px;padding:20px;margin-bottom:16px;border-left:4px solid ${brandColor};">
          <p style="color:${brandColor};font-size:12px;text-transform:uppercase;letter-spacing:1.5px;margin:0 0 6px;">STEP 1</p>
          <p style="color:#fff;font-size:16px;font-weight:700;margin:0 0 8px;">Record Videos</p>
          <p style="color:#ccc;font-size:14px;margin:0;line-height:1.6;">Use the video scripts email. Film the short-form reel first (60s). Then the YouTube video (3-5 min). Suggested Bali filming spots: Canggu coworking, rice terrace backdrop, beach sunset.</p>
        </div>
        <div style="background:#1a1a2e;border-radius:10px;padding:20px;margin-bottom:16px;border-left:4px solid ${brandColor};">
          <p style="color:${brandColor};font-size:12px;text-transform:uppercase;letter-spacing:1.5px;margin:0 0 6px;">STEP 2</p>
          <p style="color:#fff;font-size:16px;font-weight:700;margin:0 0 8px;">Upload Article to CMS</p>
          <p style="color:#ccc;font-size:14px;margin:0;line-height:1.6;">Open Wednesday's article email. Copy the HTML into your WordPress blog post editor. Add featured image, review, publish.</p>
        </div>
        <div style="background:#1a1a2e;border-radius:10px;padding:20px;margin-bottom:16px;border-left:4px solid ${brandColor};">
          <p style="color:${brandColor};font-size:12px;text-transform:uppercase;letter-spacing:1.5px;margin:0 0 6px;">STEP 3</p>
          <p style="color:#fff;font-size:16px;font-weight:700;margin:0 0 8px;">Send Newsletter</p>
          <p style="color:#ccc;font-size:14px;margin:0;line-height:1.6;">Open Thursday's newsletter email. Update the article link with your live URL. Send via your CRM or email tool.</p>
        </div>
        <div style="background:#1a1a2e;border-radius:10px;padding:20px;margin-bottom:16px;border-left:4px solid ${brandColor};">
          <p style="color:${brandColor};font-size:12px;text-transform:uppercase;letter-spacing:1.5px;margin:0 0 6px;">STEP 4</p>
          <p style="color:#fff;font-size:16px;font-weight:700;margin:0 0 8px;">Post LinkedIn Content</p>
          <p style="color:#ccc;font-size:14px;margin:0;line-height:1.6;">Copy the LinkedIn post from Wednesday's email. Paste into LinkedIn. Add a relevant image or video. Publish.</p>
        </div>
        <div style="background:#1a1a2e;border-radius:10px;padding:20px;margin-bottom:16px;border-left:4px solid ${secondaryColor};">
          <p style="color:${secondaryColor};font-size:12px;text-transform:uppercase;letter-spacing:1.5px;margin:0 0 6px;">STEP 5</p>
          <p style="color:#fff;font-size:16px;font-weight:700;margin:0 0 8px;">Send Brand Pitch</p>
          <p style="color:#ccc;font-size:14px;margin:0;line-height:1.6;">Review the brand collaboration pitch below. Customize the opening line. Send via email or LinkedIn DM.</p>
        </div>

        ${brandPitch ? `
        <div style="margin-top:24px;">
          <p style="font-size:11px;text-transform:uppercase;letter-spacing:2px;color:${secondaryColor};margin:0 0 16px;">BRAND PITCH OF THE WEEK</p>
          <div style="background:#1a1a2e;border-radius:8px;padding:20px;border:1px solid #333;font-size:14px;line-height:1.7;color:#ddd;">${brandPitch}</div>
        </div>` : ''}
      </td></tr>
      <tr><td style="background:#0a0a0a;padding:20px 24px;text-align:center;">
        <p style="color:#666;font-size:12px;margin:0;">SkynetJoe AEO Engine v2.0 | <a href="${websiteUrl}" style="color:${brandColor};">${websiteUrl.replace('https://','')}</a></p>
      </td></tr>
    </table></body></html>`;

    return [
      { json: { html: scriptsHtml, subject: 'SkynetJoe Video Scripts - ' + (meta.title || 'This Week'), recipientEmail: config.recipientEmail || 'waseemhome8@gmail.com', senderEmail: config.senderEmail || 'waseem@skynetjoe.com', emailType: 'scripts' } },
      { json: { html: actionsHtml, subject: 'SkynetJoe Weekly Action Steps + Brand Pitch', recipientEmail: config.recipientEmail || 'waseemhome8@gmail.com', senderEmail: config.senderEmail || 'waseem@skynetjoe.com', emailType: 'actions' } },
    ];
    """)
    f8 = code_node("Build Emails - Friday", [x(6), Y_FRI], build_fri_email_code)
    nodes.append(f8)

    # F9. Send Email - Scripts
    f9 = email_send("Send Email - Scripts", [x(7), Y_FRI - 60],
                    "={{ $json.recipientEmail }}",
                    "={{ $json.senderEmail }}",
                    "={{ $json.subject }}",
                    "={{ $json.html }}")
    nodes.append(f9)

    # F10. Send Email - Actions
    f10 = email_send("Send Email - Actions", [x(7), Y_FRI + 60],
                     "={{ $json.recipientEmail }}",
                     "={{ $json.senderEmail }}",
                     "={{ $json.subject }}",
                     "={{ $json.html }}")
    nodes.append(f10)

    # Friday connections
    connections.update({
        "Schedule - Friday 9AM": {"main": [[{"node": "Load State - Friday", "type": "main", "index": 0}]]},
        "Load State - Friday": {"main": [[
            {"node": "GPT Video Scripts", "type": "main", "index": 0},
            {"node": "GPT Brand Collab Pitch", "type": "main", "index": 0},
        ]]},
        "GPT Video Scripts": {"main": [[{"node": "Clean Scripts", "type": "main", "index": 0}]]},
        "GPT Brand Collab Pitch": {"main": [[{"node": "Clean Scripts", "type": "main", "index": 0}]]},
        "Clean Scripts": {"main": [[{"node": "Save Content History", "type": "main", "index": 0}]]},
        "Save Content History": {"main": [[{"node": "Save State - Friday", "type": "main", "index": 0}]]},
        "Save State - Friday": {"main": [[{"node": "Build Emails - Friday", "type": "main", "index": 0}]]},
        "Build Emails - Friday": {"main": [[
            {"node": "Send Email - Scripts", "type": "main", "index": 0},
            {"node": "Send Email - Actions", "type": "main", "index": 0},
        ]]},
    })

    # ======================================================================
    #  UTILITY NODES  — Manual Reset
    # ======================================================================

    # U1. Reset Pipeline State
    u1_trigger = manual_trigger("RESET Pipeline - Trigger", [x(0), Y_UTIL])
    nodes.append(u1_trigger)

    u1_code = code_node("RESET Pipeline State", [x(1), Y_UTIL], textwrap.dedent("""\
    // Clear pipeline state so agents start fresh
    const staticData = $getWorkflowStaticData('global');
    staticData.pipeline = {};
    return [{ json: { status: 'Pipeline state cleared', timestamp: new Date().toISOString() } }];
    """))
    nodes.append(u1_code)

    # U2. Reset Content History
    u2_trigger = manual_trigger("RESET History - Trigger", [x(3), Y_UTIL])
    nodes.append(u2_trigger)

    u2_code = code_node("RESET Content History", [x(4), Y_UTIL], textwrap.dedent("""\
    // Clear all content history (keyword rotation, dedup, etc.)
    const staticData = $getWorkflowStaticData('global');
    staticData.contentHistory = [];
    return [{ json: { status: 'Content history cleared', timestamp: new Date().toISOString() } }];
    """))
    nodes.append(u2_code)

    # Utility connections
    connections.update({
        "RESET Pipeline - Trigger": {"main": [[{"node": "RESET Pipeline State", "type": "main", "index": 0}]]},
        "RESET History - Trigger": {"main": [[{"node": "RESET Content History", "type": "main", "index": 0}]]},
    })

    return build_workflow(
        "SkynetJoe Weekly AEO Content Engine v2.0 - 5 Agent Split",
        nodes, connections
    )


# ############################################################################
#                              MAIN
# ############################################################################

def main():
    print("=" * 70)
    print("  SkynetJoe AEO Content Engine v2.0 — Build Script")
    print("=" * 70)
    print()

    # Build both workflows
    daily = build_daily_digest()
    weekly = build_weekly_aeo()

    # Write JSON files
    with open(DAILY_OUT, "w", encoding="utf-8") as f:
        json.dump(daily, f, indent=2, ensure_ascii=False)

    with open(WEEKLY_OUT, "w", encoding="utf-8") as f:
        json.dump(weekly, f, indent=2, ensure_ascii=False)

    # Stats
    daily_size = os.path.getsize(DAILY_OUT)
    weekly_size = os.path.getsize(WEEKLY_OUT)
    daily_nodes = len(daily["nodes"])
    weekly_nodes = len(weekly["nodes"])

    print(f"  FILE 1: SKYNETJOE-DAILY-DIGEST-v2.0.json")
    print(f"    Nodes: {daily_nodes}")
    print(f"    Size:  {daily_size:,} bytes ({daily_size/1024:.1f} KB)")
    print()
    print(f"  FILE 2: SKYNETJOE-WEEKLY-AEO-v2.0.json")
    print(f"    Nodes: {weekly_nodes}")
    print(f"    Size:  {weekly_size:,} bytes ({weekly_size/1024:.1f} KB)")
    print()
    print(f"  Output: {SCRIPT_DIR}")
    print()
    print("-" * 70)
    print("  WEEKLY AEO NODE BREAKDOWN")
    print("-" * 70)
    print(f"    Monday   (Keyword Strategy):  10 nodes")
    print(f"    Tuesday  (Deep Research):      9 nodes")
    print(f"    Wednesday (Article Writer):   10 nodes")
    print(f"    Thursday (Newsletter):         7 nodes")
    print(f"    Friday   (Scripts + Brand):   10 nodes")
    print(f"    Utility  (Reset):              4 nodes")
    print(f"    TOTAL:                        {weekly_nodes} nodes")
    print()
    print("-" * 70)
    print("  CREDENTIAL SETUP (replace these in n8n after import)")
    print("-" * 70)
    print("  1. OpenAI API       -> REPLACE_WITH_YOUR_OPENAI_CREDENTIAL_ID")
    print("     Model: gpt-4.1")
    print()
    print("  2. Serper API       -> REPLACE_WITH_YOUR_SERPER_CREDENTIAL_ID")
    print("     Used for: SERP + PAA research (Monday agent)")
    print("     Setup: serper.dev -> get API key -> n8n Serper credential")
    print()
    print("  3. SMTP             -> REPLACE_WITH_YOUR_SMTP_CREDENTIAL_ID")
    print("     Used for: All email sends (daily digest + 4 weekly emails)")
    print("     Setup: n8n SMTP credential with your mail server details")
    print()
    print("  4. Gemini API Key   -> REPLACE_WITH_GEMINI_API_KEY")
    print("     Used for: Deep research analysis (Tuesday agent)")
    print("     Setup: Replace in the URL of 'Gemini Deep Research' node")
    print("     OR set GEMINI_API_KEY environment variable in n8n")
    print()
    print("-" * 70)
    print("  IMPORT INSTRUCTIONS")
    print("-" * 70)
    print("  1. Open n8n -> Workflows -> Import from File")
    print("  2. Import SKYNETJOE-DAILY-DIGEST-v2.0.json")
    print("  3. Import SKYNETJOE-WEEKLY-AEO-v2.0.json")
    print("  4. In each workflow, click the credential warning icons")
    print("     and map to your existing credentials")
    print("  5. In the Weekly AEO, update the Gemini API key in the URL")
    print("  6. Test each agent manually (click each Schedule Trigger)")
    print("  7. Activate both workflows when ready")
    print()
    print("=" * 70)
    print("  Build complete!")
    print("=" * 70)


if __name__ == "__main__":
    main()
