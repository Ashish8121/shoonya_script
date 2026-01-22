import pandas as pd
import datetime
import streamlit as st
import gspread
from oauth2client.service_account import ServiceAccountCredentials

# -------------------------
# ✅ Google Sheets Setup
# -------------------------

# Load credentials from Streamlit secrets
try:
    service_account_info = st.secrets["gcp_service_account"]
except KeyError:
    st.error("GCP Service Account secrets not found. Please check your Streamlit secrets.")
    st.stop()

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

# Only update headers if the sheet is empty to avoid overwriting data every run
if not sheet.get_all_values():
    sheet.update(values=[headers], range_name='A1:K1')

# -------------------------
# ✅ Streamlit UI
# -------------------------

st.title('Ticket Tracking App')

today = str(datetime.date.today())

# Fetch all records
records = sheet.get_all_records()
dates = [str(row['Date']) for row in records] # Ensure dates are strings for comparison

# Prepare today's default values
if today in dates:
    # Find the last occurrence of today's date
    today_record = [r for r in records if str(r['Date']) == today][-1]
else:
    today_record = {col: 0 for col in headers}
    today_record['Date'] = today

# Input fields (grouped for cleaner UI)
with st.expander("Update Today's Metrics", expanded=True):
    col1, col2 = st.columns(2)
    with col1:
        additional_segment = st.number_input('Additional segments', value=int(today_record.get('Additional segment', 0)))
        bank_account = st.number_input('Bank account', value=int(today_record.get('Bank', 0)))
        close_account = st.number_input('Closed accounts', value=int(today_record.get('Close account', 0)))
        enable_exchange = st.number_input('Enable exchange', value=int(today_record.get('Enable exchange', 0)))
        reactivation = st.number_input('Reactivation', value=int(today_record.get('Reactivation', 0)))
    with col2:
        email = st.number_input('Email change', value=int(today_record.get('Email', 0)))
        mobile_number = st.number_input('Mobile number change', value=int(today_record.get('Mobile Number', 0)))
        other = st.number_input('Other tickets', value=int(today_record.get('Other', 0)))
        complaints = st.number_input('Complaints', value=int(today_record.get('Complaints', 0)))
        emails_related_shoonya = st.number_input('Emails related to shoonya', value=int(today_record.get('Emails related to shoonya', 0)))

# -------------------------
# ✅ Submit Button
# -------------------------

if st.button("Submit Data", type="primary"):
    data_row = [
        today, additional_segment, bank_account, close_account, 
        enable_exchange, reactivation, email, mobile_number, 
        other, complaints, emails_related_shoonya
    ]

    if today in dates:
        # Get row number (index is 0-based, +1 for 1-based, +1 for header)
        row_number = dates.index(today) + 2
        sheet.update(values=[data_row], range_name=f'A{row_number}:K{row_number}')
        st.success(f"✅ Existing entry updated for {today}.")
    else:
        sheet.append_row(data_row)
        st.success(f"✅ New entry added for {today}.")
    
    # Rerun to refresh the table below
    st.rerun()

# -------------------------
# ✅ Display current data safely
# -------------------------

st.subheader("Google Sheet History")

if records:
    df_display = pd.DataFrame(records)
    
    # FIX: Convert specifically to 'object' type or standard string to avoid LargeUtf8 error
    # We apply this specifically to non-numeric columns if necessary, or the whole DF
    df_display = df_display.astype(object)
    
    st.dataframe(df_display, use_container_width=True)
    
    # CSV download (full data)
    csv = df_display.to_csv(index=False).encode('utf-8')
    st.download_button(
        label="Download as CSV",
        data=csv,
        file_name=f'ticket_data_{today}.csv',
        mime='text/csv'
    )
else:
    st.info("No records found in the Google Sheet yet.")
