import streamlit as st
import psycopg2
import pandas as pd

# Load secrets
st.set_page_config(page_title="PostgreSQL Connection", layout="wide")

st.title("PostgreSQL Data Connection")

# Get secrets from Streamlit
db_credentials = st.secrets["postgres"]
  

  
# Connect to PostgreSQL
@st.cache_resource
def get_connection():
    return psycopg2.connect(
        host=db_credentials["host"],
        database=db_credentials["database"],
        user=db_credentials["username "],
        password=db_credentials["password"],
        port=db_credentials["port"]
    )

# Fetch data function
def fetch_data(query):
    conn = get_connection()
    df = pd.read_sql_query(query, conn)
    conn.close()
    return df

# User Input Query
query = st.text_area("Enter SQL Query", "SELECT * FROM clients LIMIT 10;")

if st.button("Run Query"):
    try:
        data = fetch_data(query)
        st.write("### Query Results:")
        st.dataframe(data)
    except Exception as e:
        st.error(f"Error: {e}")

st.success("Connected to PostgreSQL successfully!")  