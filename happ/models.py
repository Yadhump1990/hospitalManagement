from django.db import models

# Create your models here.
class login(models.Model):
    username=models.CharField(max_length=90, unique=True)
    password = models.CharField(max_length=90)
    type = models.CharField(max_length=90)

class hospital(models.Model):
    lid = models.ForeignKey(login, on_delete=models.CASCADE)
    hospitalname = models.CharField(max_length=90)
    phone = models.BigIntegerField()
    place = models.CharField(max_length=150)
    post = models.CharField(max_length=90)
    pin = models.IntegerField()
    email = models.EmailField()

class patient(models.Model):
    lid = models.ForeignKey(login,on_delete=models.CASCADE)
    fname = models.CharField(max_length=90)
    lname = models.CharField(max_length=90)
    gender = models.CharField(max_length=90)
    DOB = models.DateField()
    phone = models.BigIntegerField()
    place = models.CharField(max_length=150)
    post = models.CharField(max_length=90)
    pin = models.IntegerField()
    email = models.EmailField()

class department(models.Model):
    hid = models.ForeignKey(hospital, on_delete=models.CASCADE)
    depName = models.CharField(max_length=90)
    description = models.TextField()

class facilities(models.Model):
    hid = models.ForeignKey(hospital, on_delete=models.CASCADE)
    name = models.CharField(max_length=90)
    description = models.TextField()
    image = models.FileField()
    capacity = models.IntegerField()
    availability = models.CharField(max_length=90)
    location = models.CharField(max_length=90)

class doctor(models.Model):
    lid = models.ForeignKey(login, on_delete=models.CASCADE)
    hid = models.ForeignKey(hospital, on_delete=models.CASCADE)
    depId = models.ForeignKey(department, on_delete=models.CASCADE)
    fname = models.CharField(max_length=90)
    lname = models.CharField(max_length=90)
    gender = models.CharField(max_length=90)
    phone = models.BigIntegerField()
    email = models.EmailField()

class lab(models.Model):
    lid = models.ForeignKey(login, on_delete=models.CASCADE)
    hid = models.ForeignKey(hospital, on_delete=models.CASCADE)
    name = models.CharField(max_length=90)
    description = models.TextField()
    image = models.FileField()
    location = models.CharField(max_length=90)
    capacity = models.IntegerField()
    availability = models.CharField(max_length=90)

class schedule(models.Model):
    docId = models.ForeignKey(doctor, on_delete=models.CASCADE)
    date = models.DateField()
    startTime = models.TimeField()
    endTime = models.TimeField()
    maxAppointment = models.IntegerField()

class booking(models.Model):
    scheId = models.ForeignKey(schedule, on_delete=models.CASCADE)
    patId = models.ForeignKey(patient, on_delete=models.CASCADE)
    date = models.DateField()
    timeStart = models.TimeField()
    timeEnd = models.TimeField()
    status = models.CharField(max_length=90)

class prescription(models.Model):
    docId = models.ForeignKey(doctor, on_delete=models.CASCADE)
    patId = models.ForeignKey(patient, on_delete=models.CASCADE)
    date = models.DateField()
    diagnosis = models.TextField()
    medication = models.TextField()
    dosage = models.CharField(max_length=90)
    image = models.FileField()

class complaint(models.Model):
    patId = models.ForeignKey(patient, on_delete=models.CASCADE)
    complaint = models.CharField(max_length=90)
    reply = models.CharField(max_length=90)
    date = models.DateField()

class labTests(models.Model):
    labId = models.ForeignKey(lab, on_delete=models.CASCADE)
    name = models.CharField(max_length=90)
    description = models.TextField()
    contact = models.BigIntegerField()
    email = models.EmailField()

class labTestApplication(models.Model):
    patId = models.ForeignKey(patient, on_delete=models.CASCADE)
    docId = models.ForeignKey(doctor, on_delete=models.CASCADE)
    testId = models.ForeignKey(labTests, on_delete=models.CASCADE)
    dateApplied = models.DateField()
    status = models.CharField(max_length=90)

class suggest(models.Model):
    docId = models.ForeignKey(doctor, on_delete=models.CASCADE)
    patId = models.ForeignKey(patient, on_delete=models.CASCADE)
    labtesId = models.ForeignKey(labTests, on_delete=models.CASCADE)
    status = models.CharField(max_length=90)

class labReport(models.Model):
    appId = models.ForeignKey(labTestApplication, on_delete=models.CASCADE)
    dateReported = models.DateField()
    result = models.TextField()

    def save(self, *args, **kwargs):
        # Set the primary key to be the same as the foreign key
        self.pk = self.appId.pk
        super(labReport, self).save(*args, **kwargs)