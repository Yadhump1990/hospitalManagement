# Generated by Django 3.2.17 on 2023-05-04 05:46

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('happ', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='doctor',
            name='department',
        ),
        migrations.AlterField(
            model_name='login',
            name='username',
            field=models.CharField(max_length=90, unique=True),
        ),
        migrations.CreateModel(
            name='suggest',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('status', models.CharField(max_length=90)),
                ('docId', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='happ.doctor')),
                ('labtesId', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='happ.labtests')),
                ('patId', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='happ.patient')),
            ],
        ),
        migrations.CreateModel(
            name='booking',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateField()),
                ('timeStart', models.TimeField()),
                ('timeEnd', models.TimeField()),
                ('status', models.CharField(max_length=90)),
                ('patId', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='happ.patient')),
                ('scheId', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='happ.schedule')),
            ],
        ),
    ]
