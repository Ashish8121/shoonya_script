import pandas as pd
import datetime
import streamlit as st
import gspread
from oauth2client.service_account import ServiceAccountCredentials

# ✅ Load credentials from Streamlit secrets
service_account_info = st.secrets["gcp_service_account"]

# ✅ Define scope
scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]

# ✅ Authenticate using from_json_keyfile_dict
creds = ServiceAccountCredentials.from_json_keyfile_dict(service_account_info, scope)
client = gspread.authorize(creds)

# ✅ Open your Google Sheet as before
sheet = client.open("streamlit").worksheet("Sheet1")

# Ensure headers exist
headers = ['Date','Additional segment', 'Bank', 'Close account', 'Enable exchange', 'Reactivation' ,'Email', 'Mobile Number','Other', 'Complaints','Emails related to shoonya']
sheet.update(values=[headers], range_name='A1:K1')

today = str(datetime.date.today())
st.title('Ticket tracking App')

# Fetch all records to check existing dates
records = sheet.get_all_records()
dates = [row['Date'] for row in records]

# Fetch today's data if exists for default inputs
if today in dates:
    today_record = records[dates.index(today)]
else:
    today_record = {col:0 for col in headers}
    today_record['Date'] = today

# Inputs with previous values as defaults
additional_segment = st.number_input('Additional segments', value=int(today_record.get('Additional segment',0)))
bank_account = st.number_input('Bank account', value=int(today_record.get('Bank',0)))
close_account = st.number_input('Closed accounts', value=int(today_record.get('Close account',0)))
enable_exchange = st.number_input('Enable exchange', value=int(today_record.get('Enable exchange',0)))
reactivation = st.number_input('Reactivation', value=int(today_record.get('Reactivation',0)))
email = st.number_input('Email change', value=int(today_record.get('Email',0)))
mobile_number = st.number_input('Mobile number change', value=int(today_record.get('Mobile Number',0)))
other = st.number_input('Other tickets', value=int(today_record.get('Other',0)))
complaints = st.number_input('Complaints', value=int(today_record.get('Complaints',0)))
emails_related_shoonya = st.number_input('Emails related to shoonya', value=int(today_record.get('Emails related to shoonya',0)))

if st.button("Submit"):
    # Prepare data row keeping previous values
    data_row = [
        today,
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

    if today in dates:
        row_number = dates.index(today) + 2  # +2 because header is row 1
        sheet.update(f'A{row_number}:K{row_number}', [data_row])
        st.success("✅ Existing entry updated for today.")
    else:
        sheet.append_row(data_row)
        st.success("✅ New entry added to Google Sheet.")

# Display current data
records = sheet.get_all_records()
df = pd.DataFrame(records).astype(str)
st.dataframe(df)


# Download CSV button
df = pd.DataFrame(records)
csv = df.to_csv(index=False).encode('utf-8')
st.download_button(
    label="Download Google Sheet as CSV",
    data=csv,
    file_name='google_sheet_data.csv',
    mime='text/csv'
)

