import gspread
from google.oauth2 import service_account
import pandas as pd
from sqlalchemy import create_engine

# Database connection string
db_connection_string = 'postgresql://nihal:Nihal%40uatdb123@65.1.85.43:5432/mandi_UAT'

# Create a database engine
engine = create_engine(db_connection_string)

# Connect to Google Sheets
scope = ['https://spreadsheets.google.com/feeds', 'https://www.googleapis.com/auth/drive']
credentials = service_account.Credentials.from_service_account_file(r'C:\Users\Nikita\Downloads\spreadsheet-419708-cf0b0d700de0.json', scopes=scope)
gc = gspread.authorize(credentials)

# Open the Google Sheet
sheet_url = 'https://docs.google.com/spreadsheets/d/1KbCdkoU4Fhw8056BOi_oCUkCJuLThhw0G-j584WMBrY/edit#gid=0'
sh = gc.open_by_url(sheet_url)

# Get all sheet names
sheet_names = sh.sheet1.spreadsheet.fetch_sheet_metadata()['sheets']
sheet_names = [sheet['properties']['title'] for sheet in sheet_names]

# Iterate over each sheet
for sheet_name in sheet_names:
    # Open the sheet
    worksheet = sh.worksheet(sheet_name)
    records = worksheet.get_all_values()
    df = pd.DataFrame(records[1:], columns=records[0])
    
    # Insert data into the database table
    df.to_sql(sheet_name, engine, if_exists='append', index=False)

# Close the database connection
engine.dispose()

print('Data inserted successfully!')
