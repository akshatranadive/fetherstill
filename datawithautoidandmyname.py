import pandas as pd
from sqlalchemy import create_engine
from datetime import datetime

# Database connection parameters
db_params = {
    "host": "localhost",
    "database": "Stimulation",
    "user": "postgres",
    "password": "root",
}

# File paths
excel_file = "C:\\Users\\sanja\\Desktop\\project\\12v pump Cal curve.xlsx"
csv_file1 = "C:\\Users\\sanja\\Desktop\\project\\SG outlet velocity av.csv"
csv_file2 = "C:\\Users\\sanja\\Desktop\\project\\SG inlet volume flow rate.csv"

# Create a SQLAlchemy engine
engine = create_engine(f'postgresql://{db_params["user"]}:{db_params["password"]}@{db_params["host"]}/{db_params["database"]}')

try:
    # Get the current date and time
    current_datetime = datetime.now()

    # Create a new table "battery" with a single column "batteryID" and add DateTime column
    battery_data = pd.DataFrame({'id': [1], 'batteryid': [101], 'datetime': [current_datetime]})
    battery_data.to_sql('myname_battery', engine, if_exists='replace', index=False,)

    # Read data from Excel file using pandas and add DateTime and batteryID columns
    excel_data = pd.read_excel(excel_file)
    excel_data.columns = map(str.lower, excel_data.columns)  # Convert column names to lowercase
    excel_data['datetime'] = current_datetime
    excel_data['batteryid'] = 101  # Set the batteryID to the desired value
    excel_data['id'] = range(1, len(excel_data) + 1)  # Add an auto-incrementing 'id' column
    excel_data.to_sql('myname_pump', engine, if_exists='replace', index=False)

    # Read data from the first CSV file using pandas and add DateTime and batteryID columns
    csv_data1 = pd.read_csv(csv_file1)
    csv_data1.columns = map(str.lower, csv_data1.columns)  # Convert column names to lowercase
    csv_data1['datetime'] = current_datetime
    csv_data1['batteryid'] = 101  # Set the batteryID to the desired value
    csv_data1['id'] = range(1, len(csv_data1) + 1)  # Add an auto-incrementing 'id' column
    csv_data1.to_sql('myname_outflow', engine, if_exists='replace', index=False)

    # Read data from the second CSV file using pandas and add DateTime and batteryID columns
    csv_data2 = pd.read_csv(csv_file2)
    csv_data2.columns = map(str.lower, csv_data2.columns)  # Convert column names to lowercase
    csv_data2['datetime'] = current_datetime
    csv_data2['batteryid'] = 101  # Set the batteryID to the desired value
    csv_data2['id'] = range(1, len(csv_data2) + 1)  # Add an auto-incrementing 'id' column
    csv_data2.to_sql('myname_inflow', engine, if_exists='replace', index=False)

    print("Data imported successfully with lowercase column names and 'id' column.")
except Exception as e:
    print("Error:", e)
