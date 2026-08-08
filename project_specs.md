# Project Specs: Recycling Contracts Dashboard

---

## Overview

A web-based dashboard for a small team (2–5 people) to track, manage, and view
recycling and waste collection contracts across all 124 NSW councils. Contract
data is sourced by scraping council and government websites using a deterministic
search strategy. Data is stored in Google Sheets and local CSV caches. The dashboard
displays contract details including financial information, key dates, and status.

---

## What We Are Building

A two-part system:

1. **Web Scraper** — Deterministic Python scripts (`execution/01_scrape_contracts.py`) that perform live search discovery, page fetching, contract extraction, and HTTP URL validation across 124 NSW councils, updating Google Sheets.
2. **Web Dashboard** — A browser-based Streamlit UI (`execution/02_dashboard.py`) that reads contract data with filtering, summary KPIs, and contract expiration tracking.

---

## User Inputs & Configuration

| Input | Description |
|---|---|
| `nsw_lgas.csv` / Google Sheet | List of 124 NSW Councils |
| `config.yaml` | Scraping settings, search provider preferences, keywords, and cache locations |
| `.env` | API keys (`GOOGLE_SEARCH_API_KEY`, `GOOGLE_SEARCH_CX`, `TAVILY_API_KEY`, `GOOGLE_SERVICE_ACCOUNT_FILE`, `SPREADSHEET_ID`) |
| Manual triggers | Run scraper script on demand via Python CLI |

---

## Data Fields (per contract stream)

Each contract record contains the following 20 standardized fields:

| Field | Description | Validation Rule |
|---|---|---|
| Contract ID | Unique reference string | Format: `GIPA-[LGA_INDEX]-[STREAM]` |
| Council / Business Name | Name of the contracting LGA | Must match `nsw_lgas.csv` |
| Region | Metro, Regional, or Inland / Rural | Derived from LGA data |
| Population | Population count of the LGA | Numeric |
| Total Dwellings | Total residential dwelling count | Numeric |
| Contract Stream | Kerbside, MRF, FOGO, General Waste, Hard Waste | Categorical stream |
| Contractor / Service Provider | Name of contracted service provider | Extracted from source |
| Contract Start Date | Start date | `YYYY-MM-DD` |
| Contract End Date | Expiry date | `YYYY-MM-DD` |
| Contract Term (Years) | Duration in years | Numeric |
| Total Contract Value ($) | Total value of contract | Numeric |
| Annual Contract Value ($/year) | Annual value | Numeric |
| Annual Tonnes (t/year) | Volume processed | Numeric |
| Gate Fee / Rate ($/tonne) | Rate per tonne | Numeric |
| Status | Active / Expired / Pending / Unknown | Categorical |
| Contact Person | Department / Contact | Text |
| Council Home URL | Official council homepage | Verified HTTP 200 URL |
| Reference / Document URL | Exact source page or document URL | MUST be real & HTTP 200 verified. Set to "NOT FOUND" if missing. ZERO fabricated URLs. |
| Last Updated | ISO timestamp | `YYYY-MM-DDTHH:MM:SS` |
| Notes | Contract & GIPA metadata notes | Text |

---

## Workflows

### Workflow 1: Scrape Contract Data (Deterministic 2-Step Architecture)

- **Trigger:** Run script manually (`python execution/01_scrape_contracts.py`)
- **Inputs:** `data/nsw_lgas.csv`, `config.yaml`, `.env`
- **Process:**
  1. **Step 1: URL Discovery Engine**
     - For each council in `nsw_lgas.csv`, execute targeted web queries via Google Search API, DuckDuckGo Search, or Tavily API using exact query syntax:
       - `"[Council Name] Council" "Contract Register" OR "Contracts over 150000" OR "waste contract" site:.gov.au`
       - `site:tenders.nsw.gov.au "[Council Name]"`
     - Store top verified target URLs per council in `.tmp/council_urls.json`.
  2. **Step 2: Targeted Extraction & Processing**
     - Load discovered URLs from `.tmp/council_urls.json`.
     - Fetch page content via Playwright / BeautifulSoup / Requests.
     - Extract contract details for streams (Kerbside, MRF, FOGO, General Waste, Hard Waste).
     - Assign verified URL directly to `Reference / Document URL` field.
  3. **Step 3: Validation & Output**
     - Validate every non-null URL: must start with `http://` or `https://` AND have returned a successful `HTTP 200` status code during fetch.
     - If URL is invalid, unverified, or not found, explicitly set `Reference / Document URL` to `"NOT FOUND"`. NO inferred or pattern-guessed links allowed.
     - Export to `.tmp/contracts_cache.csv`, `data/contracts_cache.csv`, and sync to Google Sheets.
- **Output:** Validated contracts dataset across 124 councils.
- **Files:**
  - `instructions/01_scrape_contracts.md`
  - `execution/01_scrape_contracts.py`

### Workflow 2: Display Dashboard
- **Trigger:** Open in browser (`streamlit run app.py` or `python execution/02_dashboard.py`)
- **Input:** `data/contracts_cache.csv` or live Google Sheet
- **Process:** Render interactive Streamlit dashboard with summary statistics, expiring contract alerts, and stream filters.
- **Files:**
  - `instructions/02_dashboard.md`
  - `execution/02_dashboard.py`

---

## Technical Stack & Dependencies

| Tool | Purpose |
|---|---|
| Python 3.10+ | All scraping, parsing, and sync logic |
| Search APIs (DuckDuckGo / Tavily / Google Search) | Web discovery engine for NSW council tender/GIPA portals |
| Requests / BeautifulSoup4 / Playwright | HTTP fetching, DOM parsing, and JS rendering |
| Pandas | Data cleaning, structure validation, and CSV export |
| gspread / Google Sheets API | Cloud database sync |
| Streamlit | Web dashboard interface |

---

## Strict Source URL Compliance Rules

1. **NO Fabricated URLs:** Never use string templates (e.g. `f"{home_url}/council/governance"`) or domain guesses to fabricate a reference URL.
2. **Real Verification Required:** Every `Reference / Document URL` must be obtained from an actual web search result or live page link response.
3. **Explicit Fallback:** If a verified direct link is not retrieved during search/extraction, set `Reference / Document URL` to `"NOT FOUND"`.
4. **HTTP 200 Check:** Prior to saving, validate that the URL produces an HTTP 200 success response code.

---

## File Structure

```
Recycling Contracts/
├── instructions.md           ← Agent operating instructions
├── project_specs.md          ← Project specifications (this file)
├── instructions/             ← Workflow markdown guides
│   ├── 01_scrape_contracts.md
│   └── 02_dashboard.md
├── execution/                ← Python execution scripts
│   ├── 01_scrape_contracts.py
│   └── 02_dashboard.py
├── data/                     ← Persistent datasets & council mappings
│   ├── nsw_lgas.csv
│   └── contracts_cache.csv
├── .env                      ← API keys & service credentials
├── config.yaml               ← Search & scraper configuration
└── .tmp/                     ← Temporary discovery caches & outputs
    └── council_urls.json
```

---

## What "Done" Looks Like

- [x] `project_specs.md` updated with strict URL discovery engine & zero-fabrication rules.
- [ ] `instructions/01_scrape_contracts.md` updated with exact 2-step discovery & extraction specifications.
- [ ] `execution/01_scrape_contracts.py` implemented with search engine integration (DuckDuckGo / Tavily / Google Search), URL validation (HTTP 200), and "NOT FOUND" fallback handling.
- [ ] Search cache stored in `.tmp/council_urls.json`.
- [ ] Validated contracts saved to CSV and synced to Google Sheets.
