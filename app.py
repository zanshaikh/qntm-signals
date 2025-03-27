
import streamlit as st
import pandas as pd

st.set_page_config(page_title='QNTM Dashboard', layout='wide')
st.title("📊 QNTM Trade Signal Dashboard")

uploaded_file = st.file_uploader("Upload Your Trade Log CSV", type="csv")

if uploaded_file:
    df = pd.read_csv(uploaded_file)
    st.subheader("Signal Log")
    st.dataframe(df)

    st.subheader("Summary Stats")
    st.write("Total Trades:", len(df))
    if 'simulated_pnl' in df.columns:
        st.write("Average PnL:", round(df['simulated_pnl'].mean(), 2))
        st.write("Total PnL:", round(df['simulated_pnl'].sum(), 2))
        st.write("TP Count:", (df['exit_type'] == 'TP').sum())
        st.write("SL Count:", (df['exit_type'] == 'SL').sum())
        st.write("Time Exits:", (df['exit_type'] == 'Time Exit').sum())
