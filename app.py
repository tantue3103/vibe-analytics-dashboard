import streamlit as st
import pandas as pd
from utils.data import clean_data

# Core App Configurations
st.set_page_config(
    page_title="Enterprise Analytics", 
    page_icon="⚡", 
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom Global CSS for modern dashboard feel
st.markdown("""
<style>
    /* Premium Metric Cards */
    div[data-testid="stMetric"] {
        background-color: var(--secondary-background-color);
        border: 1px solid var(--faded-text-60);
        padding: 5% 5% 5% 10%;
        border-radius: 10px;
        box-shadow: 0 4px 6px rgba(0,0,0,0.05);
    }
    
    /* Typography Overrides */
    h1 {
        font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif;
        font-weight: 800;
        letter-spacing: -0.035em;
        padding-bottom: 0.5rem;
    }
    h2, h3 {
        font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto;
        font-weight: 600;
    }
    
    /* Sidebar Spacing */
    section[data-testid="stSidebar"] {
        padding-top: 1rem;
    }
</style>
""", unsafe_allow_html=True)

# State initialization
if 'datasets' not in st.session_state:
    st.session_state['datasets'] = {}

# Unified Global Sidebar Mapping
with st.sidebar:
    # Optional stream-native logo hook
    st.title("⚡ Data Platform")
    st.divider()
    
    st.header("🎛️ Ingestion Engine")
    
    # Secure data loader mapping
    uploaded_files = st.file_uploader(
        "Target CSV Files", 
        type=["csv"], 
        accept_multiple_files=True,
        help="Upload files formatted with columns: company, industry, address, phone, email."
    )
    
    if uploaded_files:
        current_filenames = [f.name for f in uploaded_files]
        for tf in uploaded_files:
            if tf.name not in st.session_state['datasets']:
                try:
                    df = pd.read_csv(tf)
                    
                    # Core requirements scan
                    required_cols = ['company', 'industry', 'address', 'phone', 'email']
                    df.columns = [str(col).strip().lower() for col in df.columns]
                    missing_cols = [col for col in required_cols if col not in df.columns]
                    
                    if missing_cols:
                        st.error(f"'{tf.name}' missing columns: {', '.join(missing_cols)}")
                    else:
                        clean_df, dropped_count = clean_data(df)
                        st.session_state['datasets'][tf.name] = {
                            'data': clean_df,
                            'dropped': dropped_count
                        }
                        st.toast(f"Synchronized {tf.name} securely!", icon="✅")
                except Exception as e:
                    st.error(f"Data corruption in {tf.name}: {e}")
                    
        # State cleanup if user Xs out a file
        for name in list(st.session_state['datasets'].keys()):
            if name not in current_filenames:
                del st.session_state['datasets'][name]
    else:
        st.session_state['datasets'] = {}
        st.info("Awaiting CSV uploads to activate modules.")

# MPA Router Configuration
pages = {
    "Analytics Suite": [
        st.Page("views/overview.py", title="Overview Dashboard", icon="📊", default=True),
        st.Page("views/comparison.py", title="A/B Set Comparison", icon="⚖️"),
        st.Page("views/data_quality.py", title="Data & DB Export", icon="🛠️"),
    ]
}

pg = st.navigation(pages)
pg.run()
