from django.db import models
from django.contrib.auth.models import User


class BatteryData(models.Model):
    battery_number = models.CharField(max_length=50)
    temperature = models.DecimalField(max_digits=5, decimal_places=2)
    voltage = models.DecimalField(max_digits=6, decimal_places=2)

    def __str__(self):
        return self.battery_number

class Outflow(models.Model):
    iteration = models.BigIntegerField(db_column='Iteration', blank=True, null=True)  # Field name made lowercase.
    cputime = models.BigIntegerField(db_column='CPUTime', blank=True, null=True)  # Field name made lowercase.
    phystime = models.BigIntegerField(db_column='PhysTime', blank=True, null=True)  # Field name made lowercase.
    travels = models.FloatField(db_column='Travels', blank=True, null=True)  # Field name made lowercase.
    value = models.FloatField(db_column='Value', blank=True, null=True)  # Field name made lowercase.
    avvalue = models.FloatField(db_column='AvValue', blank=True, null=True)  # Field name made lowercase.
    minvalue = models.FloatField(db_column='MinValue', blank=True, null=True)  # Field name made lowercase.
    maxvalue = models.FloatField(db_column='MaxValue', blank=True, null=True)  # Field name made lowercase.
    delta = models.FloatField(db_column='Delta', blank=True, null=True)  # Field name made lowercase.
    criteria = models.FloatField(db_column='Criteria', blank=True, null=True)  # Field name made lowercase.
    prevavrefvalue = models.BigIntegerField(db_column='PrevAvRefValue', blank=True,
                                            null=True)  # Field name made lowercase.
    progress = models.BigIntegerField(db_column='Progress', blank=True, null=True)  # Field name made lowercase.
    criteriatype = models.BigIntegerField(db_column='CriteriaType', blank=True, null=True)  # Field name made lowercase.
    criteriavartype = models.BigIntegerField(db_column='CriteriaVarType', blank=True,
                                             null=True)  # Field name made lowercase.
    criteriapercentage = models.BigIntegerField(db_column='CriteriaPercentage', blank=True,
                                                null=True)  # Field name made lowercase.
    date = models.DateField(db_column='Date', blank=True, null=True)  # Field name made lowercase.
    batteryid = models.BigIntegerField(db_column='batteryID', blank=True, null=True)  # Field name made lowercase.

    def __str__(self):
        return 'name'

# class Outflow(models.Model):
#     iteration = models.BigIntegerField(db_column='Iteration', blank=True, null=True)  # Field name made lowercase.
#     cputime = models.BigIntegerField(db_column='CPUTime', blank=True, null=True)  # Field name made lowercase.
#     phystime = models.BigIntegerField(db_column='PhysTime', blank=True, null=True)  # Field name made lowercase.
#     travels = models.FloatField(db_column='Travels', blank=True, null=True)  # Field name made lowercase.
#     value = models.FloatField(db_column='Value', blank=True, null=True)  # Field name made lowercase.
#     avvalue = models.FloatField(db_column='AvValue', blank=True, null=True)  # Field name made lowercase.
#     minvalue = models.FloatField(db_column='MinValue', blank=True, null=True)  # Field name made lowercase.
#     maxvalue = models.FloatField(db_column='MaxValue', blank=True, null=True)  # Field name made lowercase.
#     delta = models.FloatField(db_column='Delta', blank=True, null=True)  # Field name made lowercase.
#     criteria = models.FloatField(db_column='Criteria', blank=True, null=True)  # Field name made lowercase.
#     prevavrefvalue = models.BigIntegerField(db_column='PrevAvRefValue', blank=True, null=True)  # Field name made lowercase.
#     progress = models.BigIntegerField(db_column='Progress', blank=True, null=True)  # Field name made lowercase.
#     criteriatype = models.BigIntegerField(db_column='CriteriaType', blank=True, null=True)  # Field name made lowercase.
#     criteriavartype = models.BigIntegerField(db_column='CriteriaVarType', blank=True, null=True)  # Field name made lowercase.
#     criteriapercentage = models.BigIntegerField(db_column='CriteriaPercentage', blank=True, null=True)  # Field name made lowercase.
#     datetime = models.DateTimeField(db_column='DateTime', blank=True, null=True)  # Field name made lowercase.
#     batteryid = models.BigIntegerField(db_column='batteryID', blank=True, null=True)  # Field name made lowercase.
#
#     # class Meta:
#     #     managed = False
#     #     db_table = 'outflow'

# class Pump(models.Model):
#     w = models.FloatField(db_column='W', blank=True, null=True)  # Field name made lowercase.
#     v = models.FloatField(db_column='V', blank=True, null=True)  # Field name made lowercase.
#     a = models.FloatField(db_column='A', blank=True, null=True)  # Field name made lowercase.
#     flow_l_min = models.FloatField(db_column='flow', blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
#     r_sec = models.BigIntegerField(db_column='rPersec', blank=True, null=True)  # Field renamed to remove unsuitable characters.
#     temp_field = models.FloatField(db_column='Temp', blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters. Field renamed because it ended with '_'.
#     datetime = models.DateTimeField(db_column='DateTime', blank=True, null=True)  # Field name made lowercase.
#     batteryid = models.BigIntegerField(db_column='batteryID', blank=True, null=True)  # Field name made lowercase.
#
#     # class Meta:
#     #     managed = False
#     #     db_table = 'pump'

# class Inflow(models.Model):
#     iteration = models.BigIntegerField(db_column='Iteration', blank=True, null=True)  # Field name made lowercase.
#     cputime = models.BigIntegerField(db_column='CPUTime', blank=True, null=True)  # Field name made lowercase.
#     phystime = models.BigIntegerField(db_column='PhysTime', blank=True, null=True)  # Field name made lowercase.
#     travels = models.FloatField(db_column='Travels', blank=True, null=True)  # Field name made lowercase.
#     value = models.FloatField(db_column='Value', blank=True, null=True)  # Field name made lowercase.
#     avvalue = models.FloatField(db_column='AvValue', blank=True, null=True)  # Field name made lowercase.
#     minvalue = models.FloatField(db_column='MinValue', blank=True, null=True)  # Field name made lowercase.
#     maxvalue = models.FloatField(db_column='MaxValue', blank=True, null=True)  # Field name made lowercase.
#     delta = models.FloatField(db_column='Delta', blank=True, null=True)  # Field name made lowercase.
#     criteria = models.FloatField(db_column='Criteria', blank=True, null=True)  # Field name made lowercase.
#     prevavrefvalue = models.BigIntegerField(db_column='PrevAvRefValue', blank=True, null=True)  # Field name made lowercase.
#     progress = models.FloatField(db_column='Progress', blank=True, null=True)  # Field name made lowercase.
#     criteriatype = models.BigIntegerField(db_column='CriteriaType', blank=True, null=True)  # Field name made lowercase.
#     criteriavartype = models.BigIntegerField(db_column='CriteriaVarType', blank=True, null=True)  # Field name made lowercase.
#     criteriapercentage = models.BigIntegerField(db_column='CriteriaPercentage', blank=True, null=True)  # Field name made lowercase.
#     datetime = models.DateTimeField(db_column='DateTime', blank=True, null=True)  # Field name made lowercase.
#     batteryid = models.BigIntegerField(db_column='batteryID', blank=True, null=True)  # Field name made lowercase.
#
#     # class Meta:
#     #     managed = False
#     #     db_table = 'inflow'

class Inflow(models.Model):
    iteration = models.BigIntegerField(db_column='Iteration', blank=True, null=True)  # Field name made lowercase.
    cputime = models.BigIntegerField(db_column='CPUTime', blank=True, null=True)  # Field name made lowercase.
    phystime = models.BigIntegerField(db_column='PhysTime', blank=True, null=True)  # Field name made lowercase.
    travels = models.FloatField(db_column='Travels', blank=True, null=True)  # Field name made lowercase.
    value = models.FloatField(db_column='Value', blank=True, null=True)  # Field name made lowercase.
    avvalue = models.FloatField(db_column='AvValue', blank=True, null=True)  # Field name made lowercase.
    minvalue = models.FloatField(db_column='MinValue', blank=True, null=True)  # Field name made lowercase.
    maxvalue = models.FloatField(db_column='MaxValue', blank=True, null=True)  # Field name made lowercase.
    delta = models.FloatField(db_column='Delta', blank=True, null=True)  # Field name made lowercase.
    criteria = models.FloatField(db_column='Criteria', blank=True, null=True)  # Field name made lowercase.
    prevavrefvalue = models.BigIntegerField(db_column='PrevAvRefValue', blank=True,
                                            null=True)  # Field name made lowercase.
    progress = models.FloatField(db_column='Progress', blank=True, null=True)  # Field name made lowercase.
    criteriatype = models.BigIntegerField(db_column='CriteriaType', blank=True, null=True)  # Field name made lowercase.
    criteriavartype = models.BigIntegerField(db_column='CriteriaVarType', blank=True,
                                             null=True)  # Field name made lowercase.
    criteriapercentage = models.BigIntegerField(db_column='CriteriaPercentage', blank=True,
                                                null=True)  # Field name made lowercase.
    date = models.DateField(db_column='Date', blank=True, null=True)  # Field name made lowercase.
    batteryid = models.BigIntegerField(db_column='batteryID', blank=True, null=True)  # Field name made lowercase.

    def __str__(self):
        return 'name'
class Pump(models.Model):
    w = models.FloatField(db_column='W', blank=True, null=True)  # Field name made lowercase.
    v = models.FloatField(db_column='V', blank=True, null=True)  # Field name made lowercase.
    a = models.FloatField(db_column='A', blank=True, null=True)  # Field name made lowercase.
    flow_l_min = models.FloatField(db_column='flow', blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    r_sec = models.BigIntegerField(db_column='rPersec', blank=True, null=True)  # Field renamed to remove unsuitable characters.
    temp_field = models.FloatField(db_column='Temp', blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters. Field renamed because it ended with '_'.
    date = models.DateField(db_column='Date', blank=True, null=True)  # Field name made lowercase.
    batteryid = models.BigIntegerField(db_column='batteryID', blank=True, null=True)  # Field name made lowercase.

    def __str__(self):
        return self.w


class UploadLog(models.Model):
    UPLOAD_TYPE_CHOICE = [
        ("New", "New"),
        ("Edited", "Edited"),
    ]
    FILE_CATEGORY_CHOICE = [
        ("Battery Module", "Battery Module"),
        ("Simulation", "Simulation"),
    ]
    FILE_TYPE_CHOICE = [
        ("Inlet","Inlet"),
        ("Outlet","Outlet"),
        ("Pump","Pump"),
        ("Type 1","Type 1"),
        ("Type 2","Type 2"),
    ]
    upload_datetime = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, blank=False)
    file = models.FileField(blank=False)
    upload_type = models.CharField(choices=UPLOAD_TYPE_CHOICE, blank=False)
    file_category = models.CharField(choices=FILE_CATEGORY_CHOICE, blank=False)
    file_type = models.CharField(choices=FILE_TYPE_CHOICE, blank=False)
    file_date = models.DateField(blank=False)
    file_name = models.CharField(max_length=64, blank=False)