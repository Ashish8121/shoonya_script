import pandas as pd
import datetime
import streamlit as st
import os
import gspread
from oauth2client.service_account import ServiceAccountCredentials

# ✅ Load credentials from Streamlit secrets
service_account_info = json.loads(st.secrets["gcp_service_account"])

# ✅ Define scope
scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]

# ✅ Authenticate using from_json_keyfile_dict
creds = ServiceAccountCredentials.from_json_keyfile_dict(service_account_info, scope)
client = gspread.authorize(creds)

# ✅ Open your Google Sheet as before
sheet = client.open("streamlit").worksheet("Sheet1")

records = sheet.get_all_records()
headers = ['Date','Additional segment', 'Bank', 'Close account', 'Enable exchange', 'Reactivation' ,'Email', 'Mobile Number','Other', 'Complaints']
sheet.update(values=[headers], range_name='A1:K1')

today = datetime.date.today()

additional_segment = st.number_input('Additional segments', value=0)
bank_account = st.number_input('Bank account', value=0)
close_account = st.number_input('Closed accounts', value=0)
enable_exchange = st.number_input('Enable exchange', value=0)
reactivation = st.number_input('Reactivation', value=0)
email = st.number_input('Email change', value=0)
mobile_number = st.number_input('Mobile number change', value=0)
other = st.number_input('Other tickets', value=0)
complaints = st.number_input('Complaints', value=0)
emails_related_shoonya = st.number_input('Emails related to shoonya', value=0)



if st.button("Submit"):
    # Prepare data row matching your headers
    data_row = [
        str(today),  # Date as string
        str(additional_segment),
        str(bank_account),
        str(close_account),
        str(enable_exchange),
        str(reactivation),
        str(email),
        str(mobile_number),
        str(other),
        str(complaints),
        str(emails_related_shoonya)
    ]

    # ✅ Fetch all records to check existing dates
    records = sheet.get_all_records()

    # ✅ Convert records to list of dates
    dates = [str(row['Date']) for row in records]

    if str(today) in dates:
        # 🔷 If today's date exists, update that row
        row_number = dates.index(str(today)) + 2  # +2 because sheet rows are 1-indexed and header is row 1
        sheet.update(f'A{row_number}:K{row_number}', [data_row])
        st.success("✅ Existing entry updated for today.")
    else:
        # 🔷 If today's date does not exist, append new row
        sheet.append_row(data_row)
        st.success("✅ New entry added to Google Sheet.")

# 🔷 **Optional: Display current data**
records = sheet.get_all_records()
st.dataframe(records)

# 🔷 Download CSV button
import pandas as pd
df = pd.DataFrame(records)
csv = df.to_csv(index=False).encode('utf-8')
st.download_button(
    label="Download Google Sheet as CSV",
    data=csv,
    file_name='google_sheet_data.csv',
    mime='text/csv'
)















