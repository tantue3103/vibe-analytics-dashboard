import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np

st.title("⚖️ A/B Set Comparison")

# Configure styling
sns.set_style("whitegrid")
plt.rcParams['figure.figsize'] = (12, 5)

if len(st.session_state.get('datasets', {})) >= 2:
    datasets = list(st.session_state['datasets'].items())
    
    col1, col2 = st.columns(2)
    with col1:
        dataset1_name = st.selectbox("Select Dataset 1", [d[0] for d in datasets], key="ds1")
    with col2:
        dataset2_name = st.selectbox("Select Dataset 2", [d[0] for d in datasets if d[0] != dataset1_name], key="ds2")
    
    df1 = st.session_state['datasets'][dataset1_name]['data']
    df2 = st.session_state['datasets'][dataset2_name]['data']
    
    # ==================== METRICS ====================
    st.subheader("📊 Dataset Comparison Metrics")
    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Dataset 1 Records", len(df1))
    col2.metric("Dataset 2 Records", len(df2))
    col3.metric("Record Difference", len(df1) - len(df2))
    col4.metric("Size Ratio", f"{len(df1) / len(df2):.2f}x" if len(df2) > 0 else "N/A")
    
    st.divider()
    
    # ==================== COLUMN COMPARISON ====================
    st.subheader("📋 Column Structure Comparison")
    col1, col2 = st.columns(2)
    with col1:
        st.write("**Dataset 1 Columns:**")
        st.text("\n".join([f"• {col} ({df1[col].dtype})" for col in df1.columns]))
    with col2:
        st.write("**Dataset 2 Columns:**")
        st.text("\n".join([f"• {col} ({df2[col].dtype})" for col in df2.columns]))
    
    st.divider()
    
    # ==================== CHARTS ====================
    st.subheader("📈 Comparative Analysis Charts")
    
    # Tabs for different chart types
    chart_tab1, chart_tab2, chart_tab3, chart_tab4, chart_tab5 = st.tabs(
        ["📊 Bar Chart", "📉 Line Chart", "🥧 Distribution", "🔢 Statistics", "🌡️ Data Profile"]
    )
    
    # ===== BAR CHART =====
    with chart_tab1:
        st.write("**Company Count Comparison**")
        
        fig, ax = plt.subplots(figsize=(12, 5))
        
        # Count companies in each dataset
        count1 = len(df1)
        count2 = len(df2)
        
        categories = [dataset1_name[:20], dataset2_name[:20]]
        values = [count1, count2]
        colors = ['#1f77b4', '#ff7f0e']
        
        bars = ax.bar(categories, values, color=colors, alpha=0.7, edgecolor='black', linewidth=2.5)
        ax.set_ylabel('Number of Companies', fontsize=12, fontweight='bold')
        ax.set_title('Total Companies Count - Comparison', fontsize=14, fontweight='bold')
        ax.grid(axis='y', alpha=0.3)
        
        # Add value labels on bars with percentage
        total = count1 + count2
        for i, bar in enumerate(bars):
            height = bar.get_height()
            percentage = (height / total * 100)
            ax.text(bar.get_x() + bar.get_width()/2., height,
                    f'{int(height)}\n({percentage:.1f}%)', 
                    ha='center', va='bottom', fontweight='bold', fontsize=11)
        
        st.pyplot(fig)
        
        # Show metrics
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("Dataset 1 Companies", count1)
        with col2:
            st.metric("Dataset 2 Companies", count2)
        with col3:
            st.metric("Total Companies", count1 + count2)
    
    # ===== LINE CHART =====
    with chart_tab2:
        st.write("**Company Count by Industry**")
        
        if 'industry' in df1.columns and 'industry' in df2.columns:
            # Get top industries
            top_industries_1 = df1['industry'].value_counts().head(10).index.tolist()
            top_industries_2 = df2['industry'].value_counts().head(10).index.tolist()
            all_industries = sorted(list(set(top_industries_1 + top_industries_2)))
            
            fig, ax = plt.subplots(figsize=(14, 6))
            
            # Count companies by industry for both datasets
            counts1 = [df1[df1['industry'] == ind].shape[0] for ind in all_industries]
            counts2 = [df2[df2['industry'] == ind].shape[0] for ind in all_industries]
            
            x_pos = np.arange(len(all_industries))
            
            ax.plot(x_pos, counts1, marker='o', linewidth=2.5, markersize=10, 
                   label=dataset1_name[:20], color='#1f77b4')
            ax.plot(x_pos, counts2, marker='s', linewidth=2.5, markersize=10, 
                   label=dataset2_name[:20], color='#ff7f0e')
            
            ax.set_xlabel('Industry', fontsize=12, fontweight='bold')
            ax.set_ylabel('Company Count', fontsize=12, fontweight='bold')
            ax.set_title('Company Count by Industry - Comparison', fontsize=14, fontweight='bold')
            ax.set_xticks(x_pos)
            ax.set_xticklabels([ind[:15] for ind in all_industries], rotation=45, ha='right')
            ax.legend(fontsize=11, loc='best')
            ax.grid(True, alpha=0.3)
            
            plt.tight_layout()
            st.pyplot(fig)
            
            # Show industry comparison table
            st.write("**Industry Breakdown**")
            industry_comparison = pd.DataFrame({
                dataset1_name[:20]: [df1[df1['industry'] == ind].shape[0] for ind in all_industries],
                dataset2_name[:20]: [df2[df2['industry'] == ind].shape[0] for ind in all_industries],
                'Difference': [df1[df1['industry'] == ind].shape[0] - df2[df2['industry'] == ind].shape[0] for ind in all_industries]
            }, index=all_industries)
            
            st.dataframe(industry_comparison, use_container_width=True)
        else:
            st.warning("Industry column not found in datasets")
    
    # ===== PIE CHART =====
    with chart_tab3:
        st.write("**Distribution Comparison**")
        
        # Industry distribution if exists
        if 'industry' in df1.columns and 'industry' in df2.columns:
            fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 5))
            
            industry_dist1 = df1['industry'].value_counts().head(8)
            industry_dist2 = df2['industry'].value_counts().head(8)
            
            colors_pie = plt.cm.Set3(np.linspace(0, 1, max(len(industry_dist1), len(industry_dist2))))
            
            ax1.pie(industry_dist1, labels=industry_dist1.index, autopct='%1.1f%%', 
                   colors=colors_pie, startangle=90)
            ax1.set_title(f'{dataset1_name[:20]}\nIndustry Distribution', fontweight='bold')
            
            ax2.pie(industry_dist2, labels=industry_dist2.index, autopct='%1.1f%%', 
                   colors=colors_pie, startangle=90)
            ax2.set_title(f'{dataset2_name[:20]}\nIndustry Distribution', fontweight='bold')
            
            plt.tight_layout()
            st.pyplot(fig)
        else:
            st.info("Industry column not found in both datasets")
    
    # ===== STATISTICS =====
    with chart_tab4:
        st.write("**Statistical Summary**")
        
        numeric_cols_common = list(set(df1.select_dtypes(include=[np.number]).columns) & 
                                   set(df2.select_dtypes(include=[np.number]).columns))
        
        if numeric_cols_common:
            comparison_stats = pd.DataFrame({
                f'{dataset1_name} (Mean)': [df1[col].mean() for col in numeric_cols_common],
                f'{dataset2_name} (Mean)': [df2[col].mean() for col in numeric_cols_common],
                f'{dataset1_name} (Std)': [df1[col].std() for col in numeric_cols_common],
                f'{dataset2_name} (Std)': [df2[col].std() for col in numeric_cols_common]
            }, index=numeric_cols_common)
            
            st.dataframe(comparison_stats.style.highlight_max(axis=0), use_container_width=True)
            
            # Heatmap of correlations
            st.write("**Correlation Heatmap Comparison**")
            col1, col2 = st.columns(2)
            
            with col1:
                fig1, ax1 = plt.subplots(figsize=(8, 6))
                corr1 = df1[numeric_cols_common].corr()
                sns.heatmap(corr1, annot=True, fmt='.2f', cmap='coolwarm', center=0, 
                           ax=ax1, cbar_kws={'label': 'Correlation'})
                ax1.set_title(f'{dataset1_name[:15]} - Correlation Matrix', fontweight='bold')
                st.pyplot(fig1)
            
            with col2:
                fig2, ax2 = plt.subplots(figsize=(8, 6))
                corr2 = df2[numeric_cols_common].corr()
                sns.heatmap(corr2, annot=True, fmt='.2f', cmap='coolwarm', center=0, 
                           ax=ax2, cbar_kws={'label': 'Correlation'})
                ax2.set_title(f'{dataset2_name[:15]} - Correlation Matrix', fontweight='bold')
                st.pyplot(fig2)
        else:
            st.warning("No numeric columns available for statistical analysis")
    
    # ===== DATA PROFILE =====
    with chart_tab5:
        st.write("**Data Quality Profile**")
        
        # Missing values comparison
        fig, ax = plt.subplots(figsize=(12, 5))
        
        missing1 = (df1.isnull().sum() / len(df1) * 100).sort_values(ascending=False).head(10)
        missing2 = (df2.isnull().sum() / len(df2) * 100).sort_values(ascending=False).head(10)
        
        comparison_cols = list(set(missing1.index) | set(missing2.index))
        
        missing1_aligned = pd.Series([missing1.get(col, 0) for col in comparison_cols], index=comparison_cols)
        missing2_aligned = pd.Series([missing2.get(col, 0) for col in comparison_cols], index=comparison_cols)
        
        x = np.arange(len(comparison_cols))
        width = 0.35
        
        ax.bar(x - width/2, missing1_aligned, width, label=dataset1_name[:15], color='#1f77b4', alpha=0.7)
        ax.bar(x + width/2, missing2_aligned, width, label=dataset2_name[:15], color='#ff7f0e', alpha=0.7)
        
        ax.set_xlabel('Columns', fontsize=12, fontweight='bold')
        ax.set_ylabel('Missing Data %', fontsize=12, fontweight='bold')
        ax.set_title('Missing Values Comparison', fontsize=14, fontweight='bold')
        ax.set_xticks(x)
        ax.set_xticklabels([col[:10] for col in comparison_cols], rotation=45)
        ax.legend(fontsize=11)
        ax.grid(axis='y', alpha=0.3)
        
        st.pyplot(fig)
        
        # Data quality metrics
        st.write("**Quality Indicators**")
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.metric(f"{dataset1_name[:15]} Completeness", 
                     f"{(1 - df1.isnull().sum().sum() / (len(df1) * len(df1.columns))) * 100:.1f}%")
        with col2:
            st.metric(f"{dataset2_name[:15]} Completeness", 
                     f"{(1 - df2.isnull().sum().sum() / (len(df2) * len(df2.columns))) * 100:.1f}%")
        with col3:
            st.metric(f"{dataset1_name[:15]} Duplicates", 
                     f"{df1.duplicated().sum()}")
        with col4:
            st.metric(f"{dataset2_name[:15]} Duplicates", 
                     f"{df2.duplicated().sum()}")

else:
    st.info("⚠️ Upload at least 2 CSV files to compare datasets")
