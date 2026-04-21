import pandas as pd

def clean_data(df):
    """
    Clean data by removing rows with missing values in required columns.
    
    Args:
        df (pd.DataFrame): Input dataframe with required columns
        
    Returns:
        tuple: (cleaned_dataframe, dropped_row_count)
    """
    # Make a copy to avoid modifying original
    clean_df = df.copy()
    
    # Record initial count
    initial_count = len(clean_df)
    
    # Remove rows with any missing values in required columns
    required_cols = ['company', 'industry', 'address', 'phone', 'email']
    clean_df = clean_df.dropna(subset=required_cols)
    
    # Calculate dropped count
    dropped_count = initial_count - len(clean_df)
    
    # Strip whitespace from string columns
    string_cols = clean_df.select_dtypes(include=['object']).columns
    for col in string_cols:
        clean_df[col] = clean_df[col].str.strip()
    
    return clean_df, dropped_count
