# Generated by Django 3.0.3 on 2020-06-03 12:38

from django.db import migrations
import picklefield.fields


class Migration(migrations.Migration):

    dependencies = [
        ('payroll_management', '0012_auto_20200326_1857'),
    ]

    operations = [
        migrations.AlterField(
            model_name='payslip',
            name='all_allowances',
            field=picklefield.fields.PickledObjectField(editable=False, null=True),
        ),
    ]
