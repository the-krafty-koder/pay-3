# Generated by Django 2.2.5 on 2020-03-02 18:56

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('authentication', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='users',
            old_name='institution_name',
            new_name='firm_name',
        ),
    ]
