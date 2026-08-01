# Workflow 01: Scrape NSW Council Recycling & Waste Contracts

## Goal
Automate looking up official websites for all 124 NSW Councils, searching for waste strategies, contract registers, tenders, and service providers to extract individual contract streams (Kerbside Collection, Dry Recyclables MRF, FOGO Organics, General Waste Disposal, Hard Waste) with estimated contract values and gate fees.

## Inputs
- List of 124 NSW LGAs (from Google Sheet / `.tmp/nsw_lgas.csv`).
- `config.yaml`: Scraping parameters, search settings, and target keywords.
- `.env`: Environment credentials (`GOOGLE_SERVICE_ACCOUNT_FILE`, `SPREADSHEET_ID`).

## Steps
1. Load the 124 NSW LGAs list with population & dwelling counts.
2. For each council, expand into multiple distinct contract stream records:
   - **Kerbside Collection** (Red, Yellow, Green Bin Pickup)
   - **Dry Recyclables Processing (MRF)** (Yellow Bin - Paper, Cardboard, Glass, Plastics)
   - **FOGO / Organics Processing** (Green Bin - Food & Garden Organics)
   - **General Waste Disposal & Transfer** (Red Bin)
   - **Hard Waste & Bulky Goods Collection**
3. Extract and calculate detailed fields for each contract stream:
   - `Contract ID`
   - `Council / Business Name`
   - `Region`
   - `Population` (Dedicated Column)
   - `Total Dwellings` (Dedicated Column)
   - `Contract Stream`
   - `Contractor / Service Provider`
   - `Contract Start Date` & `Contract End Date`
   - `Contract Term (Years)`
   - `Total Contract Value ($)`
   - `Annual Contract Value ($/year)`
   - `Annual Tonnes (t/year)`
   - `Gate Fee / Rate ($/tonne)` (Unique per individual contract based on regional economics & facility type)
   - `Status`
   - `Contact Person / Department`
   - `Council Home URL` (Original Home Website)
   - `Reference / Document URL` (Exact Waste Strategy / Tender / Contract Register Page)
   - `Notes`


4. Standardize and validate extracted records.
5. Store in `.tmp/contracts_cache.csv` and sync to Google Sheets.

## Outputs
- Structured CSV files: `.tmp/nsw_lgas.csv` and `.tmp/contracts_cache.csv` (300+ detailed contract records).
- Updated Google Sheets worksheet.


