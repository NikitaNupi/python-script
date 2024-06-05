import gspread
from google.oauth2 import service_account
import pandas as pd
from sqlalchemy import create_engine
from sqlalchemy import text

# Database connection string
db_connection_string = 'postgresql://postgres:PJkT%402o23095%4013@65.1.85.43:5432/MAP_UAT_NEW2'

# Create a database engine
engine = create_engine(db_connection_string)

# Connect to Google Sheets
scope = ['https://spreadsheets.google.com/feeds', 'https://www.googleapis.com/auth/drive']
credentials = service_account.Credentials.from_service_account_file(r'C:\Users\Nikita\Downloads\spreadsheet-419708-cf0b0d700de0.json', scopes=scope)
gc = gspread.authorize(credentials)

# Open the Google Sheet
sheet_url = 'https://docs.google.com/spreadsheets/d/1KbCdkoU4Fhw8056BOi_oCUkCJuLThhw0G-j584WMBrY/edit#gid=0'
sh = gc.open_by_url(sheet_url)
worksheet = sh.get_worksheet(0)  # assuming data is in the first sheet

# Get all values from the sheet
records = worksheet.get_all_values()
print(records)
# Create a DataFrame from the records
df = pd.DataFrame(records[1:], columns=records[0])

# Create a list to store CorporateIds
corporate_ids = []

# Query the database for CorporateId based on Name
with engine.connect() as conn:
    for name in df['Name']:
        query = text('SELECT "CorporateId" FROM "T_Co_Corporate" WHERE "Name" = :name')
        result = conn.execute(query.bindparams(name="TESTCORPORATE1101"))
        row = result.fetchone()
        # print("Query:", query, "Result:", result, "Row:", row)

        if row:
            corporate_ids.append(row[0])
        else:
            corporate_ids.append(None)  # Handle the case where Name is not found

# Add the CorporateId to the DataFrame
df['CorporateId'] = corporate_ids

# Close the database connection
engine.dispose()

# Print the DataFrame with CorporateId
# print(df)
