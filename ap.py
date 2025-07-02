import pandas as pd
import datetime
import streamlit as st
import os

st.title("Daily Ticket Entry App")

# File name
file_name = 'tickets_summary.csv'

# Today's date
today = datetime.date.today()

# Initialize default values
defaults = {
    'Additional segment tickets': 0,
    'Bank': 0,
    'Close account': 0,
    'Enable exchange': 0,
    'Reactivation': 0,
    'Email': 0,
    'Mobile Number': 0,
    'Other': 0,
    'Complaints': 0
}

# Check if file exists and today's data exists
if os.path.isfile(file_name):
    old_data = pd.read_csv(file_name)
    old_data['Date'] = pd.to_datetime(old_data['Date']).dt.date

    if today in old_data['Date'].values:
        # Load today's data as defaults
        today_data = old_data[old_data['Date'] == today].iloc[0]
        defaults = {
            'Additional segment tickets': int(today_data['Additional segment tickets']),
            'Bank': int(today_data['Bank']),
            'Close account': int(today_data['Close account']),
            'Enable exchange': int(today_data['Enable exchange']),
            'Reactivation': int(today_data['Reactivation']),
            'Email': int(today_data['Email']),
            'Mobile Number': int(today_data['Mobile Number']),
            'Other': int(today_data['Other']),
            'Complaints': int(today_data['Complaints'])
        }

# Inputs with loaded defaults
additional_segment = st.number_input('Additional segments', value=defaults['Additional segment tickets'])
bank_account = st.number_input('Bank account', value=defaults['Bank'])
close_account = st.number_input('Closed', value=defaults['Close account'])
enable_exchange = st.number_input('Enable exchange', value=defaults['Enable exchange'])
reactivation = st.number_input('Reactivation', value=defaults['Reactivation'])
email = st.number_input('Email change ', value=defaults['Email'])
mobile_number = st.number_input('Mobile number ', value=defaults['Mobile Number'])
complaints = st.number_input('Complaint', value=defaults['Complaints'])
other = st.number_input('Other tickets', value=defaults['Other'])
email_related_shoonya = st.number_input('Emails related to shoonya', value=defaults['Other'])


# Create new data entry
new_data = pd.DataFrame({
    'Date': [today],
    'Additional segment tickets': [additional_segment],
    'Bank': [bank_account],
    'Close account': [close_account],
    'Enable exchange': [enable_exchange],
    'Reactivation': [reactivation],
    'Email': [email],
    'Mobile Number': [mobile_number], 
    'Other': [other], 
    'Complaints': [complaints], 
    'Emails related to shoonya': [email_related_shoonya]
})

# Update logic
if os.path.isfile(file_name):
    if today in old_data['Date'].values:
        # Update existing today's row
        for col in new_data.columns:
            old_data.loc[old_data['Date'] == today, col] = new_data[col].values[0]
        updated_data = old_data
    else:
        # Append new row
        updated_data = pd.concat([old_data, new_data], ignore_index=True)
else:
    updated_data = new_data

# Save updated data to CSV
updated_data.to_csv(file_name, index=False)

# Display updated data
st.dataframe(updated_data)
