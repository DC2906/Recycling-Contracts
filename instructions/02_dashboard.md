# Workflow 02: Recycling Contracts Web Dashboard

## Goal
Provide a user-friendly dashboard UI for a 2-5 person team to view, search, filter, and analyze recycling contracts data stored in Google Sheets / CSV.

## Inputs
- Google Sheets data source (or local fallback `.tmp/contracts_cache.csv`).

## Steps
1. Load contract records from Google Sheets API or local cache CSV.
2. Display summary metrics cards:
   - Total Active Contracts
   - Total Contract Value ($)
   - Average Rate ($/tonne)
   - Contracts Expiring within 90 Days
3. Render interactive data table with searching, sorting, and filtering by Council, Material Type, and Status.
4. Highlight contracts approaching expiration.

## Outputs
- Web application (Streamlit or Flask web server).
