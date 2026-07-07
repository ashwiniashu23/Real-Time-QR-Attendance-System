from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse
from .models import UserProfile
from django.views.decorators.cache import never_cache
from django.contrib.auth.decorators import login_required
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib.sessions.models import Session
from .generator.otp import generate_otp
from .generator.qr import generate_qr
from .models import QRToken, UserProfile, AttendanceRecord
import os
from datetime import date
import math
from datetime import datetime as dt



# The uuid module allows you to generate a universally unique identifier.
# These UUIDs are nearly impossible to guess or duplicate, so they are a great way to identify things like devices, sessions, or users anonymously and securely.



# Create your views here.

email=""
otp=""
qrtoken = ""


# to be changed
from django.utils import timezone
from .models import UserProfile, AttendanceRecord

def mark_all_absent_for_new_day(request):
    today = timezone.localdate()

    # Check if attendance records exist for today
    records_for_today = AttendanceRecord.objects.filter(date=today)
    if records_for_today.exists():
        print("Attendance already set for today.")
        return redirect('view_attendance')

    # Get all userprofiles
    user_profiles = UserProfile.objects.all()

    # Create AttendanceRecord for each user with status "Absent"
    new_records = []
    for profile in user_profiles:
        record = AttendanceRecord(
            date=today,
            uucms=profile.uucms,
            user=profile.user.username,
            Attendance="Absent"
        )
        new_records.append(record)

    AttendanceRecord.objects.bulk_create(new_records)
    print(f"Marked all users absent for {today}.")
    return redirect('view_attendance')
    


def home(request):

    return render(request, 'index.html')

@never_cache
def Signin(request):
    if request.method == "POST":
        username = request.POST["username"].lower()  # this will take username from html page
        password = request.POST["password"]
        userunique = request.POST.get('unique', None)


        user = authenticate(username=username,password=password) # This will validate username and password with database
        print(user)



        if user is None:
            messages.error(request,"Bad Credentials")
            return redirect('signin')

        if user is not None:
            profile = user.userprofile
            unique = profile.unique



        # elif userheight!=height or userwidth!= width or userunique != unique:
        #     messages.error(request,"Don't try to access with different Device")
        #     return redirect('signin')
        try:
            staff = User.objects.get(username=username)
        except:
            staff = None
        if staff.is_staff:
            login(request, user)
            return redirect('dashboard')

        if userunique != unique:
            messages.error(request,"Don't try to access with different Device")
            return redirect('signin')

        else:
            print("Entered")
            login(request, user)
            return redirect('dashboard')
    return render(request,'signin.html')

@login_required
def dashboard(request):
    user = request.user
    name = user.get_full_name()
    return render(request, 'home.html',{"name":name,})




@never_cache
def SignOut(request):
    logout(request)  # This clears the session
    return redirect('signin')

def Signup(request):

    if request.method == "POST":

            username = request.POST['username'].lower()
            fname = request.POST['fname']
            lname = request.POST['lname']
            user_email = request.POST['email'].lower()
            user_otp = request.POST.get('otp', None)
            pass1 = request.POST['pass1']
            pass2 = request.POST['pass2']
            unique = request.POST.get('unique', None)
            uucms = request.POST.get('uucms',None)


            print(user_otp,otp)

            if User.objects.filter(username=username):
                return render(request, 'signup.html', {'message':'User name already exists. Try different user name','form_data': request.POST})

            if User.objects.filter(email=user_email):
                return render(request, 'signup.html', {'message':'Mail id is already registered. Please Sign up','form_data': request.POST})

            if user_otp == None:
                return render(request, 'signup.html', {"message":"Validate OTP",'form_data':request.POST})

            if email=="" or otp=="":
                return render(request,'signup.html',{'message':'Please verify your email id first'})

            if user_email != email:
                return render(request, 'signup.html', {"message":"Please Don't Try to Cheat Us! We are not fools",'form_data':request.POST})

            if len(pass1)<8 and len(pass2)<8:
                return render(request,'signup.html',{"message":"Password length should not be less than 8 ",'form_data': request.POST})


            if user_otp != otp:
                print(user_otp)
                return render(request, 'signup.html', {"message":"Incorrect OTP",'form_data':request.POST})

            if pass1 != pass2:
                return render(request, 'signup.html', {"message":"Password is not matching",'form_data': request.POST})



            myuser = User.objects.create_user(username,email)
            myuser.username = username
            myuser.first_name = fname
            myuser.last_name = lname
            myuser.email = user_email
            myuser.set_password(pass1)

            myuser.save()
            UserProfile.objects.create(user=myuser,unique=unique, uucms = uucms) # Assing heigt and widht to user

            messages.success(request,"Your account has been succesfully created")

            return render(request,'signin.html')

    return render(request, 'signup.html')


def delete():
    print("Entered Delete")
    # Set the path to the folder
    folder_path = r'C:\Users\Ashwini S\Desktop\QR Attendance\Attendance\static\QRCodes'

    # Get list of .png files sorted by creation time (oldest first)
    png_files = sorted(
        [f for f in os.listdir(folder_path) if f.lower().endswith('.png')],
        key=lambda f: os.path.getctime(os.path.join(folder_path, f))
    )

    # Check if there are more than 10 .png files
    if len(png_files) > 10:
        # Delete the first 2 .png files
        for file_to_delete in png_files[:8]:
            file_path = os.path.join(folder_path, file_to_delete)
            os.remove(file_path)
            print(f"Deleted: {file_path}")
    else:
        print("No need to delete files. Total PNG files:", len(png_files))



@login_required
def show_qr_token(request):
    if not request.user.is_staff:
        messages = {'message': "You are not a staff member"}
        return render(request,'display.html',messages)
    # Create a new QRToken object
    print(request.user.is_staff)
    delete()

    qr_token = QRToken.objects.create()

    # Generate the QR code image and save it in static/qrcode/
    qr_url = generate_qr(qr_token.token)

    context = {
        'token': qr_token.token,
        'qr_url': qr_url,  # Relative to static/
    }
    return render(request, 'qrcode.html', context)

def info(request):
    return render(request, "display.html")

def attendance_redirect(request, token):
    # If user is not authenticated, redirect to login with return path
    print(request.user.is_authenticated)
    if not request.user.is_authenticated:
        return redirect('signin')

    # Get the token object (404 if not found)
    qr_token = get_object_or_404(QRToken,token=token)

    # Check if the token is already scanned or inactive
    if not qr_token.is_active:
        return render(request, 'display.html', {'message': 'Token is inactive or already used.'})
    


    # Mark attendance
    qr_token.user = request.user
    qr_token.is_active = False
    qr_token.is_scanned = True
    qr_token.save()

    global qrtoken
    qrtoken = token
    return render(request,'location.html')

def mark_attendance(request):
    UUCMS = request.user.userprofile.uucms
    Date = date.today()
    print(UUCMS)
    print(Date)
    global qrtoken
    token = qrtoken




    is_present = AttendanceRecord.objects.filter(date = Date, uucms = UUCMS, Attendance = "Present").exists()
    if is_present:
        return render(request,"display.html",{'message':f"{request.user.get_full_name()}, your attendance is already registered",})
    is_absent = AttendanceRecord.objects.filter(date = Date, uucms = UUCMS, Attendance = "Absent").exists()
    if is_absent:
        record = AttendanceRecord.objects.filter(uucms = UUCMS, date = Date).first()
        record.Attendance = "Present"
        record.save()
        return render(request, 'display.html',{'message': f"{request.user.get_full_name()} Attendance Registered Successfully",'safe':True})
    AttendanceRecord.objects.create(uucms = UUCMS, token=token, user = request.user.get_full_name(), Attendance = "Present")

    return render(request, 'display.html',{'message': f"{request.user.get_full_name()} Attendance Registered Successfully", 'safe':True})



# Change required
@login_required
def attendance_view(request):
    if request.method == "GET":
        from_date = request.GET.get('from_date')
        to_date = request.GET.get('to_date')
        records = []

        if from_date and to_date:
            try:
                print(request.user)
                from_date_obj = dt.strptime(from_date, "%Y-%m-%d").date()
                to_date_obj = dt.strptime(to_date, "%Y-%m-%d").date()

                if request.user.is_staff:
                    # Staff: get all attendance records in the date range
                    records = AttendanceRecord.objects.filter(
                        date__range=(from_date_obj, to_date_obj)
                    ).order_by('date')
                else:
                    # Non-staff: get only this user's attendance records in date range
                    records = AttendanceRecord.objects.filter(
                        user=request.user.get_full_name(),
                        date__range=(from_date_obj, to_date_obj)
                    ).order_by('date')
            except ValueError:
                records = []

        return render(request, 'attendance_view.html', {
            'records': records,
            'from_date': from_date,
            'to_date': to_date,
        })

    return render(request, "attendance_view.html")
#Generating otp
def my_function(request):
    if request.method == "POST":
        # Your Python code here
        data = request.POST.get("custom_data", "No data recieved")
        # result = {"message": f"Hello Keshava Python function executed! Recieved: {data}"}
        global email, otp # Declare global variables first
        email = data.lower()
        otp = str(generate_otp(data))
        return JsonResponse({"Nothing":"Hello"})
    
def attendance_edit(request):
    if request.method == "GET":
        Date = request.GET.get('date')
        records = []

        if Date:
            try:
                print(request.user)
                Date = dt.strptime(Date, "%Y-%m-%d").date()

                if request.user.is_staff:
                    # Staff: get all attendance records in the date range
                    records = AttendanceRecord.objects.filter(date = Date).order_by('date')
            except ValueError:
                records = []
        print(Date)
        return render(request, 'attendance_edit.html', {
            'records': records,
            'date': Date,
        })
    if request.method == 'POST':
        Date = request.POST.get("date")
        
        Date = dt.strptime(Date, "%B %d, %Y").strftime("%Y-%m-%d")
        print(Date)
        for key,value in request.POST.items():

            if key in ['csrfmiddlewaretoken', 'date','None']:
                continue 
            print("Date Submitted to filter",Date)
            record = AttendanceRecord.objects.filter(uucms = key, date = Date).first()
            print(record)
            if record:
                record.Attendance = value
                record.save()
                if value == "Present":
                    print("Attendance Marked Successfully")
                else:
                    print("Attendance Removed Successfully")
            else:
                return render(request,'display.html',{"message":f"Record not found {record}"})

        
        return redirect('dashboard')

    return render(request, "attendance_edit.html")

@login_required
def location(request):
    if request.method == "POST":
        # classroomlat = 12.9564672 # Invalid in college
        # classroomlong = 77.594624 # Invalid in college
        classroomlat =13.041546 # Valid in college
        classroomlong = 77.524441 # Valid in college
        userlattitude = float(request.POST.get("lat"))
        userlongitude = float(request.POST.get("long"))
        allowedRadius = 200
        print(classroomlat,classroomlong,userlattitude,userlongitude)

        def get_distance_from_lat_lon_in_meters(lat1, lon1, lat2, lon2):
            R = 6371000  # Earth radius in meters
            dLat = math.radians(lat2 - lat1)
            dLon = math.radians(lon2 - lon1)
            a = (math.sin(dLat / 2) ** 2 +
                math.cos(math.radians(lat1)) * math.cos(math.radians(lat2)) *
                math.sin(dLon / 2) ** 2)
            c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
            return R * c
        distance = get_distance_from_lat_lon_in_meters(userlattitude,userlongitude,classroomlat,classroomlong)
        print(f"distance = {distance}")

        if distance <= allowedRadius:
            print("entered allowed")
            return mark_attendance(request)
            
        else:
            print("entered not allowed")
            return render(request,'display.html',{'message':f'❌ You are {round(distance)} meters away. Attendance not allowed.'})
    return render(request,'location.html')