# Generated by Django 4.2.5 on 2023-12-01 13:14

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('myapp', '0003_delete_uploadlog'),
    ]

    operations = [
        migrations.CreateModel(
            name='UploadLog',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('upload_datetime', models.DateTimeField(auto_now_add=True)),
                ('file', models.FileField(upload_to='')),
                ('upload_type', models.CharField(choices=[('New', 'New'), ('Edited', 'Edited')])),
                ('file_category', models.CharField(choices=[('Battery Module', 'Battery Module'), ('Simulation', 'Simulation')])),
                ('file_type', models.CharField(choices=[('Inlet', 'Inlet'), ('Outlet', 'Outlet'), ('Pump', 'Pump'), ('Type 1', 'Type 1'), ('Type 2', 'Type 2')])),
                ('file_date', models.DateField()),
                ('file_name', models.CharField(max_length=64)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]