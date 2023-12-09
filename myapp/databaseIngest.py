import pandas as pd
from sqlalchemy import create_engine
from datetime import datetime
import os
from django.conf import settings

def ingest(file_path, file_type, file_date):
    # Database connection parameters
    db_params = {
    "host": "127.0.0.1",
    "database": "fetherstill",
    "user": "postgres",
    "password": "123",
    }

    # Create a SQLAlchemy engine
    engine = create_engine(f'postgresql://{db_params["user"]}:{db_params["password"]}@{db_params["host"]}/{db_params["database"]}')

    if file_type == "Inlet":
        table = "myapp_inflow"
    elif file_type ==  "Outlet":
        table = "myapp_outflow"
    elif file_type == "Pump":
        table = "myapp_pump"
    else:
        print("Wrong file type!")

    file_path = os.path.join(settings.MEDIA_ROOT,file_path)

    base, ext = os.path.splitext(file_path)

    if ext == ".csv":
        data = pd.read_csv(file_path)
    elif ext == ".xlsx":
        data = pd.read_excel(file_path)
    else:
        print("Unsupported extension:",ext)

    data.columns = map(str, data.columns)
    data['Date'] = file_date
    data['batteryID'] = 101
    data.to_sql(table, engine, if_exists='append', index=False)

    print("Data imported successfully")