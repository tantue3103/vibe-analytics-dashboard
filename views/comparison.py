import streamlit as st
import pandas as pd

st.title("⚖️ A/B Set Comparison")

if len(st.session_state.get('datasets', {})) >= 2:
    datasets = list(st.session_state['datasets'].items())
    
    col1, col2 = st.columns(2)
    with col1:
        dataset1_name = st.selectbox("Select Dataset 1", [d[0] for d in datasets], key="ds1")
    with col2:
        dataset2_name = st.selectbox("Select Dataset 2", [d[0] for d in datasets if d[0] != dataset1_name], key="ds2")
    
    df1 = st.session_state['datasets'][dataset1_name]['data']
    df2 = st.session_state['datasets'][dataset2_name]['data']
    
    st.subheader("Dataset Comparison")
    col1, col2, col3 = st.columns(3)
    col1.metric("Dataset 1 Records", len(df1))
    col2.metric("Dataset 2 Records", len(df2))
    col3.metric("Difference", len(df1) - len(df2))
    
    st.subheader("Column Comparison")
    st.dataframe({
        "Dataset 1 Columns": df1.columns.tolist(),
        "Dataset 2 Columns": df2.columns.tolist()
    }, use_container_width=True)
else:
    st.info("⚠️ Upload at least 2 CSV files to compare datasets")
