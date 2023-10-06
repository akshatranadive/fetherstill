from django.db import models

class BatteryData(models.Model):
    battery_number = models.CharField(max_length=50)
    temperature = models.DecimalField(max_digits=5, decimal_places=2)
    voltage = models.DecimalField(max_digits=6, decimal_places=2)

    def __str__(self):
        return self.battery_number
