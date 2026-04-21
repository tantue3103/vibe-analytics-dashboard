import streamlit as st
import pandas as pd
import io

@st.cache_data
def clean_data(df):
    """
    Data cleaning pipeline optimized for Streamlit Cloud and large datasets.
    Implements memory downcasting for categorical data and robust string cleaning.
    """
    initial_count = len(df)
    
    # 1. Normalize columns safely
    df.columns = [str(col).strip().lower() for col in df.columns]
    
    # 2. Trim spaces for all string columns and handle empty strings
    for col in df.columns:
        if df[col].dtype == 'object':
            df[col] = df[col].str.strip()
            
    # 3. Remove duplicates based on company identifier safely
    if 'company' in df.columns:
        df = df.drop_duplicates(subset=['company'])
    dropped_count = initial_count - len(df)
    
    # 4. Normalize industry formats and optimize memory
    if 'industry' in df.columns:
        df['industry'] = df['industry'].str.title()
        # Memory optimization: Convert categorical low-cardinality fields
        unique_thresh = df['industry'].nunique() / len(df) if len(df) > 0 else 1
        if unique_thresh < 0.5:  # If fewer than 50% are completely unique
            df['industry'] = df['industry'].astype('category')
            
    return df, dropped_count

def generate_csv_bytes(df):
    """Encodes a DataFrame into a rapid CSV buffer array for browser downloading."""
    output = io.BytesIO()
    df.to_csv(output, index=False)
    return output.getvalue()
