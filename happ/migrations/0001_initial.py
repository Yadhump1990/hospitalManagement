# Generated by Django 3.2.17 on 2023-03-20 17:37

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='department',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('depName', models.CharField(max_length=90)),
                ('description', models.TextField()),
            ],
        ),
        migrations.CreateModel(
            name='doctor',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('fname', models.CharField(max_length=90)),
                ('lname', models.CharField(max_length=90)),
                ('gender', models.CharField(max_length=90)),
                ('department', models.CharField(max_length=90)),
                ('phone', models.BigIntegerField()),
                ('email', models.EmailField(max_length=254)),
                ('depId', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='happ.department')),
            ],
        ),
        migrations.CreateModel(
            name='hospital',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('hospitalname', models.CharField(max_length=90)),
                ('phone', models.BigIntegerField()),
                ('place', models.CharField(max_length=150)),
                ('post', models.CharField(max_length=90)),
                ('pin', models.IntegerField()),
                ('email', models.EmailField(max_length=254)),
            ],
        ),
        migrations.CreateModel(
            name='lab',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=90)),
                ('description', models.TextField()),
                ('image', models.FileField(upload_to='')),
                ('location', models.CharField(max_length=90)),
                ('capacity', models.IntegerField()),
                ('availability', models.CharField(max_length=90)),
                ('hid', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='happ.hospital')),
            ],
        ),
        migrations.CreateModel(
            name='login',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('username', models.CharField(max_length=90)),
                ('password', models.CharField(max_length=90)),
                ('type', models.CharField(max_length=90)),
            ],
        ),
        migrations.CreateModel(
            name='patient',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('fname', models.CharField(max_length=90)),
                ('lname', models.CharField(max_length=90)),
                ('gender', models.CharField(max_length=90)),
                ('DOB', models.DateField()),
                ('phone', models.BigIntegerField()),
                ('place', models.CharField(max_length=150)),
                ('post', models.CharField(max_length=90)),
                ('pin', models.IntegerField()),
                ('email', models.EmailField(max_length=254)),
                ('lid', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='happ.login')),
            ],
        ),
        migrations.CreateModel(
            name='schedule',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateField()),
                ('startTime', models.TimeField()),
                ('endTime', models.TimeField()),
                ('maxAppointment', models.IntegerField()),
                ('docId', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='happ.doctor')),
            ],
        ),
        migrations.CreateModel(
            name='prescription',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateField()),
                ('diagnosis', models.TextField()),
                ('medication', models.TextField()),
                ('dosage', models.CharField(max_length=90)),
                ('image', models.FileField(upload_to='')),
                ('docId', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='happ.doctor')),
                ('patId', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='happ.patient')),
            ],
        ),
        migrations.CreateModel(
            name='labTests',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=90)),
                ('description', models.TextField()),
                ('contact', models.BigIntegerField()),
                ('email', models.EmailField(max_length=254)),
                ('labId', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='happ.lab')),
            ],
        ),
        migrations.CreateModel(
            name='labTestApplication',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('dateApplied', models.DateField()),
                ('status', models.CharField(max_length=90)),
                ('docId', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='happ.doctor')),
                ('patId', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='happ.patient')),
                ('testId', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='happ.labtests')),
            ],
        ),
        migrations.CreateModel(
            name='labReport',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('dateReported', models.DateField()),
                ('result', models.TextField()),
                ('appId', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='happ.labtestapplication')),
            ],
        ),
        migrations.AddField(
            model_name='lab',
            name='lid',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='happ.login'),
        ),
        migrations.AddField(
            model_name='hospital',
            name='lid',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='happ.login'),
        ),
        migrations.CreateModel(
            name='facilities',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=90)),
                ('description', models.TextField()),
                ('image', models.FileField(upload_to='')),
                ('capacity', models.IntegerField()),
                ('availability', models.CharField(max_length=90)),
                ('location', models.CharField(max_length=90)),
                ('hid', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='happ.hospital')),
            ],
        ),
        migrations.AddField(
            model_name='doctor',
            name='hid',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='happ.hospital'),
        ),
        migrations.AddField(
            model_name='doctor',
            name='lid',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='happ.login'),
        ),
        migrations.AddField(
            model_name='department',
            name='hid',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='happ.hospital'),
        ),
        migrations.CreateModel(
            name='complaint',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('complaint', models.CharField(max_length=90)),
                ('reply', models.CharField(max_length=90)),
                ('date', models.DateField()),
                ('patId', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='happ.patient')),
            ],
        ),

    ]
