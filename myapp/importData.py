import csv
from models import BatteryData  # Import your BatteryData model

def import_battery_data_from_csv(file_path):
    with open(file_path, 'r') as csv_file:
        csv_reader = csv.DictReader(csv_file)
        for row in csv_reader:
            BatteryData.objects.create(
                battery_number=row['battery_number'],
                temperature=float(row['temperature']),
                voltage=float(row['voltage'])
            )

# Call the function to import data
import_battery_data_from_csv('battery_data.csv')
