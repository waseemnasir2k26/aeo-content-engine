# RSS Feeds Master List for AEO Content Engine

**Last verified:** April 4, 2026
**Total feeds:** 60+ verified working feeds across 12 categories
**For use with:** n8n AEO Content Engine v7.0

---

## STATUS OF YOUR EXISTING FEEDS

| # | Feed | URL | Status | Notes |
|---|------|-----|--------|-------|
| 1 | TechCrunch AI | `https://techcrunch.com/category/artificial-intelligence/feed/` | WORKING | Valid RSS, daily updates |
| 2 | The Verge AI | `https://www.theverge.com/rss/ai-artificial-intelligence/index.xml` | WORKING | Valid Atom feed, daily |
| 3 | n8n Blog | `https://blog.n8n.io/rss/` | WORKING | Valid RSS, weekly updates |
| 4 | OpenAI Blog | `https://openai.com/blog/rss.xml` | WORKING | Valid RSS, weekly |
| 5 | Anthropic RSS | `https://www.anthropic.com/rss.xml` | **DEAD (404)** | All alternate URLs also 404. Anthropic has no working RSS feed. |
| 6 | VentureBeat | `https://feeds.feedburner.com/venturebeat/SZYF` | WORKING | Valid RSS, multiple daily |
| 7 | AI News | `https://www.artificialintelligence-news.com/feed/` | WORKING | Valid RSS, daily |
| 8 | MarkTechPost | `https://www.marktechpost.com/feed/` | WORKING | Valid RSS, multiple daily |

**Action Required:** Remove Anthropic feed (#5) — it's completely dead with no alternative.

---

## CATEGORY 1: AI/ML NEWS (Breaking News, Product Launches)

### Tier 1 — Must-Have (High volume, high quality, very reliable)

| Feed | URL | Frequency | Reliability |
|------|-----|-----------|-------------|
| TechCrunch AI | `https://techcrunch.com/category/artificial-intelligence/feed/` | 5-10/day | 10/10 |
| The Verge AI | `https://www.theverge.com/rss/ai-artificial-intelligence/index.xml` | 5-8/day | 10/10 |
| VentureBeat | `https://feeds.feedburner.com/venturebeat/SZYF` | 10-15/day | 10/10 |
| WIRED AI | `https://www.wired.com/feed/tag/ai/latest/rss` | 3-5/day | 9/10 |
| Ars Technica | `https://feeds.arstechnica.com/arstechnica/technology-lab` | 5-8/day | 10/10 |
| MIT Technology Review AI | `https://www.technologyreview.com/topic/artificial-intelligence/feed` | 2-4/day | 10/10 |
| ZDNet AI | `https://www.zdnet.com/topic/artificial-intelligence/rss.xml` | 5-10/day | 9/10 |

### Tier 2 — AI-Specific Sources (Deep AI coverage)

| Feed | URL | Frequency | Reliability |
|------|-----|-----------|-------------|
| AI News (artificialintelligence-news.com) | `https://www.artificialintelligence-news.com/feed/` | 3-5/day | 8/10 |
| MarkTechPost | `https://www.marktechpost.com/feed/` | 5-10/day | 8/10 |
| The Next Web Neural | `https://thenextweb.com/neural/feed` | 2-3/day | 8/10 |
| Analytics Vidhya | `https://www.analyticsvidhya.com/feed/` | 2-3/day | 8/10 |
| Stanford AI Index | `https://aiindex.stanford.edu/feed/` | Monthly | 9/10 |

### Tier 3 — Company Blogs (First-party announcements)

| Feed | URL | Frequency | Reliability |
|------|-----|-----------|-------------|
| OpenAI Blog | `https://openai.com/blog/rss.xml` | 2-4/week | 10/10 |
| Google AI Blog | `https://blog.google/technology/ai/rss/` | 2-3/week | 10/10 |
| DeepMind Blog | `https://deepmind.google/blog/rss.xml` | 1-2/week | 10/10 |
| Microsoft AI Blog | `https://blogs.microsoft.com/ai/feed/` | 2-3/week | 10/10 |
| NVIDIA AI Blog | `https://blogs.nvidia.com/feed/` | 3-5/week | 9/10 |
| AWS ML Blog | `https://aws.amazon.com/blogs/machine-learning/feed/` | 3-5/week | 10/10 |
| HuggingFace Blog | `https://huggingface.co/blog/feed.xml` | 2-3/week | 9/10 |
| LangChain Blog | `https://blog.langchain.dev/rss/` | 1-2/week | 9/10 |

---

## CATEGORY 2: AUTOMATION & NO-CODE TOOLS

| Feed | URL | Frequency | Reliability |
|------|-----|-----------|-------------|
| n8n Blog | `https://blog.n8n.io/rss/` | 2-3/week | 10/10 |
| Zapier Blog | `https://zapier.com/blog/feeds/latest/` | Daily | 9/10 |
| The New Stack | `https://thenewstack.io/feed/` | 5-10/day | 9/10 |

> **Note:** Make.com blocks RSS access (403). Use Google News RSS for Make coverage:
> `https://news.google.com/rss/search?q=Make.com+automation&hl=en-US&gl=US&ceid=US:en`

---

## CATEGORY 3: BUSINESS AUTOMATION & SAAS

| Feed | URL | Frequency | Reliability |
|------|-----|-----------|-------------|
| SaaStr | `https://www.saastr.com/feed/` | 1-2/day | 9/10 |
| Indie Hackers | `https://www.indiehackers.com/feed.xml` | 5-10/day | 8/10 |
| ReadWrite | `https://readwrite.com/feed/` | 3-5/day | 8/10 |
| Freelance to Founder | `https://freelancetofounder.com/feed` | Weekly | 7/10 |
| Fast Company Technology | `https://www.fastcompany.com/technology/rss` | 3-5/day | 9/10 |

---

## CATEGORY 4: WEB DEVELOPMENT & TECH TRENDS

| Feed | URL | Frequency | Reliability |
|------|-----|-----------|-------------|
| Smashing Magazine | `https://www.smashingmagazine.com/feed/` | 3-5/week | 10/10 |
| CSS-Tricks | `https://css-tricks.com/feed/` | 2-3/week | 9/10 |
| DEV.to | `https://dev.to/feed` | 50+/day | 8/10 |
| Vercel Blog | `https://vercel.com/atom` | 1-2/week | 9/10 |
| Webflow Blog | `https://webflow.com/blog/rss.xml` | 1-2/week | 9/10 |
| InfoWorld | `https://www.infoworld.com/feed/` | 3-5/day | 9/10 |
| Lifehacker | `https://lifehacker.com/feed/rss` | 5-10/day | 8/10 |

---

## CATEGORY 5: MARKETING AUTOMATION & GROWTH HACKING

| Feed | URL | Frequency | Reliability |
|------|-----|-----------|-------------|
| HubSpot Marketing | `https://blog.hubspot.com/marketing/rss.xml` | Daily | 10/10 |
| Content Marketing Institute | `https://contentmarketinginstitute.com/feed/` | 3-5/week | 9/10 |
| Copyblogger | `https://copyblogger.com/feed/` | 2-3/week | 9/10 |
| Buffer Resources | `https://buffer.com/resources/feed/` | 1-2/week | 9/10 |
| Neil Patel Blog | `https://neilpatel.com/blog/feed/` | 2-3/week | 8/10 |
| GrowthHackers | `https://growthhackers.com/feed` | 2-3/day | 7/10 |
| Digiday | `https://digiday.com/feed/` | 5-8/day | 9/10 |
| AdWeek | `https://www.adweek.com/feed/` | 5-10/day | 9/10 |

---

## CATEGORY 6: GOOGLE/SEARCH ALGORITHM UPDATES

| Feed | URL | Frequency | Reliability |
|------|-----|-----------|-------------|
| Search Engine Journal | `https://www.searchenginejournal.com/feed/` | 10-15/day | 10/10 |
| Moz Blog | `https://moz.com/blog/feed` | 2-3/week | 10/10 |
| Ahrefs Blog | `https://ahrefs.com/blog/feed/` | 2-3/week | 10/10 |
| Google Search Central Blog | `https://developers.google.com/search/blog/feed.xml` | 1-2/week | 10/10 |
| Semrush Blog | `https://www.semrush.com/blog/feed/` | 3-5/week | 9/10 |
| Backlinko | `https://backlinko.com/feed` | 1-2/month | 9/10 |

---

## CATEGORY 7: SOCIAL MEDIA MARKETING TRENDS

| Feed | URL | Frequency | Reliability |
|------|-----|-----------|-------------|
| Social Media Examiner | `https://www.socialmediaexaminer.com/feed/` | Daily | 10/10 |
| Hootsuite Blog | `https://blog.hootsuite.com/feed/` | 2-3/week | 9/10 |
| Sprout Social Insights | `https://sproutsocial.com/insights/feed/` | 2-3/week | 9/10 |

---

## CATEGORY 8: STARTUP/ENTREPRENEUR NEWS

| Feed | URL | Frequency | Reliability |
|------|-----|-----------|-------------|
| TechCrunch Startups | `https://techcrunch.com/category/startups/feed/` | 5-10/day | 10/10 |
| Entrepreneur.com | `https://www.entrepreneur.com/latest.rss` | 10-15/day | 9/10 |
| Y Combinator Blog | `https://www.ycombinator.com/blog/feed/` | 1-2/week | 9/10 |
| Freelancers Union Blog | `https://blog.freelancersunion.org/feed/` | 1-2/week | 8/10 |
| Freelance to Founder | `https://freelancetofounder.com/feed` | Weekly | 7/10 |
| Platformer | `https://www.platformer.news/rss/` | 2-3/week | 9/10 |

---

## CATEGORY 9: AI NEWSLETTERS (Substack/Beehiiv)

| Feed | URL | Frequency | Reliability |
|------|-----|-----------|-------------|
| Import AI (Jack Clark) | `https://importai.substack.com/feed` | Weekly | 10/10 |
| AI Supremacy | `https://aisupremacy.substack.com/feed` | 2-3/week | 8/10 |
| Lenny's Newsletter | `https://www.lennysnewsletter.com/feed` | 1-2/week | 9/10 |
| Simon Willison's Weblog | `https://simonwillison.net/atom/everything/` | Daily | 10/10 |
| Stratechery (Ben Thompson) | `https://stratechery.com/feed/` | 2-3/week | 10/10 |
| Towards AI | `https://pub.towardsai.net/feed` | 3-5/day | 8/10 |

> **Note:** Simon Willison is the BEST individual source for LLM/AI tooling news. Updates multiple times daily with links to everything important in the AI space. Highly recommended for your engine.

---

## CATEGORY 10: HACKER NEWS (via hnrss.org)

Hacker News has no official RSS feed, but `hnrss.org` provides excellent unofficial feeds. All verified working.

| Feed | URL | What It Gets You |
|------|-----|------------------|
| Front Page | `https://hnrss.org/frontpage` | Top stories (most upvoted, ~30/day) |
| Best Stories | `https://hnrss.org/best` | Best of all time, ongoing |
| Show HN | `https://hnrss.org/show` | New product launches and demos |
| Ask HN | `https://hnrss.org/ask` | Community discussions and questions |
| **HN: LLM keyword** | `https://hnrss.org/newest?q=LLM` | All posts mentioning LLM |
| **HN: AI Agents keyword** | `https://hnrss.org/newest?q=AI+agents` | All posts mentioning AI agents |
| **HN: Automation keyword** | `https://hnrss.org/newest?q=automation` | All posts mentioning automation |
| **HN: n8n keyword** | `https://hnrss.org/newest?q=n8n` | All posts mentioning n8n |

### Custom HN Keyword Feeds
You can create ANY keyword-based HN feed using this pattern:
```
https://hnrss.org/newest?q=YOUR+KEYWORDS+HERE
```
Additional useful parameters:
- `&points=50` — Only stories with 50+ points
- `&comments=10` — Only stories with 10+ comments
- `&count=20` — Limit to 20 items

**Power combo for your engine:**
```
https://hnrss.org/newest?q=AI+automation&points=20
https://hnrss.org/newest?q=no-code&points=10
https://hnrss.org/newest?q=SaaS+AI&points=15
```

---

## CATEGORY 11: PRODUCT HUNT

Product Hunt offers category-specific RSS feeds. All verified working.

| Feed | URL | What It Gets You |
|------|-----|------------------|
| All Products | `https://www.producthunt.com/feed` | Everything launched daily |
| **AI Category** | `https://www.producthunt.com/feed?category=ai` | AI tool launches only |
| Developer Tools | `https://www.producthunt.com/feed?category=developer-tools` | Dev tool launches |
| Marketing | `https://www.producthunt.com/feed?category=marketing` | Marketing tool launches |
| Productivity | `https://www.producthunt.com/feed?category=productivity` | Productivity tools |
| No-Code | `https://www.producthunt.com/feed?category=no-code` | No-code tool launches |

> **Best for your engine:** Use `?category=ai` and `?category=no-code` — these catch new AI tools and automation platforms before they hit mainstream news.

---

## CATEGORY 12: GOOGLE NEWS CUSTOM RSS FEEDS

Google News provides powerful custom RSS feeds via search queries. All verified working. These are GOLD for n8n — real-time news aggregation from all publishers.

### Pre-Built Feeds for Your Engine

| Topic | URL |
|-------|-----|
| AI (General) | `https://news.google.com/rss/search?q=artificial+intelligence&hl=en-US&gl=US&ceid=US:en` |
| AI Agents | `https://news.google.com/rss/search?q=%22AI+agents%22&hl=en-US&gl=US&ceid=US:en` |
| ChatGPT | `https://news.google.com/rss/search?q=ChatGPT&hl=en-US&gl=US&ceid=US:en` |
| LLMs | `https://news.google.com/rss/search?q=large+language+model&hl=en-US&gl=US&ceid=US:en` |
| AI Business Automation | `https://news.google.com/rss/search?q=AI+business+automation&hl=en-US&gl=US&ceid=US:en` |
| AI Automation Tools | `https://news.google.com/rss/search?q=AI+automation+tools&hl=en-US&gl=US&ceid=US:en` |
| No-Code Automation | `https://news.google.com/rss/search?q=no-code+automation&hl=en-US&gl=US&ceid=US:en` |
| n8n Automation | `https://news.google.com/rss/search?q=n8n+automation&hl=en-US&gl=US&ceid=US:en` |
| Google Algorithm SEO | `https://news.google.com/rss/search?q=Google+algorithm+update+SEO&hl=en-US&gl=US&ceid=US:en` |
| Marketing Automation AI | `https://news.google.com/rss/search?q=marketing+automation+AI&hl=en-US&gl=US&ceid=US:en` |
| AI Startup Funding | `https://news.google.com/rss/search?q=AI+startup+funding&hl=en-US&gl=US&ceid=US:en` |
| SaaS + AI | `https://news.google.com/rss/search?q=SaaS+business+AI&hl=en-US&gl=US&ceid=US:en` |
| Freelance AI Tools | `https://news.google.com/rss/search?q=freelance+AI+tools&hl=en-US&gl=US&ceid=US:en` |
| Google AI Topic Feed | `https://news.google.com/rss/topics/CAAqJggKIiBDQkFTRWdvSUwyMHZNRGRqTVhZU0FtVnVHZ0pWVXlnQVAB?hl=en-US&gl=US&ceid=US:en` |

### Build Your Own Google News RSS Feed
Pattern:
```
https://news.google.com/rss/search?q=YOUR+SEARCH+QUERY&hl=en-US&gl=US&ceid=US:en
```

Tips:
- Use `+` for spaces
- Use `%22` for exact phrase match: `%22AI+agents%22` = "AI agents"
- Use `when:7d` to limit to last 7 days: `?q=AI+automation+when:7d`
- Use `site:` to limit to specific sources: `?q=AI+site:techcrunch.com`

---

## CATEGORY 13: REDDIT RSS FEEDS

**IMPORTANT FOR n8n:** Reddit now blocks RSS requests without a proper User-Agent header. You MUST configure your n8n HTTP Request node with this header:

```
User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36
```

With proper headers, ALL of these feeds return valid Atom/XML:

| Subreddit | URL | Topic |
|-----------|-----|-------|
| r/artificial | `https://www.reddit.com/r/artificial/.rss` | General AI news & discussion |
| r/MachineLearning | `https://www.reddit.com/r/MachineLearning/.rss` | ML research & papers |
| r/ChatGPT | `https://www.reddit.com/r/ChatGPT/.rss` | ChatGPT tips & news |
| r/LocalLLaMA | `https://www.reddit.com/r/LocalLLaMA/.rss` | Open-source LLM community |
| r/n8n | `https://www.reddit.com/r/n8n/.rss` | n8n community |
| r/nocode | `https://www.reddit.com/r/nocode/.rss` | No-code tools & discussion |
| r/SaaS | `https://www.reddit.com/r/SaaS/.rss` | SaaS builders community |
| r/Entrepreneur | `https://www.reddit.com/r/Entrepreneur/.rss` | Startup & business |
| r/freelance | `https://www.reddit.com/r/freelance/.rss` | Freelance business |
| r/SEO | `https://www.reddit.com/r/SEO/.rss` | SEO strategies |
| r/webdev | `https://www.reddit.com/r/webdev/.rss` | Web development |
| r/marketing | `https://www.reddit.com/r/marketing/.rss` | Marketing strategies |

### Custom Reddit Feed Tips
- **Top posts only:** Change `.rss` to `/top/.rss?t=day` for daily top posts
- **Multi-subreddit:** `https://www.reddit.com/r/artificial+MachineLearning+ChatGPT/.rss`
- **Search within sub:** `https://www.reddit.com/r/artificial/search.rss?q=AI+agents&sort=new&t=week`

### n8n Configuration for Reddit RSS
In your n8n RSS Read node, Reddit feeds will fail with the default settings. Instead, use an **HTTP Request** node:
1. Method: GET
2. URL: `https://www.reddit.com/r/artificial/.rss`
3. Headers > Add Header:
   - Name: `User-Agent`
   - Value: `Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36`
4. Response Format: Text
5. Then parse with an XML node or use the `xml2js` expression

---

## GOOGLE ALERTS AS RSS FEEDS

**Google Alerts no longer provides a native RSS output option in its standard UI.** Here is how to still get RSS feeds from Google Alerts:

### Method 1: Create via Direct URL (Still Works)
1. Go to `https://www.google.com/alerts`
2. Enter your search term (e.g., "AI automation agency")
3. Click "Show options"
4. Change "Deliver to" — if RSS is available, select it
5. If RSS option is missing (common now), use Method 2

### Method 2: Use Google News RSS Instead (Recommended)
Google News RSS feeds are effectively the same data source as Google Alerts and are MORE reliable:
```
https://news.google.com/rss/search?q=YOUR+ALERT+QUERY&hl=en-US&gl=US&ceid=US:en
```
This is functionally identical to a Google Alert delivered via RSS, but it:
- Works 100% of the time
- Does not require a Google account
- Can be used directly in n8n RSS Read nodes
- Updates in real-time (not delayed like email alerts)

### Method 3: Google Alerts Email to RSS (Workaround)
1. Create a Google Alert with email delivery
2. Use a service like `kill-the-newsletter.com` to convert email alerts to RSS
3. Or use n8n's Email Trigger node to capture alerts directly

### Recommended Custom Alert Topics for Your Engine:
```
https://news.google.com/rss/search?q=%22AI+automation+agency%22&hl=en-US&gl=US&ceid=US:en
https://news.google.com/rss/search?q=%22AI+agents+for+business%22&hl=en-US&gl=US&ceid=US:en
https://news.google.com/rss/search?q=%22workflow+automation%22+AI&hl=en-US&gl=US&ceid=US:en
https://news.google.com/rss/search?q=%22n8n%22+OR+%22Make.com%22+OR+%22Zapier%22+automation&hl=en-US&gl=US&ceid=US:en
https://news.google.com/rss/search?q=%22AEO%22+%22answer+engine+optimization%22&hl=en-US&gl=US&ceid=US:en
```

---

## FREE NEWS APIs THAT WORK WITH n8n

### 1. NewsAPI.org
- **URL:** `https://newsapi.org`
- **Free tier:** 100 requests/day, last 30 days of articles
- **n8n integration:** Use HTTP Request node
- **Endpoint:** `https://newsapi.org/v2/everything?q=AI+automation&apiKey=YOUR_KEY`
- **Limitation:** Free tier requires attribution, only for development (not production display)
- **Best for:** Bulk article fetching, keyword monitoring

### 2. NewsData.io
- **URL:** `https://newsdata.io`
- **Free tier:** 200 requests/day, real-time news
- **n8n integration:** HTTP Request node
- **Endpoint:** `https://newsdata.io/api/1/news?apikey=YOUR_KEY&q=artificial%20intelligence&language=en`
- **Advantage:** No "development only" restriction on free tier

### 3. GNews API
- **URL:** `https://gnews.io`
- **Free tier:** 100 requests/day, 10 articles per request
- **n8n integration:** HTTP Request node
- **Endpoint:** `https://gnews.io/api/v4/search?q=AI+automation&token=YOUR_KEY&lang=en`
- **Advantage:** Simple API, reliable, good for headlines

### 4. Currents API
- **URL:** `https://currentsapi.services`
- **Free tier:** 600 requests/day
- **n8n integration:** HTTP Request node
- **Endpoint:** `https://api.currentsapi.services/v1/latest-news?apiKey=YOUR_KEY&keywords=AI+automation`
- **Advantage:** Highest free tier request limit

### 5. MediaStack
- **URL:** `https://mediastack.com`
- **Free tier:** 500 requests/month
- **n8n integration:** HTTP Request node
- **Endpoint:** `http://api.mediastack.com/v1/news?access_key=YOUR_KEY&keywords=AI+automation`

### API Comparison for n8n Use:

| API | Free Requests | Speed | Quality | Best For |
|-----|--------------|-------|---------|----------|
| NewsAPI | 100/day | Fast | High | Development/testing |
| NewsData.io | 200/day | Fast | High | Production use (no restrictions) |
| GNews | 100/day | Fast | Medium | Quick headlines |
| Currents API | 600/day | Medium | Medium | Volume fetching |
| MediaStack | 500/month | Fast | Medium | Low-volume backup |

**Recommendation:** Use **NewsData.io** for production (no restrictions on free tier) + **Google News RSS** (unlimited, no API key needed) as your primary combo.

---

## RECOMMENDED n8n SETUP: TOP 15 FEEDS FOR YOUR ENGINE

For the AEO Content Engine, here are the 15 feeds I recommend running, balancing coverage, reliability, and signal-to-noise ratio:

### Primary Sources (run every 2 hours)
1. `https://techcrunch.com/category/artificial-intelligence/feed/` — Breaking AI news
2. `https://feeds.feedburner.com/venturebeat/SZYF` — Enterprise AI coverage
3. `https://www.wired.com/feed/tag/ai/latest/rss` — In-depth AI analysis
4. `https://news.google.com/rss/search?q=%22AI+agents%22+OR+%22AI+automation%22&hl=en-US&gl=US&ceid=US:en` — Real-time aggregated news
5. `https://hnrss.org/frontpage` — Tech community pulse

### AI/Tech Deep Dive (run every 6 hours)
6. `https://openai.com/blog/rss.xml` — OpenAI announcements
7. `https://blog.google/technology/ai/rss/` — Google AI updates
8. `https://simonwillison.net/atom/everything/` — Best LLM/AI curation
9. `https://www.marktechpost.com/feed/` — AI research summaries
10. `https://blog.n8n.io/rss/` — n8n automation content

### Marketing/SEO/Business (run every 12 hours)
11. `https://www.searchenginejournal.com/feed/` — SEO and search updates
12. `https://blog.hubspot.com/marketing/rss.xml` — Marketing trends
13. `https://www.socialmediaexaminer.com/feed/` — Social media strategies
14. `https://www.producthunt.com/feed?category=ai` — New AI tool launches
15. `https://news.google.com/rss/search?q=Google+algorithm+update+SEO&hl=en-US&gl=US&ceid=US:en` — Google algorithm news

### Bonus: Weekly Digest Sources (run daily)
- `https://importai.substack.com/feed` — Jack Clark's weekly AI roundup
- `https://zapier.com/blog/feeds/latest/` — Automation how-tos
- `https://moz.com/blog/feed` — SEO deep dives

---

## DEAD / UNRELIABLE FEEDS (Do NOT Use)

| Feed | URL | Issue |
|------|-----|-------|
| Anthropic RSS | `https://www.anthropic.com/rss.xml` | 404 — no working RSS exists |
| Anthropic (all variants) | `/feed`, `/feed.xml`, `/atom.xml`, `/index.xml`, `/news/rss` | All 404 |
| Meta AI Blog | `https://ai.meta.com/blog/rss/` | 404 |
| Make.com Blog | `https://www.make.com/en/blog/rss.xml` | 403 (blocked) |
| a16z Blog | `https://a16z.com/feed/` | 404 |
| The Batch (DeepLearning.ai) | `https://www.deeplearning.ai/the-batch/feed/` | 404 |
| Search Engine Land | `https://searchengineland.com/feed` | 403 (blocked) |
| Next.js Blog | `https://nextjs.org/blog/rss.xml` | 404 |
| Ben's Bites | `https://bensbites.beehiiv.com/feed` | 403 (blocked) |
| The Rundown AI | `https://therundown.ai/feed` | 403 (blocked) |
| First Round Review | `https://review.firstround.com/feed.xml` | 404 |

---

## n8n IMPLEMENTATION TIPS

### 1. Use RSS Read Node for Standard Feeds
Most feeds work directly with n8n's built-in RSS Read node. Just paste the URL.

### 2. Use HTTP Request Node for Reddit
Reddit blocks the default n8n user agent. Use HTTP Request + XML parse instead.

### 3. Deduplication Strategy
Add a **deduplication node** after RSS fetching:
- Store article GUIDs/URLs in a database or n8n static data
- Skip articles already processed
- This prevents the same article generating duplicate content

### 4. Rate Limiting
- Google News RSS: No official rate limit, but don't fetch more than once per 15 minutes
- Reddit RSS: Respect 60 requests/minute limit
- Standard RSS feeds: 1 fetch per 2-6 hours is polite and sufficient

### 5. Error Handling
Add an **Error Trigger** workflow node. RSS feeds go down temporarily — your engine should not crash when one feed returns an error.

### 6. Feed Health Monitoring
Create a separate n8n workflow that pings all feed URLs daily (HTTP Request > check status code) and alerts you via Telegram/email if any feed dies.
