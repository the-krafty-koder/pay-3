# Generated by Django 3.0.3 on 2020-03-26 15:57

from django.db import migrations
import picklefield.fields


class Migration(migrations.Migration):

    dependencies = [
        ('employee_management', '0021_uploadedimage'),
    ]

    operations = [
        migrations.AlterField(
            model_name='employee',
            name='documents',
            field=picklefield.fields.PickledObjectField(default=list, editable=False, null=True),
        ),
        migrations.AlterField(
            model_name='employee',
            name='education',
            field=picklefield.fields.PickledObjectField(default=list, editable=False, null=True),
        ),
    ]
