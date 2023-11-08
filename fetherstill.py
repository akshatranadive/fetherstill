import pandas as pd
from sqlalchemy import create_engine
from datetime import datetime

# Database connection parameters
db_params = {
    "host": "localhost",
    "database": "fetherstill",
    "user": "postgres",
    "password": "1234",
}

# File paths
excel_file = "C:\\Users\\sanja\\fetherstill\\12v pump Cal curve.xlsx"
csv_file1 = "C:\\Users\\sanja\\Desktop\\project\\SG outlet velocity av.csv"
csv_file2 = "C:\\Users\\sanja\\Desktop\\project\\SG inlet volume flow rate.csv"

# Create a SQLAlchemy engine
engine = create_engine(f'postgresql://{db_params["user"]}:{db_params["password"]}@{db_params["host"]}/{db_params["database"]}')

try:
    # Get the current date and time
    current_datetime = datetime.now()

    # Create a new table "battery" with a single column "batteryID" and add DateTime column
    battery_data = pd.DataFrame({'batteryID': [101], 'DateTime': [current_datetime]})
    battery_data.to_sql('battery', engine, if_exists='replace', index=False)

    # Read data from Excel file using pandas and add DateTime and batteryID columns
    excel_data = pd.read_excel(excel_file)
    excel_data['DateTime'] = current_datetime
    excel_data['batteryID'] = 101  # Set the batteryID to the desired value
    excel_data.to_sql('myapp_pump', engine, if_exists='replace', index=False)

    # Read data from the first CSV file using pandas and add DateTime and batteryID columns
    csv_data1 = pd.read_csv(csv_file1)
    csv_data1['DateTime'] = current_datetime
    csv_data1['batteryID'] = 101  # Set the batteryID to the desired value
    csv_data1.to_sql('myapp_outflow', engine, if_exists='replace', index=False)

    # Read data from the second CSV file using pandas and add DateTime and batteryID columns
    csv_data2 = pd.read_csv(csv_file2)
    csv_data2['DateTime'] = current_datetime
    csv_data2['batteryID'] = 101  # Set the batteryID to the desired value
    csv_data2.to_sql('myapp_inflow', engine, if_exists='replace', index=False)

    print("Data imported successfully with DateTime and batteryID.")
except Exception as e:
    print("Error:", e)