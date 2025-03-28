
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

st.set_page_config(page_title='QNTM MFE/MAE Analyzer', layout='wide')
st.title("📊 QNTM Trade Optimization Dashboard")

uploaded_file = st.file_uploader("Upload Your Trade Data CSV", type="csv")

if uploaded_file:
    df = pd.read_csv(uploaded_file)
    st.subheader("Uploaded Signal Data")
    st.dataframe(df)

    required_columns = {'entry_price', 'direction', 'mfe_pts', 'mae_pts', 'entry_time', 'mfe_time', 'mae_time', 'timeframe'}
    if required_columns.issubset(df.columns):
        st.subheader("📊 MFE/MAE Analysis with Timing & Timeframe")

        st.write("Average MFE:", round(df['mfe_pts'].mean(), 2))
        st.write("Average MAE:", round(df['mae_pts'].mean(), 2))

        st.write("Distribution of MFE")
        fig, ax = plt.subplots()
        df['mfe_pts'].hist(bins=20, ax=ax)
        ax.set_xlabel("MFE (pts)")
        ax.set_ylabel("Count")
        st.pyplot(fig)

        st.write("Distribution of MAE")
        fig, ax = plt.subplots()
        df['mae_pts'].hist(bins=20, ax=ax, color='red')
        ax.set_xlabel("MAE (pts)")
        ax.set_ylabel("Count")
        st.pyplot(fig)

        st.subheader("🕒 Time-Based Insights")
        df['entry_time'] = pd.to_datetime(df['entry_time'])
        df['mfe_time'] = pd.to_datetime(df['mfe_time'])
        df['mae_time'] = pd.to_datetime(df['mae_time'])

        df['time_to_mfe'] = (df['mfe_time'] - df['entry_time']).dt.total_seconds() / 60
        df['time_to_mae'] = (df['mae_time'] - df['entry_time']).dt.total_seconds() / 60

        st.write("Average Time to MFE (min):", round(df['time_to_mfe'].mean(), 2))
        st.write("Average Time to MAE (min):", round(df['time_to_mae'].mean(), 2))

        st.subheader("📈 Breakdown by Timeframe")
        timeframe_group = df.groupby('timeframe').agg({
            'mfe_pts': 'mean',
            'mae_pts': 'mean',
            'time_to_mfe': 'mean',
            'time_to_mae': 'mean'
        }).rename(columns={
            'mfe_pts': 'Avg MFE',
            'mae_pts': 'Avg MAE',
            'time_to_mfe': 'Avg Time to MFE (min)',
            'time_to_mae': 'Avg Time to MAE (min)'
        })
        st.dataframe(timeframe_group)
