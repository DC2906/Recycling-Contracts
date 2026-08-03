import os
import datetime
import pandas as pd
import streamlit as st
from dotenv import load_dotenv

load_dotenv()

DATA_PATH = "data/contracts_cache.csv"
TMP_PATH = ".tmp/contracts_cache.csv"

st.set_page_config(
    page_title="NSW Council Waste & Recycling Contracts Register",
    page_icon="♻️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom Styling
st.markdown("""
    <style>
    .main-header {
        font-size: 2.2rem;
        font-weight: 700;
        color: #0F172A;
        margin-bottom: 0.2rem;
    }
    .sub-header {
        font-size: 1.05rem;
        color: #475569;
        margin-bottom: 1.5rem;
    }
    .stMetric {
        background-color: #F8FAFC;
        border: 1px solid #E2E8F0;
        padding: 1rem;
        border-radius: 10px;
    }
    </style>
""", unsafe_allow_html=True)

@st.cache_data(ttl=60)
def load_data():
    target = DATA_PATH if os.path.exists(DATA_PATH) else (TMP_PATH if os.path.exists(TMP_PATH) else None)
    if target:
        df = pd.read_csv(target)

        df["Contract Start Date"] = pd.to_datetime(df["Contract Start Date"], errors="coerce")
        df["Contract End Date"] = pd.to_datetime(df["Contract End Date"], errors="coerce")
        df["Total Contract Value ($)"] = pd.to_numeric(df["Total Contract Value ($)"], errors="coerce").fillna(0)
        df["Annual Contract Value ($/year)"] = pd.to_numeric(df["Annual Contract Value ($/year)"], errors="coerce").fillna(0)
        df["Annual Tonnes (t/year)"] = pd.to_numeric(df["Annual Tonnes (t/year)"], errors="coerce").fillna(0).astype(int)
        df["Gate Fee / Rate ($/tonne)"] = pd.to_numeric(df["Gate Fee / Rate ($/tonne)"], errors="coerce").fillna(0)
        df["Population"] = pd.to_numeric(df["Population"], errors="coerce").fillna(0).astype(int)
        df["Total Dwellings"] = pd.to_numeric(df["Total Dwellings"], errors="coerce").fillna(0).astype(int)
        return df
    else:
        return pd.DataFrame()

def main():
    st.markdown('<div class="main-header">♻️ NSW Council Waste & Recycling Contracts Register</div>', unsafe_allow_html=True)
    st.markdown('<div class="sub-header">Annual Contract Values ($/yr), Annual Processed Tonnes (t/yr), Unique Gate Fees & Document URLs across 124 NSW Councils</div>', unsafe_allow_html=True)

    df = load_data()

    if df.empty:
        st.warning("No contract data found. Please run `python execution/01_scrape_contracts.py` first.")
        st.stop()

    today = pd.to_datetime(datetime.date.today())
    df["Days Remaining"] = (df["Contract End Date"] - today).dt.days
    df["Expiry Alert"] = df["Days Remaining"].apply(
        lambda x: "⚠️ Expiring Soon (<90d)" if 0 <= x <= 90 else ("❌ Expired" if x < 0 else "✅ Active")
    )

    # Sidebar Filters
    st.sidebar.header("🔍 Search & Filters")
    
    search_query = st.sidebar.text_input("Search Council / Provider / Stream", "").strip().lower()

    regions = ["All Regions"] + sorted(list(df["Region"].dropna().unique()))
    selected_region = st.sidebar.selectbox("Region Group", regions)

    streams = ["All Contract Streams"] + sorted(list(df["Contract Stream"].dropna().unique()))
    selected_stream = st.sidebar.selectbox("Contract Stream / Category", streams)

    contractors = ["All Contractors"] + sorted(list(df["Contractor / Service Provider"].dropna().unique()))
    selected_contractor = st.sidebar.selectbox("Service Provider / Contractor", contractors)

    statuses = ["All Statuses"] + sorted(list(df["Status"].dropna().unique()))
    selected_status = st.sidebar.selectbox("Contract Status", statuses)

    # Filter Application
    filtered_df = df.copy()
    
    if search_query:
        filtered_df = filtered_df[
            filtered_df["Council / Business Name"].str.lower().str.contains(search_query) |
            filtered_df["Contractor / Service Provider"].str.lower().str.contains(search_query) |
            filtered_df["Contract Stream"].str.lower().str.contains(search_query)
        ]
        
    if selected_region != "All Regions":
        filtered_df = filtered_df[filtered_df["Region"] == selected_region]
        
    if selected_stream != "All Contract Streams":
        filtered_df = filtered_df[filtered_df["Contract Stream"] == selected_stream]

    if selected_contractor != "All Contractors":
        filtered_df = filtered_df[filtered_df["Contractor / Service Provider"] == selected_contractor]
        
    if selected_status != "All Statuses":
        filtered_df = filtered_df[filtered_df["Status"] == selected_status]

    # Metrics Section
    m1, m2, m3, m4, m5 = st.columns(5)

    unique_councils = filtered_df["Council / Business Name"].nunique()
    total_records = len(filtered_df)
    total_ann_val = filtered_df["Annual Contract Value ($/year)"].sum()
    total_ann_tonnes = filtered_df["Annual Tonnes (t/year)"].sum()
    avg_gate_fee = filtered_df["Gate Fee / Rate ($/tonne)"].mean() if not filtered_df.empty else 0
    expiring_count = len(filtered_df[filtered_df["Days Remaining"].between(0, 90)])

    with m1:
        st.metric("Total Councils", f"{unique_councils}")
    with m2:
        st.metric("Annual Portfolio Value", f"${total_ann_val:,.2f}/yr")
    with m3:
        st.metric("Annual Tonnes Processed", f"{total_ann_tonnes:,} t/yr")
    with m4:
        st.metric("Avg Gate Fee", f"${avg_gate_fee:,.2f}/t")
    with m5:
        st.metric("Expiring Soon (<90d)", f"{expiring_count}")

    st.markdown("---")

    # Interactive Data Table
    st.subheader(f"📋 Master Contracts Register ({total_records} Contract Streams across {unique_councils} Councils)")

    display_df = filtered_df.copy()
    display_df["Population"] = display_df["Population"].apply(lambda x: f"{x:,}")
    display_df["Total Dwellings"] = display_df["Total Dwellings"].apply(lambda x: f"{x:,}")
    display_df["Start Date"] = display_df["Contract Start Date"].dt.strftime("%Y-%m-%d")
    display_df["End Date"] = display_df["Contract End Date"].dt.strftime("%Y-%m-%d")
    display_df["Term"] = display_df["Contract Term (Years)"].apply(lambda x: f"{x:.1f} yrs")
    display_df["Total Value ($)"] = display_df["Total Contract Value ($)"].apply(lambda x: f"${x:,.2f}")
    display_df["Annual Value ($/yr)"] = display_df["Annual Contract Value ($/year)"].apply(lambda x: f"${x:,.2f}")
    display_df["Annual Tonnes (t/yr)"] = display_df["Annual Tonnes (t/year)"].apply(lambda x: f"{x:,} t")
    display_df["Gate Fee ($/t)"] = display_df["Gate Fee / Rate ($/tonne)"].apply(lambda x: f"${x:,.2f}")

    cols = [
        "Contract ID",
        "Council / Business Name",
        "Region",
        "Population",
        "Total Dwellings",
        "Contract Stream",
        "Contractor / Service Provider",
        "Term",
        "Total Value ($)",
        "Annual Value ($/yr)",
        "Annual Tonnes (t/yr)",
        "Gate Fee ($/t)",
        "Start Date",
        "End Date",
        "Expiry Alert",
        "Council Home URL",
        "Reference / Document URL",
        "Notes"
    ]

    st.dataframe(
        display_df[cols],
        column_config={
            "Council Home URL": st.column_config.LinkColumn(
                "Council Home URL"
            ),
            "Reference / Document URL": st.column_config.LinkColumn(
                "Reference / Document URL"
            )
        },
        use_container_width=True,
        hide_index=True
    )

    # Expiry Warning Section
    exp_df = filtered_df[filtered_df["Days Remaining"].between(0, 90)]
    if not exp_df.empty:
        st.warning(f"⚠️ **Attention Needed:** {len(exp_df)} contract stream(s) are approaching expiry in the next 90 days.")
        for _, r in exp_df.iterrows():
            st.info(f"📍 **{r['Council / Business Name']}** — Stream: *{r['Contract Stream']}* | Contractor: **{r['Contractor / Service Provider']}** | Gate Fee: **${r['Gate Fee / Rate ($/tonne)']:,.2f}/t** | Annual Tonnes: **{r['Annual Tonnes (t/year)']:,} t/yr**")

if __name__ == "__main__":
    main()
