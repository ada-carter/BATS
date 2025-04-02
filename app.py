import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

st.set_page_config(page_title="BATS Dashboard", layout="wide")
st.title("BATS Dashboard")

# -----------------------------
# Temperature Profiles Plot
# -----------------------------
try:
    df_profiles = pd.read_excel("data/BATS_temperature_profiles.xlsx")
except Exception as e:
    st.error(f"Error loading temperature profiles data: {e}")
    st.stop()

# Check that we have at least three columns (Depth, Profile 1, Profile 2)
if df_profiles.shape[1] < 3:
    st.error("BATS_temperature_profiles.xlsx must have at least 3 columns (Depth, Profile 1, Profile 2)")
    st.stop()

# Define columns (assumes first column is Depth)
depth_col = df_profiles.columns[0]
profile1_col = df_profiles.columns[1]
profile2_col = df_profiles.columns[2]

# Convert to numeric and check for conversion errors
df_profiles[depth_col] = pd.to_numeric(df_profiles[depth_col], errors="coerce")
df_profiles[profile1_col] = pd.to_numeric(df_profiles[profile1_col], errors="coerce")
df_profiles[profile2_col] = pd.to_numeric(df_profiles[profile2_col], errors="coerce")

if df_profiles[depth_col].isnull().all() or df_profiles[profile1_col].isnull().all() or df_profiles[profile2_col].isnull().all():
    st.error("One or more required columns in BATS_temperature_profiles.xlsx could not be converted to numeric values.")
    st.stop()

fig_profiles = go.Figure()
fig_profiles.add_trace(go.Scatter(
    x=df_profiles[profile1_col],
    y=df_profiles[depth_col],
    mode='lines+markers',
    name="Profile 1"
))
fig_profiles.add_trace(go.Scatter(
    x=df_profiles[profile2_col],
    y=df_profiles[depth_col],
    mode='lines+markers',
    name="Profile 2"
))
fig_profiles.update_layout(
    title="Temperature vs. Depth",
    xaxis_title="Temperature (°C)",
    yaxis_title="Depth (m)",
    yaxis=dict(autorange="reversed", range=[0, 250]),
    template="plotly_white"
)
st.plotly_chart(fig_profiles, use_container_width=True)

# -----------------------------
# Sea Surface Temperature (SST) Plot
# -----------------------------
try:
    df_sst = pd.read_excel("data/OCN330_BATS_SST.xlsx")
except Exception as e:
    st.error(f"Error loading SST data: {e}")
    st.stop()

if df_sst.shape[1] < 2:
    st.error("OCN330_BATS_SST.xlsx must have at least 2 columns (Date, SST)")
    st.stop()

date_col = df_sst.columns[0]
sst_col = df_sst.columns[1]

# Convert date column to datetime
df_sst[date_col] = pd.to_datetime(df_sst[date_col], errors="coerce")
if df_sst[date_col].isnull().all():
    st.error("Date column in OCN330_BATS_SST.xlsx could not be parsed as dates.")
    st.stop()

# Convert SST values to numeric
df_sst[sst_col] = pd.to_numeric(df_sst[sst_col], errors="coerce")
if df_sst[sst_col].isnull().all():
    st.error("SST column in OCN330_BATS_SST.xlsx could not be converted to numeric values.")
    st.stop()

fig_sst = px.line(df_sst, x=date_col, y=sst_col,
                  title="Seasonal Evolution of SST",
                  labels={date_col: "Date", sst_col: "SST (°C)"},
                  template="plotly_white")
st.plotly_chart(fig_sst, use_container_width=True)
