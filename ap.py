import pandas as pd
import streamlit as st
import gspread
from oauth2client.service_account import ServiceAccountCredentials

# -------------------------
# ✅ Google Sheets Setup
# -------------------------

# Load credentials from Streamlit secrets
service_account_info = st.secrets["gcp_service_account"]

# Define scope
scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]

# Authenticate
creds = ServiceAccountCredentials.from_json_keyfile_dict(service_account_info, scope)
client = gspread.authorize(creds)

# Open Google Sheet
sheet = client.open("streamlit").worksheet("Sheet1")

# Fetch all records from Google Sheet
records = sheet.get_all_records()

# -------------------------
# ✅ Streamlit Display
# -------------------------

st.title("Google Sheet Data Viewer")

# Handle empty sheet safely
if records:
    df_display = pd.DataFrame(records)
    
    # Truncate long text to avoid LargeUtf8 errors in Streamlit
    TRUNCATE_CHARS = 100
    for col in df_display.columns:
        df_display[col] = df_display[col].astype(str).str.slice(0, TRUNCATE_CHARS)
else:
    # If sheet is empty, create empty dataframe with headers
    headers = sheet.row_values(1)  # get headers from first row
    df_display = pd.DataFrame(columns=headers)

# Display dataframe in Streamlit
st.dataframe(df_display)

# Optional: allow CSV download of full data
if records:
    df_csv = pd.DataFrame(records)
    csv = df_csv.to_csv(index=False).encode('utf-8')
    st.download_button(
        label="Download Google Sheet as CSV",
        data=csv,
        file_name="google_sheet_data.csv",
        mime="text/csv"
    )
