# Generated by Django 3.2.17 on 2023-05-04 05:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('happ', '0002_auto_20230504_1116'),
    ]

    operations = [
        migrations.AlterField(
            model_name='login',
            name='username',
            field=models.CharField(max_length=90),
        ),
    ]
