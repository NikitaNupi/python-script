import gspread
from google.oauth2 import service_account
import pandas as pd
from sqlalchemy import create_engine

# Database connection string
db_connection_string = 'postgresql://postgres:PJkT%402o23095%4013@13.201.6.102:5432/qairis30'

# Create a database engine
engine = create_engine(db_connection_string)

# Connect to Google Sheets
scope = ['https://spreadsheets.google.com/feeds', 'https://www.googleapis.com/auth/drive']
credentials = service_account.Credentials.from_service_account_file(r'C:\Users\Nikita\Downloads\spreadsheet-419708-cf0b0d700de0.json', scopes=scope)
gc = gspread.authorize(credentials)

# Open the Google Sheet
# sheet_url = 'https://docs.google.com/spreadsheets/d/1eJl_m_TSbOqasH_2SU4PFYC_raY86N1I/edit#gid=2052419810'
sheet_url = 'https://docs.google.com/spreadsheets/d/1KbCdkoU4Fhw8056BOi_oCUkCJuLThhw0G-j584WMBrY/edit#gid=0'
sh = gc.open_by_url(sheet_url)
worksheet = sh.get_worksheet(0)  # assuming data is in the first sheet

# Get all values from the sheet
records = worksheet.get_all_values()

# Create a DataFrame from the records
df = pd.DataFrame(records[1:], columns=records[0])

# Insert data into the database table
df.to_sql('T_MST_Product', engine, if_exists='append', index=False)

# Close the database connection
engine.dispose()

print('Data inserted successfully!')