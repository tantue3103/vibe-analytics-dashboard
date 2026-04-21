import streamlit as st
import pandas as pd

st.title("🛠️ Data & DB Export")

if st.session_state.get('datasets'):
    st.header("Data Quality Report")
    
    for dataset_name, dataset_info in st.session_state['datasets'].items():
        with st.container(border=True):
            st.subheader(f"{dataset_name}")
            df = dataset_info['data']
            
            # Data quality metrics
            col1, col2, col3 = st.columns(3)
            col1.metric("Missing Values", df.isnull().sum().sum())
            col2.metric("Duplicate Rows", df.duplicated().sum())
            col3.metric("Completeness", f"{(1 - df.isnull().sum().sum() / (len(df) * len(df.columns))) * 100:.1f}%")
            
            st.subheader("Column Quality")
            quality_df = pd.DataFrame({
                'Column': df.columns,
                'Type': df.dtypes.values,
                'Missing': [df[col].isnull().sum() for col in df.columns],
                'Unique': [df[col].nunique() for col in df.columns]
            })
            st.dataframe(quality_df, use_container_width=True)
            
            # Export option
            csv = df.to_csv(index=False)
            st.download_button(
                label=f"Download {dataset_name} as CSV",
                data=csv,
                file_name=f"{dataset_name}.csv",
                mime="text/csv"
            )
else:
    st.info("📤 Upload CSV files from the sidebar to view quality metrics")
