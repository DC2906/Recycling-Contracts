# Workflow 01: Scrape NSW Council Recycling & Waste Contracts

## Goal
Automate the discovery and extraction of official waste strategies, contract registers, tenders, and service provider contract streams for all 124 NSW Councils using a deterministic, multi-provider web search strategy.

## Critical Rules for Source URLs
1. **DO NOT GUESS OR GUESS-PATTERN ANY URLS:** Every `Reference / Document URL` MUST be a real, verified link retrieved directly from a live web search query or page response. String templates, domain extrapolations, and pattern-guessed paths are strictly forbidden.
2. **EXPLICIT NOT FOUND FALLBACK:** If a direct source URL is not found via web search or page fetch, set `Reference / Document URL` to `"NOT FOUND"`. Do not infer or fabricate a link under any circumstances.

## Inputs
- List of 124 NSW LGAs (`data/nsw_lgas.csv` / `.tmp/nsw_lgas.csv`).
- `config.yaml`: Search settings, keywords, and local cache paths.
- `.env`: API credentials (`GOOGLE_SEARCH_API_KEY`, `GOOGLE_SEARCH_CX`, `TAVILY_API_KEY`, `GOOGLE_SERVICE_ACCOUNT_FILE`, `SPREADSHEET_ID`).

## Execution Requirements & Steps

### Step 1: URL Discovery Engine
For each council in `nsw_lgas.csv`:
1. Execute targeted web searches using exact query formats:
   - Query A: `"[Council Name] Council" "Contract Register" OR "Contracts over 150000" OR "waste contract" site:.gov.au`
   - Query B: `site:tenders.nsw.gov.au "[Council Name]"`
2. Support search providers: Google Custom Search API, DuckDuckGo Search, or Tavily Search API.
3. Extract and verify top target URLs for each LGA.
4. Store the discovered target URL mapping in `.tmp/council_urls.json`.

### Step 2: Targeted Extraction
1. Load the verified target URL mapping from `.tmp/council_urls.json`.
2. Fetch page content using Requests / BeautifulSoup (with Playwright fallback for JS-heavy portals).
3. Extract detailed contract records across five contract streams:
   - Kerbside Collection Service
   - Dry Recyclables Processing (MRF)
   - FOGO & Organics Processing
   - General Waste Disposal & Landfill Transfer
   - Hard Waste & Bulky Goods Collection
4. Assign the explicit discovered page URL directly to the `Reference / Document URL` field.

### Step 3: Validation & Output
1. Before writing to output caches, validate every non-null URL:
   - Must begin with `http://` or `https://`
   - Must have returned a successful `HTTP 200` status code during the fetch step.
   - If invalid or unverified, set `Reference / Document URL` to `"NOT FOUND"`.
2. Export validated contract records to `.tmp/contracts_cache.csv` and `data/contracts_cache.csv`.
3. Append/sync validated records to Google Sheets if credentials are configured.

## Outputs
- `.tmp/council_urls.json`: Verified search discovery URL cache.
- `.tmp/contracts_cache.csv` & `data/contracts_cache.csv`: Standardized 20-column contract stream records.
- Google Sheets worksheet sync.
