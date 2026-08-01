# ♻️ Recycling Contracts Dashboard

An automated tracking system and interactive web dashboard for **124 Local Government Areas (LGAs) in New South Wales (NSW)**, capturing waste management contracts across multiple streams (Kerbside Collection, Dry Recyclables MRF, FOGO Organics, General Waste Disposal).

---

## 📊 Features & Capabilities

- **124 NSW Councils Covered:** Detailed LGA directory including population, total dwellings, and council home website domains.
- **364+ Individual Contract Streams:** Multi-contract breakdown per council (Red, Yellow, and Green bin services).
- **Financial & Volume Metrics:**
  - `Total Contract Value ($)` & `Annual Contract Value ($/year)`
  - `Annual Processed Tonnes (t/year)` based on LGA demographic generation factors
  - `Unique Gate Fees ($/tonne)` calculated per contract based on regional economics & processing facility type
- **Dual Link Transparency:**
  - `Council Home URL`: Direct link to council homepage (`.nsw.gov.au`).
  - `Reference / Document URL`: Link to exact waste strategy, tender notice, MRF processing contract, or contract register page.
- **Interactive Streamlit Dashboard:** Instant search, region filtering, contractor filtering, and 90-day expiry alerts.

---

## 📁 Repository Structure

```
Recycling Contracts/
├── instructions.md           # System behaviour & architecture guide
├── project_specs.md          # Approved project specification
├── config.yaml               # Target sources & sheet settings
├── .env                      # API credentials & keys (environment variables)
├── instructions/             # Workflow step markdown guides
│   ├── 01_scrape_contracts.md
│   └── 02_dashboard.md
├── execution/                # Executable Python scripts
│   ├── 01_scrape_contracts.py  # Council lookup, stream generation & CSV export
│   └── 02_dashboard.py         # Streamlit web dashboard interface
└── .tmp/                     # Structured CSV data storage
    ├── nsw_lgas.csv            # 124 NSW LGA demographic directory
    └── contracts_cache.csv     # 364 multi-stream waste contract records
```

---

## 🚀 Quickstart Guide

### 1. Clone & Install Dependencies

```bash
git clone git@github.com:DC2906/Recycling-Contracts.git
cd Recycling-Contracts

# Create virtual environment & install requirements
uv venv --python 3.12 .venv
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
```

### 2. Generate / Refresh Contract Data

```bash
.\.venv\Scripts\python.exe execution/01_scrape_contracts.py
```

### 3. Launch Local Web Dashboard

```bash
.\.venv\Scripts\python.exe -m streamlit run execution/02_dashboard.py
```

Open **`http://localhost:8501`** in your browser to view the interactive dashboard.

---

## 📜 License

MIT License.
