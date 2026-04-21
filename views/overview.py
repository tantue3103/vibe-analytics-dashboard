import streamlit as st
import pandas as pd

st.title("📊 Overview Dashboard")

if st.session_state.get('datasets'):
    st.header("Dataset Summary")
    
    for dataset_name, dataset_info in st.session_state['datasets'].items():
        with st.container(border=True):
            st.subheader(f"{dataset_name}")
            df = dataset_info['data']
            dropped = dataset_info['dropped']
            
            col1, col2, col3 = st.columns(3)
            col1.metric("Total Records", len(df))
            col2.metric("Dropped Rows", dropped)
            col3.metric("Data Quality", f"{(len(df) / (len(df) + dropped) * 100):.1f}%" if (len(df) + dropped) > 0 else "0%")
            
            st.dataframe(df.head(10), use_container_width=True)
else:
    st.info("📤 Upload CSV files from the sidebar to view analytics")
