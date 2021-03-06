# Generated by Django 2.2.5 on 2020-03-02 17:16

from django.db import migrations, models
import employee_management.models


class Migration(migrations.Migration):

    dependencies = [
        ('employee_management', '0013_education_employee'),
    ]

    operations = [
        migrations.CreateModel(
            name='Documents',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=20)),
                ('files', models.FileField(upload_to=employee_management.models.document_file_path)),
            ],
        ),
        migrations.AlterField(
            model_name='education',
            name='files',
            field=models.FileField(upload_to=employee_management.models.document_file_path),
        ),
    ]
