#!/usr/bin/env python3
"""
FAA NOTAM Search Dashboard (Simplified)
Features:
1. Single Search: Quick check for one airport.
2. Batch Search: Edit a list of airports/criteria and run them all at once.
"""

import streamlit as st
from faa_notam_lib import FAAClient
import pandas as pd
from datetime import datetime
import html
import re
import io

# =============================================================================
# CONFIG & CLIENT
# =============================================================================

# =============================================================================
# CONFIG & CLIENT
# =============================================================================

@st.cache_resource
def get_client():
    # Load credentials from secrets
    try:
        c_id = st.secrets["FAA_ID"]
        c_secret = st.secrets["FAA_SECRET"]
        return FAAClient(c_id, c_secret)
    except Exception as e:
        st.error(f"Missing API Credentials in .streamlit/secrets.toml: {e}")
        return None

client = get_client()

if not client:
    st.stop()

st.set_page_config(
    page_title="FAA NOTAM Search",
    page_icon="✈️",
    layout="wide"
)

# Custom minimal styling
st.markdown("""
    <style>
    .block-container { padding-top: 2rem; }
    /* Hide the index column in dataframes and data editors */
    [data-testid="stDataFrame"] th:first-child, 
    [data-testid="stDataFrame"] td:first-child,
    [data-testid="stDataEditor"] th:first-child,
    [data-testid="stDataEditor"] td:first-child,
    [data-testid="stDataEditor"] .row-header {
        display: none !important;
    }
    /* Targeted hide for the row numbering in data editor */
    [data-testid="stDataEditor"] div[role="gridcell"]:first-child {
        display: none !important;
    }
    </style>
""", unsafe_allow_html=True)

# Initialize Session State for the table data
if 'batch_df' not in st.session_state:
    st.session_state.batch_df = pd.DataFrame(columns=['FIR/AIRPORT', 'Type', 'Keyword'])

# =============================================================================
# HELPER FUNCTIONS
# =============================================================================

def render_notam_list(notams):
    """Render NOTAMs in a 2-column grid using Full ICAO text."""
    if not notams:
        return

    # Grid Layout: 2 NOTAMs per row
    for i in range(0, len(notams), 2):
        cols = st.columns(2)
        
        # First column
        with cols[0]:
            n = notams[i]
            # Use Filtered/Full ICAO text if available, else raw
            content = n.get('full_icao') or n.get('text', '')
            
            st.markdown(f"**#{n.get('id', 'N/A')}** | {n.get('start', '')[:16]} -> {n.get('end', '')[:16]}")
            st.text(html.unescape(content)) # Use st.text for monospaced ICAO look or st.info
            
        # Second column (if exists)
        if i + 1 < len(notams):
            with cols[1]:
                n = notams[i+1]
                content = n.get('full_icao') or n.get('text', '')
                
                st.markdown(f"**#{n.get('id', 'N/A')}** | {n.get('start', '')[:16]} -> {n.get('end', '')[:16]}")
                st.text(html.unescape(content))
        
        st.divider()

# =============================================================================
# MAIN APP
# =============================================================================

st.title("✈️ FAA NOTAM Search")

# Swap Tabs: Batch Search First
tabs = st.tabs(["📋 Batch Search", "🔍 Single Search"])

# -----------------------------------------------------------------------------
# TAB 1: BATCH SEARCH (Merged Monitor + Profile) -> Now Default
# -----------------------------------------------------------------------------
with tabs[0]:
    st.markdown("### Batch Search Manager")
    
    # Callback for CSV Upload
    def load_csv_data():
        uploaded_file = st.session_state.csv_uploader
        if uploaded_file:
            try:
                df = pd.read_csv(uploaded_file)
                required = ['FIR/AIRPORT', 'Type', 'Keyword']
                if all(c in df.columns for c in required):
                    st.session_state.batch_df = df
                    # Reset search state on new file load
                    st.session_state.show_batch_results = False
                    st.session_state.batch_cache = {}
                    st.toast("CSV Loaded Successfully!", icon="✅")
                else:
                    st.toast("Invalid CSV format. Columns must be: FIR/AIRPORT, Type, Keyword", icon="❌")
            except Exception as e:
                st.toast(f"Error reading file: {e}", icon="❌")

    st.caption("1. Upload or Edit your list below.  2. Click 'Run Batch Search'.")
    
    # 1. File Upload (Loads into Session State)
    with st.expander("📂 Import CSV List", expanded=False):
        st.file_uploader("Choose CSV", type=['csv'], label_visibility="collapsed", 
                         key="csv_uploader", on_change=load_csv_data)

    # 2. Data Editor (The Source of Truth)
    col_config = {
        "FIR/AIRPORT": st.column_config.TextColumn(required=True, max_chars=4, width="small"),
        "Type": st.column_config.SelectboxColumn(options=["Runway", "Keyword"], width="small", required=True),
        "Keyword": st.column_config.TextColumn(width="medium", help="Leave blank for All")
    }
    
    edited_df = st.data_editor(
        st.session_state.batch_df, 
        num_rows="dynamic",
        column_config=col_config,
        column_order=["FIR/AIRPORT", "Type", "Keyword"],
        hide_index=True,
        use_container_width=True,
        key="batch_editor_main"
    )
    
    # 3. Action Buttons
    c1, c2, c3, c4, c5 = st.columns([1, 1, 1, 1, 3])
    with c1:
        run_batch = st.button("▶️ Run Batch Search", type="primary")
    with c2:
        csv_data = edited_df.to_csv(index=False).encode('utf-8')
        st.download_button("💾 Export CSV", csv_data, "my_search_list.csv", "text/csv")
        
    # Expand/Collapse Controls moved up
    with c3:
        if st.button("➕ Expand All"):
            st.session_state.batch_expander_state = True
            st.rerun()
    with c4:
        if st.button("➖ Collapse All"):
            st.session_state.batch_expander_state = False
            st.rerun()

    # Init state for results visibility
    if 'show_batch_results' not in st.session_state:
        st.session_state.show_batch_results = False
    if 'batch_expander_state' not in st.session_state:
        st.session_state.batch_expander_state = None 
    if 'batch_cache' not in st.session_state:
        st.session_state.batch_cache = {}

    # 4. Processing Logic Trigger (Fetch & Cache)
    if run_batch:
        if edited_df.empty:
            st.warning("Please add at least one airport to the list.")
        else:
            st.session_state.show_batch_results = True
            st.session_state.batch_expander_state = None 
            
            # Standardize & Clean
            clean_df = edited_df.copy()
            clean_df['FIR/AIRPORT'] = clean_df['FIR/AIRPORT'].astype(str).str.upper().str.strip()
            clean_df['Keyword'] = clean_df['Keyword'].fillna("").astype(str).str.strip().str.upper()
            
            # Persist clean data with reset index to prevent ID column from appearing
            st.session_state.batch_df = clean_df.reset_index(drop=True)
            
            # --- PERFORM FETCH HERE (ONCE) ---
            run_df = clean_df[clean_df['FIR/AIRPORT'].str.len() == 4]
            if run_df.empty:
                st.warning("No valid 4-letter ICAO codes found.")
                st.session_state.batch_cache = {}
            else:
                unique_locs = run_df['FIR/AIRPORT'].unique()
                new_cache = {}
                
                # Progress Bar
                progress_text = "Fetching data from FAA..."
                bar = st.progress(0, text=progress_text)
                
                for i, loc in enumerate(unique_locs):
                    bar.progress((i + 1) / len(unique_locs), text=f"Fetching {loc}...")
                    try:
                        new_cache[loc] = client.search_notams(loc, search_type="all")
                    except Exception:
                        new_cache[loc] = []
                
                bar.empty()
                st.session_state.batch_cache = new_cache
            
            st.rerun()

    # 5. Render Results (From Cache)
    if st.session_state.show_batch_results:
        st.divider()
        st.subheader("Results")
        
        # Use Cached Data
        current_df = st.session_state.batch_df
        # Re-filter just in case
        run_df = current_df[current_df['FIR/AIRPORT'].str.len() == 4]
        notam_cache = st.session_state.batch_cache
        
        if not notam_cache:
            st.info("No data cached. Please run search.")
        else:
            for idx, row in run_df.iterrows():
                loc = row['FIR/AIRPORT']
                rtype = row['Type'].lower()
                
                # SAFE CAST to string to prevent 'float' error
                val = row['Keyword']
                k_raw = str(val) if pd.notna(val) else ""
                
                all_notams = notam_cache.get(loc, [])
                
                keywords = [k.strip() for k in k_raw.split('|') if k.strip()]
                if not keywords: keywords = [""]
                
                row_label = f"Row {idx+1}: {loc} - {row['Type']} {f'({k_raw})' if k_raw else '(All)'}"
                
                matches = []
                for k in keywords:
                    k_upper = k.upper()
                    for n in all_notams:
                        text_blob = f"{n['text']} {n['full_icao']}".upper()
                        is_match = False
                        if rtype == 'runway':
                            if "RWY" in text_blob or "RUNWAY" in text_blob:
                                if re.search(r"(?<!\d)" + re.escape(k_upper) + r"(?![0-9])", text_blob):
                                    is_match = True
                        else:
                            if not k: is_match = True
                            elif k_upper in text_blob: is_match = True
                        
                        if is_match:
                            if n not in matches:
                                matches.append(n)
                
                count = len(matches)
                icon = "🔴" if count > 0 else "🟢"
                
                # Default: Collapsed (False)
                exp_state = False
                # Override if user clicked buttons
                if st.session_state.batch_expander_state is not None:
                    exp_state = st.session_state.batch_expander_state
                
                with st.expander(f"{icon} {row_label} ({count} found)", expanded=exp_state):
                    if matches:
                        render_notam_list(matches)
                    else:
                        st.caption("No matches found.")
        
        # We don't show success message at bottom anymore to avoid clutter, 
        # result presence is enough.


# -----------------------------------------------------------------------------
# TAB 2: SINGLE SEARCH -> Now Second
# -----------------------------------------------------------------------------
with tabs[1]:
    st.markdown("### Quick Search")
    
    # Adjust Ratio to make input box narrower (1 vs 4)
    col1, col2 = st.columns([1, 4])
    with col1:
        s_loc = st.text_input("Airport / FIR", "KJFK", max_chars=4).upper()
        s_type = st.radio("Search Type", ["All NOTAMs", "Runway", "Keyword"])
        
        s_query = ""
        s_regex = False
        
        if s_type == "Runway":
            s_query = st.text_input("Runway (e.g. 04R)", "04R")
        elif s_type == "Keyword":
            s_query = st.text_input("Keyword", "CRANE")
            s_regex = st.checkbox("Regex Pattern", value=False)
            
        btn_search = st.button("🔎 Search Now", type="primary")

    with col2:
        if btn_search:
            if len(s_loc) != 4:
                st.error("Please enter a valid 4-letter ICAO code.")
            else:
                with st.spinner(f"Searching {s_loc}..."):
                    try:
                        api_type = "all"
                        if s_type == "Runway": api_type = "runway"
                        elif s_type == "Keyword": api_type = "keyword"
                        
                        results = client.search_notams(
                            s_loc, 
                            query=s_query, 
                            search_type=api_type, 
                            is_regex=s_regex
                        )
                        
                        st.subheader(f"Results: {len(results)} NOTAMs")
                        
                        if results:
                            render_notam_list(results)
                        else:
                            st.info("No active NOTAMs found matching criteria.")
                            
                    except Exception as e:
                        st.error(f"Error: {e}")
