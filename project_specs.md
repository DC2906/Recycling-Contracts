# Project Specs: Recycling Contracts Dashboard

---

## Overview

A web-based dashboard for a small team (2–5 people) to track, manage, and view
recycling and waste collection contracts with councils or businesses. Contract
data is sourced by scraping council and government websites. Data is stored in
Google Sheets. The dashboard displays contract details including financial
information, key dates, and status.

---

## What We Are Building

A two-part system:

1. **Web Scraper** — Python scripts that extract recycling contract and pricing
   data from council/government websites and write it to Google Sheets.
2. **Web Dashboard** — A browser-based UI that reads from Google Sheets and
   displays contract data with filtering and financial summaries.

---

## User Inputs

| Input | Description |
|---|---|
| Target URLs | List of council/government websites to scrape |
| Google Sheet ID | The destination spreadsheet for scraped data |
| Manual triggers | Run scraper script on demand (no automated schedule yet) |

---

## Data Fields (per contract)

Each contract record will store the following fields in Google Sheets:

| Field | Description |
|---|---|
| Contract ID | Unique reference number |
| Council / Business Name | Name of the contracting organisation |
| Material Type | e.g. Cardboard, Plastic, Glass, Mixed Recyclables |
| Contract Start Date | When the contract begins |
| Contract End Date | When the contract expires |
| Contract Value ($) | Total dollar value of the contract |
| Pricing per Tonne ($) | Rate charged per tonne of material |
| Status | Active / Expired / Pending / Unknown |
| Contact Person | Name and/or email of key contact |
| Source URL | The webpage where this data was scraped from |
| Last Updated | Timestamp of when the record was last scraped/updated |
| Notes | Free-text field for team comments |

---

## Workflows

### Workflow 1: Scrape Contract Data
- **Trigger:** Run script manually
- **Input:** List of target URLs (stored in a config file)
- **Process:**
  1. Load target URLs from config
  2. Scrape each URL for contract/pricing data
  3. Parse and clean extracted data
  4. Write records to Google Sheets (append or update)
- **Output:** Updated Google Sheet with latest contract records
- **Files:**
  - `instructions/01_scrape_contracts.md`
  - `execution/01_scrape_contracts.py`

### Workflow 2: Display Dashboard
- **Trigger:** Open in browser
- **Input:** Google Sheets data (read via API or exported CSV)
- **Process:**
  1. Load contract data from Google Sheets
  2. Display in filterable, searchable table
  3. Show financial summary cards (total contract value, avg price/tonne, etc.)
  4. Highlight contracts expiring within 90 days
- **Output:** Live dashboard in browser
- **Files:**
  - `instructions/02_dashboard.md`
  - `execution/02_dashboard.py` (Python web server, e.g. Streamlit or Flask)

---

## Tools & Technologies

| Tool | Purpose |
|---|---|
| Python | All scripting and backend logic |
| Google Sheets | Primary data store |
| Google Sheets API (gspread) | Read/write data from Python |
| BeautifulSoup / Playwright | Web scraping |
| Streamlit (or Flask + HTML) | Web dashboard |
| `.env` file | Store API keys and credentials securely |

---

## Data Storage

- **Live data:** Google Sheets (shared with the team)
- **Temp/test data:** `.tmp/` folder as CSV files
- **Config:** `config.yaml` for target URLs and sheet settings

---

## Deployment

- **Phase 1:** Run locally (scripts triggered manually)
- **Phase 2 (future):** Deploy to Modal for scheduled scraping

---

## File Structure

```
Recycling Contracts/
├── instructions.md           ← System behaviour rules
├── project_specs.md          ← This file
├── instructions/             ← Workflow descriptions (markdown)
│   ├── 01_scrape_contracts.md
│   └── 02_dashboard.md
├── execution/                ← Python scripts
│   ├── 01_scrape_contracts.py
│   └── 02_dashboard.py
├── .env                      ← API keys (never commit this)
├── config.yaml               ← Target URLs and sheet config
└── .tmp/                     ← Temporary test data (CSV files)
```

---

## What "Done" Looks Like

- [ ] Scraper successfully extracts data from at least one council website
- [ ] Data is written correctly to Google Sheets
- [ ] Dashboard loads in browser and shows contract data from the sheet
- [ ] Dashboard displays financial summary (total value, avg price/tonne)
- [ ] Contracts expiring within 90 days are highlighted
- [ ] Team members can filter contracts by material type and status
- [ ] `.env` file holds all credentials and no secrets are hardcoded
