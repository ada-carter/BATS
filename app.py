import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import numpy as np
import datetime

st.set_page_config(page_title="BATS Dashboard", layout="wide")
st.title("BATS Dashboard")

# -----------------------------
# Temperature Profiles Plot
# -----------------------------
try:
    # Read the CSV file for temperature profiles
    df_profiles_raw = pd.read_csv("data/BATS_temperature_profiles.csv")
    
    # Process the data to handle the specific format of this CSV
    # Extract Profile 1 data (first two columns)
    profile1_depth = df_profiles_raw.iloc[2:, 0].reset_index(drop=True)
    profile1_temp = df_profiles_raw.iloc[2:, 1].reset_index(drop=True)
    
    # Extract Profile 2 data (columns 3 and 4)
    profile2_depth = df_profiles_raw.iloc[2:, 3].reset_index(drop=True)
    profile2_temp = df_profiles_raw.iloc[2:, 4].reset_index(drop=True)
    
    # Create clean dataframes for each profile
    df_profile1 = pd.DataFrame({
        'depth': profile1_depth,
        'temperature': profile1_temp
    })
    
    df_profile2 = pd.DataFrame({
        'depth': profile2_depth,
        'temperature': profile2_temp
    })
    
    # Clean and convert the data
    for df in [df_profile1, df_profile2]:
        # Convert to string first to handle any potential mixed types
        for col in df.columns:
            df[col] = df[col].astype(str)
        
        # Remove any non-numeric characters except decimal points and negative signs
        for col in df.columns:
            df[col] = df[col].str.replace(r'[^0-9.-]', '', regex=True)
            # Replace empty strings with NaN
            df[col] = df[col].replace('', np.nan)
            df[col] = df[col].replace('-', np.nan)  # Solo hyphens aren't valid numbers
            df[col] = df[col].replace('.', np.nan)  # Solo periods aren't valid numbers
        
        # Convert to numeric values
        for col in df.columns:
            df[col] = pd.to_numeric(df[col], errors='coerce')
        
        # Drop rows with missing values
        df.dropna(inplace=True)
    
    # Create a more compact layout with columns
    col1, col2, col3 = st.columns([1, 1, 1])
    
    # Combined profiles plot (middle column)
    with col2:
        st.subheader("Combined Temperature Profiles")
        fig_combined = go.Figure()
        
        fig_combined.add_trace(go.Scatter(
            x=df_profile1['temperature'],
            y=df_profile1['depth'],
            mode='lines',
            name="Profile 1"
        ))
        
        fig_combined.add_trace(go.Scatter(
            x=df_profile2['temperature'],
            y=df_profile2['depth'],
            mode='lines',
            name="Profile 2"
        ))
        
        fig_combined.update_layout(
            xaxis_title="Temperature (°C)",
            yaxis_title="Depth (m)",
            yaxis=dict(autorange="reversed", range=[0, 250]),
            template="plotly_white",
            height=400,
            margin=dict(l=40, r=20, t=10, b=40),
            legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1)
        )
        
        st.plotly_chart(fig_combined, use_container_width=True)
    
    # Individual profile 1 (left column)
    with col1:
        st.subheader("Profile 1")
        fig_profile1 = go.Figure()
        
        fig_profile1.add_trace(go.Scatter(
            x=df_profile1['temperature'],
            y=df_profile1['depth'],
            mode='lines+markers',
            marker=dict(size=4),
            line=dict(color='blue'),
            name="Profile 1"
        ))
        
        fig_profile1.update_layout(
            xaxis_title="Temperature (°C)",
            yaxis_title="Depth (m)",
            yaxis=dict(autorange="reversed", range=[0, 250]),
            template="plotly_white",
            height=400,
            margin=dict(l=40, r=20, t=10, b=40),
            showlegend=False
        )
        
        st.plotly_chart(fig_profile1, use_container_width=True)
    
    # Individual profile 2 (right column)
    with col3:
        st.subheader("Profile 2")
        fig_profile2 = go.Figure()
        
        fig_profile2.add_trace(go.Scatter(
            x=df_profile2['temperature'],
            y=df_profile2['depth'],
            mode='lines+markers',
            marker=dict(size=4),
            line=dict(color='red'),
            name="Profile 2"
        ))
        
        fig_profile2.update_layout(
            xaxis_title="Temperature (°C)",
            yaxis_title="Depth (m)",
            yaxis=dict(autorange="reversed", range=[0, 250]),
            template="plotly_white",
            height=400,
            margin=dict(l=40, r=20, t=10, b=40),
            showlegend=False
        )
        
        st.plotly_chart(fig_profile2, use_container_width=True)
    
    # Add a data display section in an expander to keep the layout compact
    with st.expander("View Raw Temperature Profile Data"):
        tab1, tab2 = st.tabs(["Profile 1", "Profile 2"])
        with tab1:
            st.dataframe(df_profile1.head(20))
        with tab2:
            st.dataframe(df_profile2.head(20))

except Exception as e:
    st.error(f"Error processing temperature profiles data: {str(e)}")
    st.write("Detailed error information:", e)

# -----------------------------
# Sea Surface Temperature (SST) Plot
# -----------------------------
try:
    # Read the CSV file for SST data with encoding='latin1' to fix Unicode error
    df_sst_raw = pd.read_csv("data/OCN330_BATS_SST.csv", encoding='latin1')
    
    # Extract and clean the data
    df_sst = df_sst_raw.copy()
    
    # Define column names based on the first row
    date_col = df_sst.columns[0]  # 'Days since September 1'
    sst_col = df_sst.columns[1]   # 'Observed SST'
    
    # Clean the data
    # 1. Convert to string first to handle any potential mixed types
    for col in [date_col, sst_col]:
        df_sst[col] = df_sst[col].astype(str)
    
    # 2. Remove any non-numeric characters except decimal points and negative signs
    for col in [date_col, sst_col]:
        df_sst[col] = df_sst[col].str.replace(r'[^0-9.-]', '', regex=True)
        # Replace empty strings with NaN
        df_sst[col] = df_sst[col].replace('', np.nan)
        df_sst[col] = df_sst[col].replace('-', np.nan)  # Solo hyphens aren't valid numbers
        df_sst[col] = df_sst[col].replace('.', np.nan)  # Solo periods aren't valid numbers
    
    # 3. Convert to numeric values
    for col in [date_col, sst_col]:
        df_sst[col] = pd.to_numeric(df_sst[col], errors='coerce')
    
    # 4. Drop rows with missing values
    df_sst = df_sst.dropna(subset=[date_col, sst_col])
    
    # 5. Convert days since September 1 to actual dates
    # Assuming the current year for September 1st
    current_year = datetime.datetime.now().year - 1  # Use previous year for complete annual cycle 
    start_date = datetime.datetime(current_year, 9, 1)
    df_sst['Date'] = df_sst[date_col].apply(lambda x: start_date + datetime.timedelta(days=int(x)))
    
    # Identify the three temperature sections
    # Define boundaries for the three sections based on days since September 1
    section1_end = 120  # Approximately December
    section2_end = 240  # Approximately April
    
    # Add a section column to the dataframe
    conditions = [
        (df_sst[date_col] <= section1_end),
        (df_sst[date_col] > section1_end) & (df_sst[date_col] <= section2_end),
        (df_sst[date_col] > section2_end)
    ]
    choices = ['Fall', 'Winter', 'Spring/Summer']
    df_sst['Season'] = np.select(conditions, choices, default='Unknown')
    
    # Create the SST plot with a more compact design and three sections
    st.subheader("Seasonal Evolution of Sea Surface Temperature")
    
    # Create a base figure
    fig_sst = go.Figure()
    
    # Define season colors for both lines and backgrounds
    season_colors = {
        'Fall': {'line': 'orange', 'fill': 'rgba(255, 165, 0, 0.2)'},  # Light orange background
        'Winter': {'line': 'blue', 'fill': 'rgba(173, 216, 230, 0.2)'},  # Light blue background
        'Spring/Summer': {'line': 'green', 'fill': 'rgba(144, 238, 144, 0.2)'}  # Light green background
    }
    
    # Add a background highlight for each season
    for season, colors in season_colors.items():
        season_data = df_sst[df_sst['Season'] == season]
        if not season_data.empty:
            min_date = season_data['Date'].min()
            max_date = season_data['Date'].max()
            
            # Add a rectangle shape for each season
            fig_sst.add_shape(
                type="rect",
                x0=min_date,
                x1=max_date,
                y0=df_sst[sst_col].min() - 0.5,  # Extend slightly below the min temperature
                y1=df_sst[sst_col].max() + 0.5,  # Extend slightly above the max temperature
                fillcolor=colors['fill'],
                opacity=1.0,
                layer="below",
                line_width=0,
            )
    
    # Add traces for each season section
    for season in ['Fall', 'Winter', 'Spring/Summer']:
        season_data = df_sst[df_sst['Season'] == season]
        fig_sst.add_trace(
            go.Scatter(
                x=season_data['Date'],
                y=season_data[sst_col],
                mode='lines',
                name=season,
                line=dict(color=season_colors[season]['line'], width=3)
            )
        )
    
    # Update layout for better visualization
    fig_sst.update_layout(
        height=350,
        margin=dict(l=40, r=20, t=10, b=40),
        xaxis_title="Date",
        yaxis_title="Temperature (°C)",
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
        template="plotly_white",
        hovermode="x unified"
    )
    
    # Add annotations for each section
    section_midpoints = {
        'Fall': df_sst[df_sst['Season'] == 'Fall']['Date'].mean(),
        'Winter': df_sst[df_sst['Season'] == 'Winter']['Date'].mean(),
        'Spring/Summer': df_sst[df_sst['Season'] == 'Spring/Summer']['Date'].mean()
    }
    
    for season, midpoint in section_midpoints.items():
        if pd.notna(midpoint):
            fig_sst.add_annotation(
                x=midpoint,
                y=df_sst[sst_col].max() + 0.3,
                text=season,
                showarrow=False,
                font=dict(size=14, color=season_colors[season]['line'])
            )
    
    st.plotly_chart(fig_sst, use_container_width=True)
    
    # Add data display in an expander to keep the layout compact
    with st.expander("View SST Data"):
        st.dataframe(df_sst[['Date', sst_col, 'Season']].head(20))
        st.write(f"Total rows: {len(df_sst)}")

except Exception as e:
    st.error(f"Error processing SST data: {str(e)}")
    st.write("Detailed error information:", e)
