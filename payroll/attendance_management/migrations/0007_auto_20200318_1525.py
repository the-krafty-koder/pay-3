# Generated by Django 3.0.3 on 2020-03-18 15:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('attendance_management', '0006_remove_dailyattendance_name'),
    ]

    operations = [
        migrations.AddField(
            model_name='dailyattendance',
            name='name',
            field=models.CharField(max_length=15, null=True),
        ),
        migrations.AlterField(
            model_name='attendance',
            name='date_created',
            field=models.DateField(auto_now_add=True),
        ),
    ]
