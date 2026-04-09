import streamlit as st
import pandas as pd
import psycopg2
import os
import time

# Config
DB_HOST = os.getenv("DB_HOST", "postgres-service")
DB_NAME = os.getenv("DB_NAME", "cryptodb")
DB_USER = os.getenv("DB_USER", "user")
DB_PASS = os.getenv("DB_PASS", "password")

st.set_page_config(page_title="Crypto K8s Dashboard", layout="wide")
st.title("📈 Real-Time Crypto Pipeline")
st.subheader("Data fetched from API -> Redis -> Processor -> Postgres")

def get_data():
    try:
        conn = psycopg2.connect(host=DB_HOST, database=DB_NAME, user=DB_USER, password=DB_PASS)
        query = "SELECT timestamp, symbol, price, trend FROM prices ORDER BY timestamp DESC LIMIT 20"
        df = pd.read_sql(query, conn)
        conn.close()
        return df
    except Exception as e:
        st.error(f"Error connecting to Database: {e}")
        return pd.DataFrame()

# Auto-refresh logic
placeholder = st.empty()

while True:
    with placeholder.container():
        df = get_data()
        if not df.empty:
            col1, col2 = st.columns(2)
            with col1:
                st.write("### Latest 20 Records")
                st.dataframe(df, use_container_width=True)
            with col2:
                st.write("### Price Movement")
                st.line_chart(df.set_index('timestamp')['price'])
        else:
            st.warning("Waiting for data to arrive in Postgres...")
    
    time.sleep(10)