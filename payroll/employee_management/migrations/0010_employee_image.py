# Generated by Django 2.2.5 on 2020-03-02 13:18

from django.db import migrations, models
import employee_management.models


class Migration(migrations.Migration):

    dependencies = [
        ('employee_management', '0009_auto_20200218_1531'),
    ]

    operations = [
        migrations.AddField(
            model_name='employee',
            name='image',
            field=models.ImageField(default=None, null=True, upload_to=employee_management.models.image_file_path),
        ),
    ]
