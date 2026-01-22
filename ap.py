import pandas as pd
import datetime
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

# Ensure headers exist
headers = [
    'Date','Additional segment','Bank','Close account','Enable exchange','Reactivation',
    'Email','Mobile Number','Other','Complaints','Emails related to shoonya'
]
sheet.update(values=[headers], range_name='A1:K1')

# -------------------------
# ✅ Streamlit UI
# -------------------------

st.title('Ticket Tracking App')

today = str(datetime.date.today())

# Fetch all records to check existing dates
records = sheet.get_all_records()
dates = [row['Date'] for row in records]

# Fetch today's data if exists, else create default
if today in dates:
    today_record = records[dates.index(today)]
else:
    today_record = {col: 0 for col in headers}
    today_record['Date'] = today

# Inputs with previous values as defaults
additional_segment = st.number_input('Additional segments', value=int(today_record.get('Additional segment', 0)))
bank_account = st.number_input('Bank account', value=int(today_record.get('Bank', 0)))
close_account = st.number_input('Closed accounts', value=int(today_record.get('Close account', 0)))
enable_exchange = st.number_input('Enable exchange', value=int(today_record.get('Enable exchange', 0)))
reactivation = st.number_input('Reactivation', value=int(today_record.get('Reactivation', 0)))
email = st.number_input('Email change', value=int(today_record.get('Email', 0)))
mobile_number = st.number_input('Mobile number change', value=int(today_record.get('Mobile Number', 0)))
other = st.number_input('Other tickets', value=int(today_record.get('Other', 0)))
complaints = st.number_input('Complaints', value=int(today_record.get('Complaints', 0)))
emails_related_shoonya = st.number_input('Emails related to shoonya', value=int(today_record.get('Emails related to shoonya', 0)))

# -------------------------
# ✅ Submit Button
# -------------------------

if st.button("Submit"):
    # Prepare data row
    data_row = [
        today,
        additional_segment,
        bank_account,
        close_account,
        enable_exchange,
        reactivation,
        email,
        mobile_number,
        other,
        complaints,
        emails_related_shoonya
    ]

    if today in dates:
        row_number = dates.index(today) + 2  # +2 because header is row 1
        sheet.update(f'A{row_number}:K{row_number}', [data_row])
        st.success("✅ Existing entry updated for today.")
    else:
        sheet.append_row(data_row)
        st.success("✅ New entry added to Google Sheet.")

# -------------------------
# ✅ Display current data safely
# -------------------------

# Truncate long strings aggressively to avoid LargeUtf8
TRUNCATE_CHARS = 100  # keep 100 chars max for display

if records:
    df_display = pd.DataFrame(records)
    for col in df_display.columns:
        df_display[col] = df_display[col].astype(str).str.slice(0, TRUNCATE_CHARS)
else:
    df_display = pd.DataFrame(columns=headers)

st.dataframe(df_display)

# -------------------------
# ✅ CSV download (full data, no truncation)
# -------------------------

if records:
    df_csv = pd.DataFrame(records)
else:
    df_csv = pd.DataFrame(columns=headers)

csv = df_csv.to_csv(index=False).encode('utf-8')
st.download_button(
    label="Download Google Sheet as CSV",
    data=csv,
    file_name='google_sheet_data.csv',
    mime='text/csv'
)
