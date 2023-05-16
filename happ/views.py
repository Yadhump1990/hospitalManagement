import logging
import os
import secrets
from pprint import pprint

from django.conf import settings
from django.contrib import messages, auth
from django.contrib.auth.decorators import login_required
from django.contrib.auth.hashers import make_password
from django.core.files.storage import FileSystemStorage
from django.core.mail import send_mail
from django.http import HttpResponse, HttpResponseBadRequest, HttpResponseServerError, JsonResponse
from django.shortcuts import render, get_object_or_404, redirect

from django.utils import timezone
from django.utils.datetime_safe import datetime
import random
#for pdf generation\
import pdfkit
from fpdf import FPDF
# from weasyprint import HTML
# from io import BytesIO
# from django.conf import settings
# from django.template.loader import get_template
#####################
# Create your views here.
from happ.models import *


def main(request):
    return render(request, 'loginIndex.html')


def hospitalReg(request):
    return render(request, 'hospitalRegisterIndex.html')


def hospital_registration(request):
    try:
        name = request.POST['hosName']
        phone = request.POST['tel']
        place = request.POST['place']
        post = request.POST['post']
        pin = request.POST['pin']
        email = request.POST['email']
        username = request.POST['uname']
        password = request.POST['password']
        # to save username and password to login
        lob = login()
        lob.username = username
        lob.password = password
        lob.type = 'pending'
        lob.save()
        # save to hospital database
        hob = hospital()
        hob.hospitalname = name
        hob.phone = phone
        hob.place = place
        hob.post = post
        hob.pin = pin
        hob.email = email
        hob.lid = lob
        hob.save()
        # messages.success(request, 'Hospital registered successfully')
        return HttpResponse('''<script>alert("Hospital registered successfully");window.location='/'</script>''')
        # return redirect('/')
    except:
        messages.success(request, 'Username already exist')
        # return redirect('/hospitalReg')
        return HttpResponse('''<script>alert("Username already exist");window.location='/hospitalReg'</script>''')


def patientReg(request):
    return render(request, 'UserRegisterIndex.html')


def patient_registration(request):
    try:
        fname = request.POST['fname']
        lname = request.POST['lname']
        dob = request.POST['dob']
        phone = request.POST['tel']
        place = request.POST['place']
        post = request.POST['post']
        pin = request.POST['pin']
        gender = request.POST['radio']
        email = request.POST['email']
        uname = request.POST['uname']
        password = request.POST['password']
        lob = login()
        lob.username = uname
        lob.password = password
        lob.type = 'patient'
        lob.save()
        pob = patient()
        pob.fname = fname
        pob.lname = lname
        pob.DOB = dob
        pob.phone = phone
        pob.place = place
        pob.post = post
        pob.pin = pin
        pob.gender = gender
        pob.email = email
        pob.lid = lob
        pob.save()
        return HttpResponse('''<script>alert("patient registered successfully");window.location='/'</script>''')
    except:
        return HttpResponse('''<script>alert("Username already exist");window.location='/patientReg'</script>''')


def log(request):
    username = request.POST['uname']
    password = request.POST['password']
    try:
        logOb = login.objects.get(username=username, password=password)
        if logOb.type == 'admin':
            request.session['lid'] = logOb.id
            ob1 = auth.authenticate(username='admin', password='admin')  # for login authentication
            auth.login(request, ob1)  # for login authentication
            return HttpResponse('''<script>alert("welcome admin");window.location='/adminHome'</script>''')
        elif logOb.type == 'hospital':
            request.session['lid'] = logOb.id
            ob1 = auth.authenticate(username='admin', password='admin')  # for login authentication
            auth.login(request, ob1)  # for login authentication
            user_name = logOb.username
            print(user_name)
            alert_message = f"welcome, {user_name}!"
            response_text = f"<script>alert('{alert_message}');window.location='/hospitalHome'</script>"
            # return HttpResponse('''<script>alert('welcome hospital');window.location='/hospitalHome'</script>''')

            return HttpResponse(response_text)
        elif logOb.type == 'doctor':
            request.session['lid'] = logOb.id
            ob1 = auth.authenticate(username='admin', password='admin')  # for login authentication
            auth.login(request, ob1)  # for login authentication
            user_name = logOb.username
            alert_message = "welcome, %s!" % user_name
            response_text = "<script>alert('{}');window.location='/doctorHome'</script>".format(alert_message)

            return HttpResponse(response_text)
        elif logOb.type == 'patient':
            request.session['lid'] = logOb.id
            ob1 = auth.authenticate(username='admin', password='admin')  # for login authentication
            auth.login(request, ob1)  # for login authentication
            user_name = logOb.username
            alert_message = f"welcome, {user_name}!"
            response_text = f"<script>alert('{alert_message}');window.location='/userHome'</script>"

            return HttpResponse(response_text)
        elif logOb.type == 'lab':
            request.session['lid'] = logOb.id
            ob1 = auth.authenticate(username='admin', password='admin')  # for login authentication
            auth.login(request, ob1)  # for login authentication
            user_name = logOb.username
            alert_message = f"welcome, {user_name}!"
            response_text = f"<script>alert('{alert_message}');window.location='/labHome'</script>"

            return HttpResponse(response_text)
        else:
            return HttpResponse('''<script>alert("invalid username or password ");window.location='/'</script>''')
    except:
        return HttpResponse('''<script>alert("invalid username or password ");window.location='/'</script>''')


################  ADMIN   ##################
@login_required(login_url='/') #for login authentication
def adminHome(request):
    return render(request, 'AdminIndex_inner.html')

@login_required(login_url='/') #for login authentication
def blockUnblockHospital(request):
    hob = hospital.objects.all()
    return render(request, 'admin/BlockUnblockHospital.html',{'val':hob})

@login_required(login_url='/') #for login authentication
def blockHospital(request,id):
    lob = login.objects.get(id=id)
    lob.type = 'blocked'
    lob.save()
    return HttpResponse('''<script>alert("hospital blocked");window.location="/blockUnblockHospital"</script>''')

@login_required(login_url='/') #for login authentication
def unblockHospital(request,id):
    lob = login.objects.get(id=id)
    lob.type = 'hospital'
    lob.save()
    return HttpResponse('''<script>alert("hospital unblocked");window.location="/blockUnblockHospital"</script>''')


@login_required(login_url='/') #for login authentication
def viewComp(request):
    cob = complaint.objects.all()
    return render(request, 'admin/VIEW_COMPLAINT.html',{'val':cob})

@login_required(login_url='/') #for login authentication
def sendReplyComp(request,id):
    request.session['rid'] = id
    return render(request, 'admin/sendCompReply.html')

@login_required(login_url='/') #for login authentication
def send_Reply_Comp(request):
    reply = request.POST['textarea']
    cob = complaint.objects.get(id=request.session['rid'])
    cob.reply = reply
    cob.date = datetime.today()
    cob.save()
    return HttpResponse('''<script>alert("reply sent");window.location="/viewComp"</script>''')

@login_required(login_url='/') #for login authentication
def verifyHospital(request):
    hob = hospital.objects.all()
    return render(request, 'admin/VerifyHospital.html',{'val':hob})

@login_required(login_url='/') #for login authentication
def acceptHospital(request,id):
    lob = login.objects.get(id=id)
    lob.type = 'hospital'
    lob.save()
    return HttpResponse('''<script>alert("hospital accepted");window.location="/verifyHospital"</script>''')

@login_required(login_url='/') #for login authentication
def rejectHospital(request,id):
    lob = login.objects.get(id=id)
    lob.type = 'rejected'
    lob.save()
    return HttpResponse('''<script>alert("hospital rejected");window.location="/verifyHospital"</script>''')

@login_required(login_url='/') #for login authentication
def viewPatient(request):
    pob = patient.objects.all()
    return render(request, 'admin/viewPatient.html',{'val':pob})


################  Hospital   ##################

@login_required(login_url='/') #for login authentication
def hospitalHome(request):
    hob = hospital.objects.get(lid__id=request.session['lid'])
    return render(request, 'hospitalIndex.html',{'val':hob})

@login_required(login_url='/') #for login authentication
def manageFacilities(request):
    hid = hospital.objects.get(lid__id=request.session['lid'])
    fob = facilities.objects.select_related('hid').filter(hid=hid)
    # message = request.GET.get('message') # get the message parameter from the request
    return render(request, 'hospital/MANAGE_FACILITY.html',{'val':fob})

@login_required(login_url='/') #for login authentication
def addFacilities(request):

    return render(request, 'hospital/ADD_FACILITY.html')

@login_required(login_url='/') #for login authentication
def add_facilities(request):
    name = request.POST['facname']
    desc = request.POST['desc']
    img = request.FILES['image']
    Fp = FileSystemStorage()
    Fs = Fp.save(img.name, img)
    capacity = request.POST['cap']
    availability = request.POST['select']
    location = request.POST['select2']
    fob = facilities()
    fob.name = name
    fob.description = desc
    fob.image = Fs
    fob.capacity = capacity
    fob.availability = availability
    fob.location = location
    fob.hid = hospital.objects.get(lid__id=request.session['lid'])
    fob.save()
    # add a success message to the messages framework
    messages.success(request, 'Facility added')
    # return HttpResponse('''<script>alert("Facility added");window.location="/manageFacilities"</script>''')
    return redirect('/manageFacilities')


@login_required(login_url='/') #for login authentication
def editFacilities(request,id):
    fob = facilities.objects.get(id=id)
    request.session['efid'] = id
    return render(request, 'hospital/EDIT_FACILITY.html',{'val':fob})

@login_required(login_url='/') #for login authentication
def updateFacilities(request):
    try:
        facname = request.POST['facname']
        desc = request.POST['desc']
        img = request.FILES['fileField']
        Fp = FileSystemStorage()
        Fs = Fp.save(img.name, img)
        capacity = request.POST['cap']
        availability = request.POST['select']
        location = request.POST['select2']
        fob = facilities.objects.get(id=request.session['efid'])
        fob.name = facname
        fob.description = desc
        fob.image = Fs
        fob.capacity = capacity
        fob.availability = availability
        fob.location = location
        fob.hid = hospital.objects.get(lid__id=request.session['lid'])
        fob.save()
        return HttpResponse('''<script>alert("Facility updated");window.location="/manageFacilities"</script>''')
    except:
        facname = request.POST['facname']
        desc = request.POST['desc']
        capacity = request.POST['cap']
        availability = request.POST['select']
        location = request.POST['select2']
        fob = facilities.objects.get(id=request.session['efid'])
        fob.name = facname
        fob.description = desc
        fob.capacity = capacity
        fob.availability = availability
        fob.location = location
        fob.hid = hospital.objects.get(lid__id=request.session['lid'])
        fob.save()
        return HttpResponse('''<script>alert("Facility updated");window.location="/manageFacilities"</script>''')

@login_required(login_url='/') #for login authentication
def delFacility(request,id):
    fob = facilities.objects.get(id=id)
    fob.delete()
    return HttpResponse('''<script>alert("Facility deleted");window.location="/manageFacilities"</script>''')

@login_required(login_url='/') #for login authentication
def manageDepartment(request):
    hid = hospital.objects.get(lid__id=request.session['lid'])
    dob = department.objects.select_related('hid').filter(hid=hid)
    return render(request, 'hospital/MANAGE_DEPARTMENT.html',{'val':dob})

@login_required(login_url='/') #for login authentication
def addDepartment(request):
    return render(request, 'hospital/ADD_DEPARTMENT.html')

@login_required(login_url='/') #for login authentication
def add_department(request):
    depName = request.POST['depname']
    description = request.POST['textarea']
    dob = department()
    dob.depName = depName
    dob.description = description
    dob.hid = hospital.objects.get(lid__id=request.session['lid'])
    dob.save()
    return HttpResponse('''<script>alert("department added");window.location="/manageDepartment"</script>''')

@login_required(login_url='/') #for login authentication
def editDepartment(request,id):
    dob = department.objects.get(id=id)
    request.session['edid'] = id
    return render(request, 'hospital/EDIT_DEPARTMENT.html',{'val':dob})

@login_required(login_url='/') #for login authentication
def updateDepartment(request):
    name = request.POST['textfield']
    description = request.POST['textarea']
    dob = department.objects.get(id=request.session['edid'])
    dob.depName = name
    dob.description = description
    dob.hid = hospital.objects.get(lid__id=request.session['lid'])
    dob.save()
    return HttpResponse('''<script>alert("department updated");window.location="/manageDepartment"</script>''')

@login_required(login_url='/') #for login authentication
def delDepartment(request,id):
    dob = department.objects.get(id=id)
    dob.delete()
    return HttpResponse('''<script>alert("department deleted");window.location="/manageDepartment"</script>''')

@login_required(login_url='/') #for login authentication
def manageDoctor(request):
    hid = hospital.objects.get(lid__id=request.session['lid'])
    docOb = doctor.objects.select_related('hid').filter(hid=hid)
    return render(request, 'hospital/MANAGE_DOCTORS.html',{'val':docOb})

@login_required(login_url='/') #for login authentication
def addDoctor(request):
    hid = hospital.objects.get(lid__id=request.session['lid'])
    dob = department.objects.select_related('hid').filter(hid=hid)
    print(dob)
    return render(request, 'hospital/ADD_DOCTORS.html',{'val':dob})

@login_required(login_url='/') #for login authentication
def add_doctor(request):
    try:
        fname = request.POST['fname']
        lname = request.POST['lname']
        gender = request.POST['radio']
        phone = request.POST['tel']
        email = request.POST['email']
        depid = request.POST['dep']
        pprint('//////////////')
        pprint(depid)
        pprint('//////////////')
        username = request.POST['uname']
        password = request.POST['password']
        lob = login()
        lob.username = username
        lob.password = password
        lob.type = 'doctor'
        lob.save()
        docOb = doctor()
        docOb.fname = fname
        docOb.lname = lname
        docOb.gender = gender
        docOb.phone = phone
        docOb.email = email
        docOb.hid = hospital.objects.get(lid__id=request.session['lid'])
        docOb.depId = department.objects.get(id=depid)
        docOb.lid = lob
        docOb.save()
        return HttpResponse('''<script>alert("doctor added");window.location="/manageDoctor"</script>''')
    except:
        return HttpResponse('''<script>alert("username already exists");window.location="/manageDoctor"</script>''')


def docExist(request):
    username = request.GET['uname']
    data = {
        'is_taken': doctor.objects.filter(lid__username__iexact=username).exists()
    }
    if data['is_taken']:
        data['error_message'] = "a user with username already exists"

    return JsonResponse(data)


@login_required(login_url='/') #for login authentication
def editDoctor(request,id):
    docOb = doctor.objects.get(id=id)
    hid = hospital.objects.get(lid__id=request.session['lid'])
    dob = department.objects.select_related('hid').filter(hid=hid)
    request.session['edocid'] = id
    return render(request, 'hospital/EDIT_DOCTOR.html',{'val':docOb,'val2':dob})

@login_required(login_url='/') #for login authentication
def updateDoctor(request):
    try:
        fname = request.POST['fname']
        lname = request.POST['lname']
        gender = request.POST['radio']
        phone = request.POST['tel']
        email = request.POST['email']
        depid = request.POST['select2']
        pprint('//////////////')
        pprint(depid)
        pprint('//////////////')
        docOb = doctor.objects.get(id=request.session['edocid'])
        docOb.fname = fname
        docOb.lname = lname
        docOb.gender = gender
        docOb.phone = phone
        docOb.email = email
        docOb.depId = department.objects.get(id=depid)
        docOb.hid = hospital.objects.get(lid__id=request.session['lid'])
        docOb.save()
        return HttpResponse('''<script>alert("doctor updated");window.location="/manageDoctor"</script>''')
    except:
        fname = request.POST['fname']
        lname = request.POST['lname']
        gender = request.POST['radio']
        phone = request.POST['tel']
        email = request.POST['email']
        # depid = request.POST['select2']
        pprint('//////////////')
        # pprint(depid)
        pprint('//////////////')
        docOb = doctor.objects.get(id=request.session['edocid'])
        docOb.fname = fname
        docOb.lname = lname
        docOb.gender = gender
        docOb.phone = phone
        docOb.email = email
        # docOb.depId = department.objects.get(id=depid)
        docOb.hid = hospital.objects.get(lid__id=request.session['lid'])
        docOb.save()
        return HttpResponse('''<script>alert("doctor updated");window.location="/manageDoctor"</script>''')

@login_required(login_url='/') #for login authentication
def delDoc(request,id):
    ob = doctor.objects.get(lid__id=id)
    ob.delete()
    lob = login.objects.get(id=id)
    lob.delete()
    return HttpResponse('''<script>alert("doctor deleted");window.location="/manageDoctor"</script>''')


@login_required(login_url='/') #for login authentication
def viewSchedule(request):
    hosId = hospital.objects.get(lid__id=request.session['lid'])
    sob= schedule.objects.filter(docId__hid=hosId)
    # sob= schedule.objects.filter(docId__hid__lid__id= request.session['lid'])
    return render(request, 'hospital/VIEW_SCHEDULE.html',{'val':sob})

@login_required(login_url='/') #for login authentication
def viewBooking(request):
    hosId = hospital.objects.get(lid__id=request.session['lid'])
    bob = booking.objects.filter(scheId__docId__hid=hosId)
    # bob = booking.objects.filter(scheId__docId__hid__lid__id= request.session['lid'])
    return render(request, 'hospital/VIEW_BOOKING.html',{'val':bob})

@login_required(login_url='/') #for login authentication
def manageLab(request):
    lob = lab.objects.filter(hid__lid__id=request.session['lid'])
    return render(request, 'hospital/MANAGE_LAB.html',{'val':lob})

@login_required(login_url='/') #for login authentication
def addLab(request):
    return render(request, 'hospital/ADD_LAB.html')

@login_required(login_url='/') #for login authentication
def add_lab(request):
    try:
        labName = request.POST['labname']
        description = request.POST['desc']
        img = request.FILES['fileField']
        Fp = FileSystemStorage()
        Fs = Fp.save(img.name, img)
        location = request.POST['select']
        capacity = request.POST['cap']
        availability = request.POST['select2']
        username = request.POST['uname']
        password = request.POST['password']
        lob = login()
        lob.username = username
        lob.password = password
        lob.type = 'lab'
        lob.save()
        ob = lab()
        ob.name = labName
        ob.description = description
        ob.location = location
        ob.image = Fs
        ob.capacity = capacity
        ob.availability = availability
        ob.hid = hospital.objects.get(lid__id=request.session['lid'])
        ob.lid = lob
        ob.save()
        return HttpResponse('''<script>alert("lab added");window.location="/manageLab"</script>''')
    except:
        return HttpResponse('''<script>alert("username already exists");window.location="/manageLab"</script>''')


@login_required(login_url='/') #for login authentication
def editLab(request,id):
    lob = lab.objects.get(id=id)
    request.session['elob'] = id
    return render(request, 'hospital/EDIT_LAB.html',{'val':lob})

@login_required(login_url='/') #for login authentication
def updateLab(request):
    try:
        labname = request.POST['labname']
        desc = request.POST['desc']
        img = request.FILES['fileField']
        Fp = FileSystemStorage()
        Fs = Fp.save(img.name, img)
        capacity = request.POST['cap']
        availability = request.POST['select2']
        location = request.POST['select']
        lob = lab.objects.get(id=request.session['efid'])
        lob.name = labname
        lob.description = desc
        lob.image = Fs
        lob.capacity = capacity
        lob.availability = availability
        lob.location = location
        lob.hid = hospital.objects.get(lid__id=request.session['lid'])
        lob.save()
        return HttpResponse('''<script>alert("lab updated");window.location="/manageLab"</script>''')
    except:
        labname = request.POST['labname']
        desc = request.POST['desc']
        # img = request.FILES['fileField']
        # Fp = FileSystemStorage()
        # Fs = Fp.save(img.name, img)
        capacity = request.POST['cap']
        availability = request.POST['select2']
        location = request.POST['select']
        lob = lab.objects.get(id=request.session['efid'])
        lob.name = labname
        lob.description = desc
        # lob.image = Fs
        lob.capacity = capacity
        lob.availability = availability
        lob.location = location
        lob.hid = hospital.objects.get(lid__id=request.session['lid'])
        lob.save()
        return HttpResponse('''<script>alert("lab updated");window.location="/manageLab"</script>''')

@login_required(login_url='/') #for login authentication
def delLab(request,id):
    lob = lab.objects.get(lid__id=id)
    lob.delete()
    logOb = login.objects.get(id=id)
    logOb.delete()
    return HttpResponse('''<script>alert("lab deleted");window.location="/manageLab"</script>''')


################  patient   ##################

@login_required(login_url='/') #for login authentication
def userHome(request):
    patOb = patient.objects.get(lid__id=request.session['lid'])
    pprint('////////////')
    pprint(patOb)
    pprint('////////////')

    return render(request, 'patientIndex.html',{'val':patOb})

@login_required(login_url='/') #for login authentication
def searchHospital(request):
    hob = hospital.objects.all()
    return render(request, 'patient/SEARCH_HOSPITAL.html',{'val':hob})

@login_required(login_url='/') #for login authentication
def search_hospital(request):
    Hob = request.POST['select']
    ob = hospital.objects.filter(id=Hob)
    hob = hospital.objects.all()
    return render(request, 'patient/SEARCH_HOSPITAL.html', {'val2': ob,'val':hob,'s':Hob})

@login_required(login_url='/') #for login authentication
def viewDoctor(request,id):
    dob = doctor.objects.filter(hid=id)
    return render(request, 'patient/VIEW_DOCTOR.html',{'val':dob})

@login_required(login_url='/') #for login authentication
def viewFacility(request,id):
    fob = facilities.objects.filter(hid=id)
    return render(request, 'patient/VIEW_FACILITY.html',{'val':fob})

@login_required(login_url='/') #for login authentication
def viewPatSchedule(request,id):
    sob = schedule.objects.filter(docId=id)
    return render(request, 'patient/VIEW_SCHEDULE.html',{'val':sob})

@login_required(login_url='/') #for login authentication
def book_shed(request,id):
    scheid = schedule.objects.get(id=id)
    # schedules = get_object_or_404(schedule, pk=scheid)
    dat = scheid.date
    start_time = scheid.startTime
    endTime = scheid.endTime
    ob = booking()
    ob.scheId = scheid
    ob.date = dat
    ob.timeStart = start_time
    ob.timeEnd = endTime
    ob.status = 'pending'
    ob.patId = patient.objects.get(lid__id=request.session['lid'])
    ob.save()
    return HttpResponse('''<script>alert("slot booked");window.location="/searchHospital"</script>''')

@login_required(login_url='/') #for login authentication
def book(request):
    sob = schedule.objects.all()
    return render(request, 'patient/BOOK.html',{'val':sob})

@login_required(login_url='/') #for login authentication
def Book(request):
    scheid = request.POST['select']
    ob = schedule.objects.filter(id=scheid)
    sob = schedule.objects.all()
    bob = booking.objects.all()
    return render(request, 'patient/BOOK.html', {'val': sob,'val2':ob,'s':scheid,'val3':bob})

@login_required(login_url='/') #for login authentication
def bookSlot(request):
    scheid = request.POST['select']
    schedules = get_object_or_404(schedule, pk=scheid)
    dat = schedules.date
    start_time = schedules.startTime
    endTime = schedules.endTime
    ob = booking()
    ob.scheId = schedule.objects.get(id=scheid)
    ob.patId = patient.objects.get(lid__id=request.session['lid'])
    ob.date = dat
    ob.timeStart = start_time
    ob.timeEnd = endTime
    ob.status = 'pending'
    ob.save()
    return HttpResponse('''<script>alert("slot booked");window.location="/book"</script>''')

@login_required(login_url='/') #for login authentication
def viewBookStatus(request):
    patid = patient.objects.get(lid__id=request.session['lid'])
    ob = booking.objects.filter(patId=patid.id)
    return render(request, 'patient/BOOKING_STATUS_USER.html',{'val':ob})


@login_required(login_url='/') #for login authentication
def viewSuggestedLab(request):
    patid = patient.objects.get(lid__id=request.session['lid'])
    sugOb = suggest.objects.filter(patId=patid.id)
    return render(request, 'patient/VIEW_SUG_LAB_APPLY.html',{'val':sugOb})

@login_required(login_url='/') #for login authentication
def applySuggLab(request,id):
    sugOb = get_object_or_404(suggest, id=id)
    docName = sugOb.docId
    testName = sugOb.labtesId
    apOb = labTestApplication()
    apOb.patId = patient.objects.get(lid__id=request.session['lid'])
    apOb.docId = docName
    apOb.testId = testName
    apOb.dateApplied = datetime.today()
    apOb.status = 'applied'
    apOb.save()
    sugOb.status = 'applied'
    sugOb.save()
    return HttpResponse('''<script>alert("applied to the lab");window.location="/viewSuggestedLab"</script>''')

@login_required(login_url='/') #for login authentication
def sendComp(request):

    return render(request, 'patient/SEND_COMP.html')

@login_required(login_url='/') #for login authentication
def add_comp(request):
    comp = request.POST['textarea']
    cob = complaint()
    cob.patId = patient.objects.get(lid__id=request.session['lid'])
    cob.complaint = comp
    cob.date = datetime.today()
    cob.save()
    return HttpResponse('''<script>alert("Complaint added");window.location="/viewRep"</script>''')

@login_required(login_url='/') #for login authentication
def viewRep(request):
    patid = patient.objects.get(lid__id=request.session['lid'])
    cob = complaint.objects.filter(patId=patid.id)
    return render(request, 'patient/VIEW_REPLY.html',{'val':cob})

@login_required(login_url='/') #for login authentication
def viewDownldPrescription(request):
    patid = patient.objects.get(lid__id=request.session['lid'])
    prescriptions = prescription.objects.filter(patId=patid)
    return render(request, 'patient/VIEW_DWNLD_PRESCRIPTION.html',{'prescriptions': prescriptions})


# def download_pdf(request, pk):
#     # Retrieve the object from the database
#     obj = prescription.objects.get(pk=pk)
#
#     # Generate the PDF file
#     buffer = BytesIO()
#     pdf = canvas.Canvas(buffer)
#     pdf.setTitle(f"Prescription - {obj.date.strftime('%m/%d/%Y')}")
#
#     # Add content to the PDF file
#     pdf.drawString(100, 750, "Doctor Name: {}".format(obj.docId.name))
#     pdf.drawString(100, 700, "Patient Name: {}".format(obj.patId.name))
#     pdf.drawString(100, 650, "Date: {}".format(obj.date.strftime('%m/%d/%Y')))
#     pdf.drawString(100, 600, "Diagnosis: {}".format(obj.diagnosis))
#     pdf.drawString(100, 550, "Medication: {}".format(obj.medication))
#     pdf.drawString(100, 500, "Dosage: {}".format(obj.dosage))
#     pdf.drawImage(obj.image.path, 100, 250)
#
#     # Close the PDF file and return the response
#     pdf.showPage()
#     pdf.save()
#     buffer.seek(0)
#     return FileResponse(buffer, as_attachment=True, filename=f"prescription_{obj.date.strftime('%m_%d_%Y')}.pdf")

# def generate_pdf(request):
#     # Get prescription data from the database
#     prescriptions = prescription.objects.all()
#
#     # Get the HTML template for the report
#     template = get_template('VIEW_DWNLD_PRESCRIPTION.html')
#     html = template.render({'prescriptions': prescriptions})
#
#     # Generate the PDF
#     response = HttpResponse(content_type='application/pdf')
#     response['Content-Disposition'] = 'attachment; filename="prescriptions.pdf"'
#     HTML(string=html, base_url=request.build_absolute_uri()).write_pdf(response, stylesheets=[settings.STATIC_ROOT + '/css/style.css'])
#
#     return response
# path to your wkhtmltopdf.exe file
wkhtml_to_pdf = os.path.join(
    settings.BASE_DIR, "wkhtmltopdf.exe")


@login_required(login_url='/') #for login authentication
def download_prescription(request, id):
    # Get the prescription object
    prescription_obj = prescription.objects.get(id=id)

    # Define the PDF document object
    pdf = FPDF()
    pdf.add_page()

    # Set font and font size
    pdf.set_font('Arial', '', 12)

    # Add doctor name to the PDF
    pdf.cell(30, 10, 'Doctor Name: ', 0)
    pdf.cell(60, 10, prescription_obj.docId.fname + ' ' + prescription_obj.docId.lname, 0)
    pdf.ln()

    # Add diagnosis to the PDF
    pdf.cell(30, 10, 'Diagnosis: ', 0)
    pdf.cell(60, 10, prescription_obj.diagnosis, 0)
    pdf.ln()

    # Add medication to the PDF
    pdf.cell(30, 10, 'Medication: ', 0)
    pdf.cell(60, 10, prescription_obj.medication, 0)
    pdf.ln()

    # Add dosage to the PDF
    pdf.cell(30, 10, 'Dosage: ', 0)
    pdf.cell(60, 10, prescription_obj.dosage, 0)
    pdf.ln()

    # Add image to the PDF
    if prescription_obj.image:
        image_path = os.path.join(settings.MEDIA_ROOT, str(prescription_obj.image))
        pdf.image(image_path, w=100, h=100)
        pdf.ln()

    # Set the filename of the PDF file
    filename = f'prescription_{prescription_obj.id}.pdf'

    # Create the HTTP response as a PDF file attachment
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="{filename}"'

    # Output the PDF to the response
    response.write(pdf.output(dest='S').encode('latin1'))

    return response


@login_required(login_url='/') #for login authentication
def viewReport(request):
    patid = patient.objects.get(lid__id=request.session['lid'])
    laOb = labReport.objects.filter(appId__patId=patid.id)
    return render(request, 'patient/VIEW_REPORT.html',{'laOb': laOb})


################  LAB   ##################

@login_required(login_url='/') #for login authentication
def labHome(request):
    labOb = lab.objects.get(lid__id=request.session['lid'])
    return render(request, 'labIndex.html',{'val':labOb})

@login_required(login_url='/') #for login authentication
def viewDrSugg(request):
    did = doctor.objects.all()
    labid = lab.objects.get(lid__id=request.session['lid'])
    suggOb = suggest.objects.filter(labtesId__labId=labid, docId__hid__in=did.values_list('hid', flat=True))
    return render(request, 'lab/VIEW_DOCTOR_SUGGESTIONS.html',{'val':suggOb})

@login_required(login_url='/') #for login authentication
def manageReport(request):
    labid = lab.objects.get(lid__id=request.session['lid'])
    # labRepOb = labReport.objects.filter(appId__docId__hid=labid.hid, appId__testId__labId__hid=labid.hid)
    labRepOb = labTestApplication.objects.filter(docId__hid=labid.hid)
    # labrep = [get_object_or_404(labReport, appId=app.id) for app in labRepOb]
    # labrep = []
    # for rep in labRepOb:
    #     labrep.append(labReport.objects.filter(appId=rep.id))
    # val = labRepOb
    # val2 = labrep
    # zipped_results = zip(val, val2)
    # context = {'zipped_results': zipped_results}
    return render(request, 'lab/MANAGE_REPORT.html',{'val':labRepOb})

@login_required(login_url='/') #for login authentication
def addReport(request,id):
    request.session['elrpid'] = id
    return render(request, 'lab/ADD_REPORT.html')

@login_required(login_url='/') #for login authentication
def add_report(request):
    rep = request.POST['textarea']
    labrepob = labReport()
    labrepob.appId = labTestApplication.objects.get(id=request.session['elrpid'])
    labrepob.dateReported = datetime.today()
    labrepob.result = rep
    labrepob.save()
    lob = labTestApplication.objects.get(id=request.session['elrpid'])
    lob.status = 'reported'
    lob.save()
    return HttpResponse('''<script>alert("report added");window.location="/manageReport"</script>''')


@login_required(login_url='/') #for login authentication
def editReport(request,id):
    lob = labReport.objects.get(id=id)
    request.session['rid'] = id
    return render(request, 'lab/EDIT_REPORT.html',{'val':lob})

@login_required(login_url='/') #for login authentication
def updateReport(request):
    rep = request.POST['textarea']
    lob = labReport.objects.get(id=request.session['rid'])
    lob.result = rep
    lob.dateReported = datetime.today()
    lob.save()
    return HttpResponse('''<script>alert("report updated");window.location="/manageReport"</script>''')

@login_required(login_url='/') #for login authentication
def view_report(request,id):
    lob = labReport.objects.get(id=id)

    return render(request,'lab/viewReport.html',{'val':lob})

@login_required(login_url='/') #for login authentication
def manageLabtest(request):
    labid = lab.objects.get(lid__id=request.session['lid'])
    labtId  = labTests.objects.filter(labId__hid=labid.hid)
    return render(request, 'lab/MANAGE_LABTEST.html',{'val':labtId})

@login_required(login_url='/') #for login authentication
def addLabTest(request):
    return render(request, 'lab/ADD_LAB_TEST.html')

@login_required(login_url='/') #for login authentication
def add_labtest(request):
    testName = request.POST['name']
    des = request.POST['desc']
    phone = request.POST['tel']
    email = request.POST['email']
    ob = labTests()
    ob.name = testName
    ob.description = des
    ob.contact = phone
    ob.email = email
    ob.labId = lab.objects.get(lid__id=request.session['lid'])
    ob.save()
    return HttpResponse('''<script>alert("test added");window.location="/manageLabtest"</script>''')

@login_required(login_url='/') #for login authentication
def delLabtest(request,id):
    lob = labTests.objects.get(id=id)
    lob.delete()
    return HttpResponse('''<script>alert("test deleted");window.location="/manageLabtest"</script>''')


################  DOCTOR   ##################
@login_required(login_url='/') #for login authentication
def doctorHome(request):
    docOb = doctor.objects.get(lid__id=request.session['lid'])
    return render(request, 'doctorIndex.html',{'val':docOb})

@login_required(login_url='/') #for login authentication
def manageSchedule(request):
    sob = schedule.objects.filter(docId__lid__id=request.session['lid'])
    return render(request, 'doctor/MANAGE_SCHEDULE.html',{'val':sob})

@login_required(login_url='/') #for login authentication
def addSchedule(request):
    return render(request, 'doctor/ADD_SCHEDULE.html')

@login_required(login_url='/') #for login authentication
def add_schedule(request):
    shcDate = request.POST['date']
    Date = datetime.strptime(shcDate, '%Y-%m-%d')
    shcsTtime = request.POST['time']
    shceTtime = request.POST['time2']
    shcsTtime_str = f"{shcDate} {shcsTtime}"
    shceTtime_str = f"{shcDate} {shceTtime}"
    start_datetime = timezone.make_aware(datetime.strptime(shcsTtime_str, '%Y-%m-%d %H:%M'))
    end_datetime = timezone.make_aware(datetime.strptime(shceTtime_str, '%Y-%m-%d %H:%M'))
    maxappoint = request.POST['number']
    sob = schedule()
    sob.date = Date
    sob.startTime = start_datetime
    sob.endTime = end_datetime
    sob.maxAppointment = maxappoint
    sob.docId = doctor.objects.get(lid__id=request.session['lid'])
    sob.save()
    return HttpResponse('''<script>alert("schedule added");window.location="/manageSchedule"</script>''')

@login_required(login_url='/') #for login authentication
def editSchedule(request,id):
    sob = schedule.objects.get(id=id)
    request.session['esid'] = id
    return render(request, 'doctor/EDIT SCHEDULE.html',{'val':sob})

@login_required(login_url='/') #for login authentication
def updateSchedule(request):
    Date = request.POST['date']
    Date_frmt = datetime.strptime(Date, '%Y-%m-%d')
    starttime = request.POST['time']
    starttime_frmt = datetime.strptime(starttime, '%H:%M')
    endtime = request.POST['time2']
    endtime_frmt = datetime.strptime(endtime, '%H:%M')
    maxappoint = request.POST['number']
    sob = schedule.objects.get(id=request.session['esid'])
    sob.date = Date_frmt
    sob.startTime = starttime_frmt
    sob.endTime = endtime_frmt
    sob.maxAppointment = maxappoint
    sob.docId = doctor.objects.get(lid__id=request.session['lid'])
    sob.save()
    return HttpResponse('''<script>alert("schedule updated");window.location="/manageSchedule"</script>''')

@login_required(login_url='/') #for login authentication
def delSchedule(request,id):
    sob = schedule.objects.get(id=id)
    sob.delete()
    return HttpResponse('''<script>alert("schedule deleted");window.location="/manageSchedule"</script>''')

@login_required(login_url='/') #for login authentication
def viewBookingUpdate(request):
    bob = booking.objects.filter(scheId__docId__lid__id=request.session['lid'])
    return render(request, 'doctor/VIEW_BOOKING_UPDATE.html',{'val':bob})

@login_required(login_url='/') #for login authentication
def appointBook(request,id):
    bob = booking.objects.get(id=id)
    bob.status = 'appointed'
    bob.save()
    return HttpResponse('''<script>alert("patient appointed");window.location="/viewBookingUpdate"</script>''')

@login_required(login_url='/') #for login authentication
def rejectBook(request,id):
    bob = booking.objects.get(id=id)
    bob.status = 'rejected'
    bob.save()
    return HttpResponse('''<script>alert("patient rejected");window.location="/viewBookingUpdate"</script>''')


@login_required(login_url='/') #for login authentication
def managePrescription(request):
    pob = prescription.objects.filter(docId__lid__id=request.session['lid'])
    return render(request, 'doctor/MANAGE_PRESCRIPTION.html',{'val':pob})

@login_required(login_url='/') #for login authentication
def uploadPrescription(request):
    pob = patient.objects.all()
    return render(request, 'doctor/UPLOAD_PRESCRIPTION.html',{'val':pob})

@login_required(login_url='/') #for login authentication
def addPrescription(request):
    patName = request.POST['select']
    img = request.FILES['fileField']
    Fp = FileSystemStorage()
    Fs = Fp.save(img.name, img)
    diagnosis = request.POST['diag']
    medication = request.POST['medic']
    dosage = request.POST['dos']
    date = datetime.today()
    pob = prescription()
    pob.patId = patient.objects.get(id=patName)
    pob.docId = doctor.objects.get(lid__id=request.session['lid'])
    pob.diagnosis = diagnosis
    pob.medication = medication
    pob.dosage = dosage
    pob.image = Fs
    pob.date = date
    pob.save()
    return HttpResponse('''<script>alert("prescription added");window.location="/managePrescription"</script>''')

@login_required(login_url='/') #for login authentication
def delPresc(request,id):
    pob = prescription.objects.get(id=id)
    pob.delete()
    return HttpResponse('''<script>alert("prescription deleted");window.location="/managePrescription"</script>''')

@login_required(login_url='/') #for login authentication
def suggestLabAndLabtest(request):
    pob = patient.objects.all()
    did = doctor.objects.get(lid__id=request.session['lid'])
    # lob = lab.objects.filter(hid=did.hid)
    ltob = labTests.objects.filter(labId__hid=did.hid)
    pprint("//////////////////////////////")
    pprint(ltob)
    pprint("//////////////////////////////")
    return render(request, 'doctor/SUGGEST_LAB_LABTEST.html',{'val1':pob,'val3':ltob})

def viewSuggestedLabsAndLt(request):
    did = doctor.objects.get(lid__id=request.session['lid'])
    ob = suggest.objects.filter(docId=did)
    return render(request,'doctor/viewSuggestedLabs&Labtest.html',{'val':ob})

@login_required(login_url='/') #for login authentication
def suggestbtn(request):
    patid = request.POST['select']
    lbtid = request.POST['select3']
    sugOb = suggest()
    sugOb.docId = doctor.objects.get(lid__id=request.session['lid'])
    sugOb.patId = get_object_or_404(patient, pk=patid)
    sugOb.labtesId = get_object_or_404(labTests, pk=lbtid)
    sugOb.status = 'suggested'
    sugOb.save()
    return HttpResponse('''<script>alert("suggested");window.location="/suggestLabAndLabtest"</script>''')

@login_required(login_url='/') #for login authentication
def viewReportToDoc(request):
    did = doctor.objects.get(lid__id=request.session['lid'])
    lob = labReport.objects.filter(appId__docId=did.id)
    return render(request, 'doctor/VIEW_REPORT_TODOC.html',{'val':lob})


def forgotPass(request):
    return render(request,'forgotPassIndex.html')


def password_reset(request):
    uname = request.POST['uname']
    mail = request.POST['email']
    try:
        g = login.objects.get(username=uname)
        pprint('/////////////')
        pprint(g)
        pprint('/////////////')
        if g is not None:
            a = random.randint(0000, 9999)
            g.password = (str(a))
            g.save()
            send_mail('forgot password ', "YOUR NEW PASSWORD IS  -" + str(a), 'yadhusample1998@gmail.com', [mail],fail_silently=False)
            return HttpResponse('''<script>alert("Password sent to your registered email address !!!");window.location='/'</script>''')
            # return redirect('/')
        else:
            print('error==========')
            return HttpResponse(
                '''<script>alert("Invalid Username or Email Adress!!!");window.location='/forgotPass'</script>''')
            # return HttpResponse('''<script>alert("Invalid Username or Email Adress!!!")</script>''')
            # return redirect('forgotPass')
    except:
        return HttpResponse(
            '''<script>alert("Invalid Username or Email Adress!!!");window.location='/forgotPass'</script>''')
#

# logger = logging.getLogger(__name__)

# def password_reset(request):
#     if request.method != 'POST':
#         return HttpResponseBadRequest('Invalid request method')
#
#     username = request.POST.get('uname', '').strip()
#     email = request.POST.get('email', '').strip()
#
#     if not username or not email:
#         return HttpResponseBadRequest('Missing required parameters')
#
#     try:
#         user = login.objects.get(username=username)
#     except login.DoesNotExist:
#         logger.warning(f'Invalid username "{username}"')
#         return HttpResponseBadRequest('Invalid username or email address')
#
#     if user.email != email:
#         logger.warning(f'Invalid email address for user "{username}"')
#         return HttpResponseBadRequest('Invalid username or email address')
#
#     new_password = secrets.token_urlsafe(8)
#     hashed_password = make_password(new_password)
#     user.password = hashed_password
#     user.save()
#
#     subject = 'Password reset request'
#     message = f'Your new password is {new_password}. Please log in and change it immediately.'
#     sender = 'yadhusample1998@gmail.com'
#     recipient_list = [email]
#
#     try:
#         send_mail(subject, message, sender, recipient_list, fail_silently=False)
#     except Exception as e:
#         logger.exception(f'Error sending email: {str(e)}')
#         return HttpResponseServerError('Error sending password reset email')
#
#     return HttpResponse('Password reset email sent')


def logout(request):
    auth.logout(request)
    return redirect('/')