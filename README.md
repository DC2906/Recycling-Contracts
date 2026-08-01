# ♻️ NSW Council Waste & Recycling Contracts Dashboard

An automated tracking system and interactive web dashboard for **124 Local Government Areas (LGAs) in New South Wales (NSW)**, capturing waste management contracts across multiple streams (Kerbside Collection, Dry Recyclables MRF, FOGO Organics, General Waste Disposal).

---

## 🌐 Web Server & Cloud Deployment

This repository is pre-configured for instant 1-click cloud deployment on **Streamlit Community Cloud**, **Render**, **Railway**, **Hugging Face Spaces**, or **Heroku**.

### Option A: Streamlit Community Cloud (Recommended Free Hosting)
1. Go to [share.streamlit.io](https://share.streamlit.io)
2. Connect your GitHub account and select repository: `DC2906/Recycling-Contracts`
3. Set **Main file path** to: `app.py`
4. Click **Deploy!**

### Option B: Render / Railway / Heroku
- Uses the included [`Procfile`](Procfile) (`web: streamlit run app.py`).
- Automatic port binding via `$PORT`.

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
- **Interactive Dashboard UI:** Search, region filtering, stream filtering, contractor filtering, and 90-day expiry alerts.

---

## 📁 Repository Structure

```
Recycling Contracts/
├── app.py                     <-- Web Server Root Entrypoint (for Cloud Deployment)
├── README.md                  # Project overview & Cloud deployment guide
├── requirements.txt           # Python dependencies
├── Procfile                   # Web server process file (Render / Railway)
├── config.yaml                # Configuration settings
├── .streamlit/
│   └── config.toml            # Streamlit server configuration
├── data/                      # Tracked Production Data Directory
│   ├── nsw_lgas.csv           # 124 NSW LGA demographic directory
│   └── contracts_cache.csv    # 364 multi-stream waste contract records
├── instructions/              # Workflow step markdown guides
│   ├── 01_scrape_contracts.md
│   └── 02_dashboard.md
└── execution/                 # Executable Python scripts
    ├── 01_scrape_contracts.py # Ingestion & dataset builder
    └── 02_dashboard.py        # Streamlit web dashboard interface
```

---

## 🚀 Local Running Instructions

```bash
# 1. Clone Repository
git clone https://github.com/DC2906/Recycling-Contracts.git
cd Recycling-Contracts

# 2. Install Dependencies
pip install -r requirements.txt

# 3. Generate / Refresh Data (Optional)
python execution/01_scrape_contracts.py

# 4. Run Dashboard Server
streamlit run app.py
```

---

## 📜 License

MIT License.
