from django.http import StreamingHttpResponse
from django.shortcuts import render,redirect ,get_object_or_404
from django.http import JsonResponse
from django.contrib import messages
from django import forms
from .models import StudentData , TeacherData ,AttendanceData ,SubjectData ,DatabaseAdministratorList ,DepartmentandSemestre ,StudentRegistration ,TeacherLectureData
from django.contrib.auth import login, authenticate
import cv2
import face_recognition
import numpy as np
import os
from datetime import datetime




# Create your views here.
def Login_Base(request):
    return render(request,'Login_Base.html')


def Student_Login(request):
    if request.method == "POST":
        StudentID = request.POST.get('StudentID')
        CollageCode = request.POST.get('CollageCode')
        Password = request.POST.get('Password')
        try:
            student = StudentData.objects.get(StudentID=StudentID)
            if student.CollageCode == CollageCode:  # For production, use hashed passwords
                if student.Password == Password:  # For production, use hashed passwords
                    request.session['StudentID'] = StudentID  # Store user ID in session
                    user = authenticate(request, StudentID=StudentID, Password=Password)
                    if user is not None:
                        login(request, user)
                        request.session['StudentID'] = user.studentprofile.StudentID  # Store StudentID in session
                        return redirect('Student_Home')  # Redirect to home page
                    #messages.success(request, "Login successful!")
                    return redirect('Student_Home')  # Redirect to a success page
                else:
                    messages.error(request, "Invalid Student ID or Password.")
            else:
                messages.error(request, "Invalid Student ID or CollageCode.")
        except StudentData.DoesNotExist:
            messages.error(request, "Invalid Student ID or Password.")
    return render(request,'Student_Login.html')

def Teacher_Login(request):
    if request.method == "POST":
        TeacherID = request.POST.get('TeacherID')
        CollageCode = request.POST.get('CollageCode')
        Password = request.POST.get('Password')
        try:
            teacher = TeacherData.objects.get(TeacherID=TeacherID)
            if teacher.CollageCode == CollageCode:  # For production, use hashed passwords
                if teacher.Password == Password:  # For production, use hashed passwords
                    request.session['TeacherID'] = TeacherID  # Store user ID in session
                    user = authenticate(request, TeacherID=TeacherID, Password=Password)
                    if user is not None:
                        login(request, user)
                        request.session['TeacherID'] = user.teacherprofile.TeacherID  # Store StudentID in session
                        return redirect('Teacher_Home')  # Redirect to home page
                #messages.success(request, "Login successful!")
                    return redirect('Teacher_Home')  # Redirect to a success page
                else:
                    messages.error(request, "Invalid User ID or CollageCode.")
            else:
                messages.error(request, "Invalid User ID or CollageCode.")
        except TeacherData.DoesNotExist:
            messages.error(request, "Invalid User ID or Password.")
    return render(request,'Teacher_Login.html')

#def Student_Registration(request):
#    DepartmentandSemestre1 = DepartmentandSemestre.objects.values_list('Department_Name', flat=True).distinct()
#    print('Meetb0811')
#    if request.method == "POST":
#        StudentID = request.POST.get('StudentID')
#        CollageCode = request.POST.get('CollageCode')
#        Student_Name = request.POST.get('Student_Name')
#        Semestre = request.POST.get('Semestre')
#        Department = request.POST.get('Department')
#        Email = request.POST.get('Email')
#        Mobile = request.POST.get('Mobile')
#        Password = request.POST.get('Password')
#        try:
#            student = StudentRegistration.objects.get(StudentID=StudentID)
#            if student.CollageCode == CollageCode:  # For production, use hashed passwords
#                if student.Department == Department:  # For production, use hashed passwords
#                    if StudentData.objects.filter(Email=Email).exists():
#                        messages.error(request, "Email already exists. Please choose another.")
#                    elif StudentData.objects.filter(Mobile=Mobile).exists():
#                        messages.error(request, "Mobile already exists. Please choose another.")
#                    else:
#                        StudentData.objects.create(StudentID=StudentID, Student_Name=Student_Name, CollageCode=CollageCode, Semestre=Semestre, Department=Department, Email=Email, Mobile=Mobile, Password=Password)
#                        def save(self):
#                            print(f"Data saved: {self.data}")
#                            StudentData.save()
#                            return redirect('Login_Base')  # Redirect to a success page
#                        return redirect('Login_Base')  # Redirect to a success page
#                else:
#                    messages.error(request, "Invalid Student ID or CollageCode or Department.")
                
#            else:
#                messages.error(request, "Invalid Student ID or CollageCode.")
#        except StudentRegistration.DoesNotExist:
#            messages.error(request, "Invalid Student ID or CollageCode.")
#        DepartmentandSemestre1 = DepartmentandSemestre.objects.values_list('Department_Name', flat=True).distinct()
#        return render(request,'Student_Registration.html',{'DepartmentandSemestre':DepartmentandSemestre1})
#    return render(request,'Student_Registration.html',{'DepartmentandSemestre':DepartmentandSemestre1})

def Student_Registration(request):
    DepartmentandSemestre1 = DepartmentandSemestre.objects.values_list('Department_Name', flat=True).distinct()
    
    if request.method == "POST":
        StudentID = request.POST.get('StudentID')
        CollageCode = request.POST.get('CollageCode')
        Student_Name = request.POST.get('Student_Name')
        Semestre = request.POST.get('Semestre')
        Department = request.POST.get('Department')
        Email = request.POST.get('Email')
        Mobile = request.POST.get('Mobile')
        Password = request.POST.get('Password')  # Note: Not hashed (bad for production)

        try:
            student = StudentRegistration.objects.get(StudentID=StudentID)
            if student.CollageCode == CollageCode and student.Department == Department:
                if StudentData.objects.filter(Email=Email).exists():
                    messages.error(request, "Email already exists. Please choose another.")
                elif StudentData.objects.filter(Mobile=Mobile).exists():
                    messages.error(request, "Mobile already exists. Please choose another.")
                else:
                    StudentData.objects.create(
                        StudentID=StudentID,
                        Student_Name=Student_Name,
                        CollageCode=CollageCode,
                        Semestre=Semestre,
                        Department=Department,
                        Email=Email,
                        Mobile=Mobile,
                        Password=Password  # ⚠️ Insecure: use hashed passwords for real apps
                    )
                    return redirect('Login_Base')
            else:
                messages.error(request, "Invalid Student ID, CollageCode or Department.")
        except StudentRegistration.DoesNotExist:
            messages.error(request, "Invalid Student ID or CollageCode.")

    return render(request, 'Student_Registration.html', {'DepartmentandSemestre': DepartmentandSemestre1})


def Student_Password_Forget1(request):
    print('Meet')
    if request.method == "POST":
        print('bameet11')
        StudentID = request.POST.get('StudentID')
        Email = request.POST.get('Email')
        print('bameet11')
        try:
            student = StudentData.objects.get(StudentID=StudentID)
            print('bameet11')
            if student.Email == Email:  # For production, use hashed passwords
                request.session['StudentID'] = StudentID  # Store user ID in session
                #messages.success(request, "Login successful!")
                return redirect('Student_Password_Forget_New')  # Redirect to a success page
            else:
                messages.error(request, "Invalid Student ID or Email.")
        except StudentData.DoesNotExist:
            messages.error(request, "Invalid Student ID or Email.")
    return render(request, 'Student_Password_Forget.html')
    

def Student_Password_Forget_New(request):
    StudentID = request.session.get('StudentID')
    PasswordChange = get_object_or_404(StudentData, StudentID=StudentID)
    if not StudentID:
        messages.error(request, 'Session expired. Please try again.')
        return redirect('Login_Base')
    if request.method == "POST":
        NewPassword = request.POST.get('Password')

        try:
            if NewPassword is not None:
                PasswordChange.Password = NewPassword
                PasswordChange.save()
                return redirect('Login_Base')

    #if NewPassword is not None:
        except StudentData.DoesNotExist:
            messages.error(request, 'Invalid user.')
            return redirect('Student_Password_Forget')
    return render(request,'Student_Password_Forget_New.html')

def Student_Home_Base(request):
    StudentID = request.session.get('StudentID')
    StudentData1 = get_object_or_404(StudentData, StudentID=StudentID)
    print(StudentData1)
    print(StudentID)
    if StudentID:
        return render(request, 'Student_Home_Base.html', {'StudentID': StudentID,'StudentData':StudentData1})
    return render(request,'Student_Home_Base.html',{'StudentData':StudentData1})
    
def Student_Home(request):
    StudentID = request.session.get('StudentID')
    StudentData1 = get_object_or_404(StudentData, StudentID=StudentID)
    if not StudentData1.Profile_Photo:
        StudentData1.Profile_Photo = 'profile_photos/default-profile.png'
    if StudentID:
        return render(request, 'Student_Home.html', {'StudentID': StudentID,'StudentData':StudentData1})
    return render(request,'Login_Base.html',{'StudentData':StudentData1})

def Student_Home_Profile(request):
    StudentID = request.session.get('StudentID')
    student = get_object_or_404(StudentData, StudentID=StudentID)

    profile, created = StudentData.objects.get_or_create(StudentID=StudentID)
    if request.method == 'POST':
        # Check if the request has a file
        if request.FILES.get('Profile_Photo'):
            profile.Profile_Photo = request.FILES['Profile_Photo']
            profile.save()
            return redirect('Student_Home_Profile')
    return render(request,'Student_Home_Profile.html',{'student': student})

def Student_Home_Profile_Update(request):
    print('Meet')
    StudentID = request.session.get('StudentID')
    print('Meet1')
    student = get_object_or_404(StudentData, StudentID=StudentID)
    student = get_object_or_404(StudentData, StudentID=StudentID)
    if request.method == "POST":
        print('Meet2')
        New_Email = request.POST.get('Old_Email')
        New_Mobile = request.POST.get('Old_Mobile')
        print(New_Email)
        print(New_Mobile)
        try:
            #if New_Email 
            student.Email = New_Email
            student.Mobile = New_Mobile
            student.save()
            print('Save')
            return render(request,'Student_Home_Profile.html',{'student': student})
        except:
            print('Meet')
        
    return render(request,'Student_Home_Profile_Update.html',{'student': student})

def Student_Home_Profile_Password_Change(request):
    StudentID = request.session.get('StudentID')
    student = get_object_or_404(StudentData, StudentID=StudentID) 
    PasswordChange = get_object_or_404(StudentData, StudentID=StudentID)
    if request.method == 'POST':
        Old_Password = request.POST.get('Old_Password')
        New_Password = request.POST.get('New_Password')
        print(Old_Password)
        print(New_Password)
        try:
            student = StudentData.objects.get(StudentID=StudentID)
            if student.Password == Old_Password:
                PasswordChange.Password = New_Password
                PasswordChange.save()
                return render(request,'Student_Home_Profile.html',{'student': student})

                  # For production, use hashed passwords
        except:
            print('Meet')

    return render(request,'Student_Home_Profile_Password_Change.html',{'student': student})

def Student_Home_Attendance_Show(request):
    StudentID = request.session.get('StudentID')
    Attendancedata = AttendanceData.objects.filter(StudentID=StudentID)
    if request.method == 'POST':
        Subject_Name = request.POST.get('Subject_Name')
        Subject_Code = request.POST.get('Subject_Code')
        AttendanceDay = request.POST.get('AttendanceDay')
        AttendanceDate = request.POST.get('AttendanceDate')
    
        if Subject_Name:
            Attendancedata = AttendanceData.objects.filter(Subject_Name=Subject_Name,StudentID=StudentID)
        elif Subject_Code:
            Attendancedata = AttendanceData.objects.filter(Subject_Code=Subject_Code,StudentID=StudentID)
        elif AttendanceDay:
            Attendancedata = AttendanceData.objects.filter(AttendanceDay=AttendanceDay,StudentID=StudentID)
        elif AttendanceDate:
            Attendancedata = AttendanceData.objects.filter(AttendanceDate=AttendanceDate,StudentID=StudentID)

    else:
            Attendancedata = AttendanceData.objects.filter(StudentID=StudentID)
    return render(request,'Student_Home_Attendance_Show.html', {'Attendancedata' : Attendancedata})

def Student_Home_Subject_Attendance(request): 
    StudentID = request.session.get('StudentID')
    try:
        student = StudentData.objects.get(StudentID=StudentID)
        #print(student.Semestre)
        #print(student.Department)
        Semestre = student.Semestre
        Department = student.Department
        Subject = SubjectData.objects.filter(Semestre=Semestre,Department=Department)
        if Semestre and Department:
            #StudentData = StudentRegistration.objects.filter(Semestre=Semestre)
            print('Meet2')
            for subject in Subject:
                    Subject = SubjectData.objects.filter(Semestre=Semestre,Department=Department)
                    Meet = subject.Subject_Name
                    TotalAttendance = AttendanceData.objects.filter(StudentID=StudentID,Subject_Name=Meet).count()
                    print(TotalAttendance)
            #return render(request,'Student_Home_Subject_Attendance.html',{'Subject':Subject,'TotalAttendance':TotalAttendance})
        else:
            messages.error(request, "No Data Available")
        #print(Subject)
        #if Semestre and Department and StudentID:
        #    print(StudentID)
        #    print(Semestre)
        #    print(Department)

        #    print(TotalAttendance)
        #TotalAttendance1 = (
        #AttendanceData.objects
        #.values('Subject_Name')
        #.annotate(TotalAttendance=Count(StudentID))
        #.order_by('Subject_Name')
        #)
    except:
        print('Meet1')
    return render(request,'Student_Home_Subject_Attendance.html',{'Subject':Subject,'TotalAttendance':AttendanceData.objects.filter(StudentID=StudentID,Subject_Name=Meet).count() })

def Teacher_Home_Base(request): 
    TeacherID = request.session.get('TeacherID')
    TeacherData1 = get_object_or_404(TeacherData, TeacherID=TeacherID)
    if TeacherID:
        return render(request, 'Teacher_Home_Base.html', {'TeacherID': TeacherID,'TeacherData':TeacherData1})
    return render(request,'Teacher_Home_Base.html')

def Teacher_Home(request):
    TeacherID = request.session.get('TeacherID')
    TeacherData1 = get_object_or_404(TeacherData, TeacherID=TeacherID)
    if TeacherID:
        return render(request, 'Teacher_Home.html', {'TeacherData':TeacherData1})
    return render(request,'Teacher_Home.html')

def Teacher_Home_Student_Data(request):
    StudentData1 = StudentData.objects.all()
    TeacherID = request.session.get('TeacherID')
    TeacherData1 = get_object_or_404(TeacherData, TeacherID=TeacherID)
    if request.method == 'POST':
        Semestre = request.POST.get('Semestre')
        Department = request.POST.get('Department')
        StudentID = request.POST.get('StudentID')
        if Semestre and Department:
            #if Semestre and Department:
            StudentData1 = StudentData.objects.filter(Semestre=Semestre,Department=Department) 
        elif Semestre:
            StudentData1 = StudentData.objects.filter(Semestre=Semestre)
        elif Department:
            StudentData1 = StudentData.objects.filter(Department=Department)
        elif StudentID:
            StudentData1 = StudentData.objects.filter(StudentID=StudentID)
        else:
            StudentData1 = StudentData.objects.all()
    return render(request,'Teacher_Home_Student_Data.html', {'StudentData' : StudentData1,'TeacherData':TeacherData1})

def Teacher_Home_Student_Data_Show(request, StudentID):
    StudentData1 = get_object_or_404(StudentData, StudentID=StudentID)
    return render(request,'Teacher_Home_Student_Data_Show.html', {'StudentData' : StudentData1})

def Teacher_Home_Attendance_Data(request): 
    Attendancedata = AttendanceData.objects.all()
    TeacherID = request.session.get('TeacherID')
    TeacherData1 = get_object_or_404(TeacherData, TeacherID=TeacherID)
    if request.method == 'POST':
        StudentID = request.POST.get('StudentID')
        Subject_Name = request.POST.get('Subject_Name')
        Subject_Code = request.POST.get('Subject_Code')
        AttendanceDay = request.POST.get('AttendanceDay')
        AttendanceDate = request.POST.get('AttendanceDate')
        if StudentID and Subject_Name and Subject_Code and AttendanceDay and AttendanceDate:
            Attendancedata = AttendanceData.objects.filter(StudentID=StudentID, Subject_Name=Subject_Name, Subject_Code=Subject_Code, AttendanceDay=AttendanceDay, AttendanceDate=AttendanceDate)

        elif StudentID and Subject_Name and Subject_Code and AttendanceDay:
            Attendancedata = AttendanceData.objects.filter(StudentID=StudentID, Subject_Name=Subject_Name, Subject_Code=Subject_Code, AttendanceDay=AttendanceDay)
        elif StudentID and Subject_Name and Subject_Code and  AttendanceDate:
            Attendancedata = AttendanceData.objects.filter(StudentID=StudentID, Subject_Name=Subject_Name, Subject_Code=Subject_Code, AttendanceDate=AttendanceDate)
        elif StudentID and Subject_Name and AttendanceDay and AttendanceDate:
            Attendancedata = AttendanceData.objects.filter(StudentID=StudentID, Subject_Name=Subject_Name, AttendanceDay=AttendanceDay, AttendanceDate=AttendanceDate)
        elif StudentID and Subject_Code and AttendanceDay and AttendanceDate:
            Attendancedata = AttendanceData.objects.filter(StudentID=StudentID, Subject_Code=Subject_Code, AttendanceDay=AttendanceDay, AttendanceDate=AttendanceDate)

        elif Subject_Name and Subject_Code and AttendanceDay and AttendanceDate:
            Attendancedata = AttendanceData.objects.filter(Subject_Name=Subject_Name, Subject_Code=Subject_Code, AttendanceDay=AttendanceDay, AttendanceDate=AttendanceDate)

        elif StudentID and Subject_Name and Subject_Code:
            Attendancedata = AttendanceData.objects.filter(StudentID=StudentID, Subject_Name=Subject_Name, Subject_Code=Subject_Code)
        elif StudentID and Subject_Name and AttendanceDay:
            Attendancedata = AttendanceData.objects.filter(StudentID=StudentID, Subject_Name=Subject_Name, AttendanceDay=AttendanceDay)
        elif StudentID and Subject_Name and AttendanceDate:
            Attendancedata = AttendanceData.objects.filter(StudentID=StudentID, Subject_Name=Subject_Name, AttendanceDate=AttendanceDate)

        elif StudentID and Subject_Code and AttendanceDay:
            Attendancedata = AttendanceData.objects.filter(StudentID=StudentID, Subject_Code=Subject_Code, AttendanceDate=AttendanceDate)
        elif StudentID and Subject_Code and AttendanceDate:
            Attendancedata = AttendanceData.objects.filter(StudentID=StudentID, Subject_Code=Subject_Code, AttendanceDate=AttendanceDate)

        elif Subject_Name and Subject_Code and AttendanceDay:
            Attendancedata = AttendanceData.objects.filter(Subject_Name=Subject_Name, AttendanceDay=AttendanceDay)
        elif Subject_Name and Subject_Code and AttendanceDate:
            Attendancedata = AttendanceData.objects.filter(Subject_Name=Subject_Name, AttendanceDate=AttendanceDate)

        elif StudentID and AttendanceDay and AttendanceDate:
            Attendancedata = AttendanceData.objects.filter(StudentID=StudentID, AttendanceDay=AttendanceDay, AttendanceDate=AttendanceDate)

        elif StudentID and Subject_Name:
            Attendancedata = AttendanceData.objects.filter(StudentID=StudentID,Subject_Name=Subject_Name)
        elif StudentID and Subject_Code:
            Attendancedata = AttendanceData.objects.filter(StudentID=StudentID,Subject_Code=Subject_Code)
        elif StudentID and AttendanceDay:
            Attendancedata = AttendanceData.objects.filter(StudentID=StudentID,AttendanceDay=AttendanceDay)
        elif StudentID and AttendanceDate:
            Attendancedata = AttendanceData.objects.filter(StudentID=StudentID,AttendanceDate=AttendanceDate)

        elif Subject_Name and Subject_Code:
            Attendancedata = AttendanceData.objects.filter(StudentID=StudentID,Subject_Code=Subject_Code)
        elif Subject_Name and AttendanceDay:
            Attendancedata = AttendanceData.objects.filter(StudentID=StudentID,AttendanceDay=AttendanceDay)
        elif Subject_Name and AttendanceDate:
            Attendancedata = AttendanceData.objects.filter(StudentID=StudentID,AttendanceDate=AttendanceDate)

        elif Subject_Code and AttendanceDay:
            Attendancedata = AttendanceData.objects.filter(Subject_Code=Subject_Code,AttendanceDay=AttendanceDay)
        elif Subject_Code and AttendanceDate:
            Attendancedata = AttendanceData.objects.filter(Subject_Code=Subject_Code,AttendanceDate=AttendanceDate)

        elif AttendanceDay and AttendanceDate:
            Attendancedata = AttendanceData.objects.filter(Subject_Code=Subject_Code,AttendanceDay=AttendanceDay)

        elif StudentID:
            Attendancedata = AttendanceData.objects.filter(StudentID=StudentID)
        elif Subject_Name:
            Attendancedata = AttendanceData.objects.filter(Subject_Name=Subject_Name)
        elif Subject_Code:
            Attendancedata = AttendanceData.objects.filter(Subject_Code=Subject_Code)
        elif AttendanceDay:
            Attendancedata = AttendanceData.objects.filter(AttendanceDay=AttendanceDay)
        elif AttendanceDate:
            Attendancedata = AttendanceData.objects.filter(AttendanceDate=AttendanceDate)

        else:
            Attendancedata = AttendanceData.objects.all()

    return render(request,'Teacher_Home_Attendance_Data.html',{'Attendancedata':Attendancedata,'TeacherData':TeacherData1})

def Teacher_Home_New_Attendance_Select(request):
    DepartmentandSemestre1 = DepartmentandSemestre.objects.values_list('Department_Name', flat=True).distinct()
    TeacherID = request.session.get('TeacherID')
    TeacherData1 = get_object_or_404(TeacherData, TeacherID=TeacherID)
    if request.method == 'POST':
        TeacherID = TeacherData1.TeacherID
        Teacher_Name = TeacherData1.Teacher_Name
        Department = request.POST.get('Department')
        Semestre = request.POST.get('Semestre') 
        SubjectName = request.POST.get('SubjectName') 
        SubjectCode = request.POST.get('SubjectCode')
        LectureStartingTime = request.POST.get('LectureStartingTime')
        LectureEndingTime = request.POST.get('LectureEndingTime')
        current_datetime = datetime.now()
        formatted_date = current_datetime.strftime('%Y-%m-%d')
        day_of_week = current_datetime.strftime('%A')
        formatted_time = current_datetime.strftime('%H:%M:%S')
        if Department and Semestre and SubjectName and SubjectCode:
            request.session['Department'] = Department  # Store in session
            request.session['Semestre'] = Semestre  # Store in session
            request.session['SubjectName'] = SubjectName  # Store in session
            request.session['SubjectCode'] = SubjectCode  # Store in session
            TeacherLectureData.objects.create(TeacherID=TeacherID, Teacher_Name=Teacher_Name, Department=Department, Semestre=Semestre, Subject_Name=SubjectName, Subject_Code=SubjectCode, LectureDate=formatted_date, LectureDay=day_of_week, LectureTime=formatted_time, LectureStartingTime=LectureStartingTime, LectureEndingTime=LectureEndingTime)
            #return redirect('Teacher_Home_New_Attendance')
            return render(request,'Teacher_Home_New_Attendance.html')
        if DepartmentandSemestre1 and TeacherData1:
            return render(request,'Teacher_Home_New_Attendance_Select.html',{'DepartmentandSemestre':DepartmentandSemestre1,'TeacherData':TeacherData1})
        return render(request,'Teacher_Home_New_Attendance_Select.html',{'DepartmentandSemestre':DepartmentandSemestre1,'TeacherData':TeacherData1})
    return render(request,'Teacher_Home_New_Attendance_Select.html',{'DepartmentandSemestre':DepartmentandSemestre1,'TeacherData':TeacherData1})

def Teacher_Home_New_Attendance(request):
    return render(request,'Teacher_Home_New_Attendance.html')

def load_known_faces():
    known_faces = []
    known_names = []
    
    users = StudentData.objects.all()
    for user in users:
        if user.Profile_Photo:
            # Load the user's profile image
            image = face_recognition.load_image_file(user.Profile_Photo.path)
            encoding = face_recognition.face_encodings(image)
            if encoding: 
                known_faces.append(encoding[0])  # Take the first face encoding
                known_names.append(user.StudentID)  # Use the user's name as the label
    
    return known_faces, known_names

known_faces, known_names = load_known_faces()

video_feed_active = True

#def gen_frames(Department,Semestre,SubjectName,SubjectCode):
#    video_capture = cv2.VideoCapture(0, cv2.CAP_ANY)  # 0 is the default camera
#    #video_capture.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
#    #video_capture.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)
#    video_capture.set(cv2.CAP_PROP_FPS, 15)  # Set the frame rate to 15 fps
#    frame_skip = 2  # Skip every other frame to optimize performance
#    frame_count = 0
#    while video_feed_active:
#        # Read a frame from the camera
#        ret, frame = video_capture.read()
#        if not ret:
#            break


#        ##  Convert the frame to grayscale (required for face detection)
#        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

#        # Find all faces in the current frame
#        face_locations = face_recognition.face_locations(rgb_frame)
#        face_encodings = face_recognition.face_encodings(rgb_frame, face_locations)

#        # Check for each face if it matches any of the known faces
#        for (top, right, bottom, left), face_encoding in zip(face_locations, face_encodings):
#            matches = face_recognition.compare_faces(known_faces, face_encoding)
#            current_datetime = datetime.now()
#            name = "Unknown" 
#            current_datetime = datetime.now()
#            formatted_date = current_datetime.strftime('%Y-%m-%d')
#            day_of_week = current_datetime.strftime('%A')
#            formatted_time = current_datetime.strftime('%H:%M:%S')
#            if True in matches:
#                first_match_index = matches.index(True)
#                name = known_names[first_match_index]

#                # Check if attendance already exists for the same student, subject, and time
#                existing_entry = AttendanceData.objects.filter(
#                    StudentID=name,
#                    Subject_Name=SubjectName,
#                    AttendanceDate=formatted_date,
#                    AttendanceTime=formatted_time
#                ).exists()
#                if not existing_entry:
#                    AttendanceData.objects.create(
#                        StudentID=name,
#                        Subject_Name=SubjectName,
#                        Subject_Code=SubjectCode,
#                        AttendanceTime=formatted_time,
#                        AttendanceDay=day_of_week,
#                        AttendanceDate=formatted_date
#                    )

#            # Draw a rectangle around the face
#            cv2.rectangle(frame, (left, top), (right, bottom), (0, 255, 0), 2)

#            # Display the name under the face
#            font = cv2.FONT_HERSHEY_DUPLEX
#            cv2.putText(frame, name, (left + 6, bottom - 6), font, 0.5, (255, 255, 255), 1)

#    # Skip frames for performance optimization
#        #if frame_count % frame_skip == 0:
#        #    # Resize frame to reduce processing load
#        #    frame = cv2.resize(frame, (640, 480))

#        #    # Add processing (e.g., face detection)
#        #    # Convert the frame to RGB (OpenCV uses BGR by default)
#        #    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

#        #    # Further processing or face detection could happen here

#        #    # Encode the frame in JPEG format
#        #    encode_param = [int(cv2.IMWRITE_JPEG_QUALITY), 80]  # Set compression quality to 80
#        #    # Convert frame to JPEG format
#        #    _, buffer = cv2.imencode('.jpg', frame, encode_param)
#        #    frame = buffer.tobytes()
#        _, buffer = cv2.imencode('.jpg', frame)
#        frame = buffer.tobytes()

#            # Yield the frame as a JPEG image
#        yield (b'--frame\r\n'
#                    b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n')

#        #frame_count += 1
#    # Release the camera when done
#    video_capture.release()

def gen_frames(Department, Semestre, SubjectName, SubjectCode):
    video_capture = cv2.VideoCapture(0, cv2.CAP_ANY)  # 0 is the default camera
    video_capture.set(cv2.CAP_PROP_FPS, 15)  # Set the frame rate to 15 fps
    frame_skip = 2  # Skip every other frame to optimize performance
    frame_count = 0

    while video_feed_active:
        # Read a frame from the camera
        ret, frame = video_capture.read()
        if not ret:
            break

        # Convert the frame to RGB (required for face detection)
        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

        # Find all faces in the current frame
        face_locations = face_recognition.face_locations(rgb_frame)
        face_encodings = face_recognition.face_encodings(rgb_frame, face_locations)

        # Check for each face if it matches any of the known faces
        for (top, right, bottom, left), face_encoding in zip(face_locations, face_encodings):
            matches = face_recognition.compare_faces(known_faces, face_encoding)
            name = "Unknown"
            current_datetime = datetime.now()
            formatted_date = current_datetime.strftime('%Y-%m-%d')
            day_of_week = current_datetime.strftime('%A')
            formatted_time = current_datetime.strftime('%H:%M:%S')

            if True in matches:
                first_match_index = matches.index(True)
                name = known_names[first_match_index]

                # Check if attendance already exists for the same student, subject, date, and time
                existing_entry = AttendanceData.objects.filter(
                    StudentID=name,
                    Subject_Name=SubjectName,
                    AttendanceDate=formatted_date,
                    AttendanceTime=formatted_time
                ).exists()

                if not existing_entry:
                    print('Meet1')
                    # Create a new attendance record if one doesn't exist
                    AttendanceData.objects.create(
                        StudentID=name,
                        Subject_Name=SubjectName,
                        Subject_Code=SubjectCode,
                        AttendanceTime=formatted_time,
                        AttendanceDay=day_of_week,
                        AttendanceDate=formatted_date
                    )

            # Draw a rectangle around the face and display the name
            cv2.rectangle(frame, (left, top), (right, bottom), (0, 255, 0), 2)
            font = cv2.FONT_HERSHEY_DUPLEX
            cv2.putText(frame, name, (left + 6, bottom - 6), font, 0.5, (255, 255, 255), 1)

        # Convert the frame to JPEG and yield it
        _, buffer = cv2.imencode('.jpg', frame)
        frame = buffer.tobytes()
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n')

    # Release the camera when done
    video_capture.release()


def video_feed(request): 
    Department = request.session.get('Department','Unknown Department')
    Semestre = request.session.get('Semestre','Unknown Semestre')
    SubjectName = request.session.get('SubjectName','Unknown SubjectName')
    SubjectCode = request.session.get('SubjectCode','Unknown SubjectCode')
    return StreamingHttpResponse(gen_frames(Department,Semestre,SubjectName,SubjectCode), content_type='multipart/x-mixed-replace; boundary=frame')


def stop_feed(request):
    global video_feed_active
    if request.method == "POST":
        video_feed_active = False
        return JsonResponse({"message": "Video feed stopped successfully!"})
    return JsonResponse({"error": "Invalid request method."}, status=400)


def Teacher_Home_LectureData(request): 
    TeacherID = request.session.get('TeacherID')
    TeacherData1 = get_object_or_404(TeacherData, TeacherID=TeacherID)
    TeacherID = request.session.get('TeacherID')
    LectureData = TeacherLectureData.objects.filter(TeacherID=TeacherID)
    return render(request,'Teacher_Home_LectureData.html',{'LectureData':LectureData,'TeacherData':TeacherData1})

#def Student_Password_Forget(request): 

#    return render(request,'Student_Password_Forget.html')



def DatabaseAdministrator_Base(request):
    return render(request,'DatabaseAdministrator_Base.html')


def DatabaseAdministrator_Login(request):
    if request.method == "POST":
        DatabaseAdministratorID = request.POST.get('DatabaseAdministratorID')
        DatabaseAdministrator_CollageCode = request.POST.get('DatabaseAdministrator_CollageCode')
        Password = request.POST.get('Password')
        try:
            DatabaseAdministrator = DatabaseAdministratorList.objects.get(DatabaseAdministratorID=DatabaseAdministratorID)
            if DatabaseAdministrator.DatabaseAdministrator_CollageCode == DatabaseAdministrator_CollageCode and DatabaseAdministrator.Password == Password:  # For production, use hashed passwords
                request.session['DatabaseAdministratorID'] = DatabaseAdministratorID  # Store user ID in session
                user = authenticate(request, DatabaseAdministratorID=DatabaseAdministratorID,DatabaseAdministrator_CollageCode=DatabaseAdministrator_CollageCode, Password=Password)
                if user is not None:
                    login(request, user)
                    request.session['DatabaseAdministratorID'] = user.DatabaseAdministratorID  # Store StudentID in session
                    return redirect('DatabaseAdministrator_Home')  # Redirect to home page
                #DatabaseAdministratorStatus = DatabaseAdministratorList.objects.get(DatabaseAdministratorID=DatabaseAdministratorID)
                DatabaseAdministrator.LoginStatus = True
                DatabaseAdministrator.save()
                    #messages.success(request, "Login successful!")
                return redirect('DatabaseAdministrator_Home')  # Redirect to a success page
            else:
                messages.error(request, "Invalid ID or Password.")
        except StudentData.DoesNotExist:
            messages.error(request, "Invalid ID or Password.") 
    return render(request,'DatabaseAdministrator_Login.html')


def DatabaseAdministrator_Home(request):
    DatabaseAdministratorID = request.session.get('DatabaseAdministratorID')
    if request.method == 'POST':
        Student_Response = request.POST.get('Student_Response')  # Retrieve the value from the form
        print(Student_Response)
        if Student_Response == 'Yes':
            DatabaseAdministratorStatus = DatabaseAdministratorList.objects.get(DatabaseAdministratorID=DatabaseAdministratorID)
            DatabaseAdministratorStatus.LoginStatus = False
            DatabaseAdministratorStatus.save()
            return render(request,'Login_Base.html')
    DatabaseAdministrator = get_object_or_404(DatabaseAdministratorList, DatabaseAdministratorID=DatabaseAdministratorID)
    if DatabaseAdministratorID:
        return render(request, 'DatabaseAdministrator_Home.html', {'DatabaseAdministrator': DatabaseAdministrator})
    return render(request,'DatabaseAdministrator_Home.html')

def DatabaseAdministrator_DepartmentSemester(request): 
    DepartmentandSemestre1 = DepartmentandSemestre.objects.all()
    return render(request,'DatabaseAdministrator_DepartmentSemester.html',{'DepartmentandSemestre':DepartmentandSemestre1})

def DepartmentandSemestre_AddNew(request):
    if request.method == 'POST':
        Department_Code = request.POST.get('Department_Code')
        Department_Name = request.POST.get('Department_Name')
        Semestre = request.POST.get('Semestre')

        # Save data to the database
        DepartmentandSemestre.objects.create(Department_Code=Department_Code, Department_Name=Department_Name, Semestre=Semestre)

        return redirect('DatabaseAdministrator_DepartmentSemester')  # Redirect to a success page or another page
    return render(request, 'DatabaseAdministrator_DepartmentSemester.html')  # Render a page if needed

def DepartmentandSemestre_Updatedata(request):
    if request.method == 'POST':
        DepartmentandSemestreID = request.POST.get('DepartmentandSemestreID')
        Department_Code = request.POST.get('Department_Code')
        Department_Name = request.POST.get('Department_Name')
        Semestre = request.POST.get('Semestre')
        print(DepartmentandSemestreID)
        print(Department_Code)

        UpdateData = get_object_or_404(DepartmentandSemestre, DepartmentandSemestreID=DepartmentandSemestreID)

        try:
            if DepartmentandSemestreID is not None:
                if Department_Code is not None:
                   if Department_Name is not None:
                        print(Department_Name)
                        if Semestre is not None:
                            print(Semestre)
 
                            UpdateData.Department_Code = Department_Code
                            UpdateData.Department_Name = Department_Name
                            UpdateData.Semestre = Semestre
                            UpdateData.save()
                            return redirect('DatabaseAdministrator_DepartmentSemester')
        except:
            return redirect('DatabaseAdministrator_DepartmentSemester')


# View for deleting a record
def DepartmentandSemestre_Deletedata(request, id):
    record = get_object_or_404(DepartmentandSemestre, pk=id)
    record.delete()
    return JsonResponse({'message': 'Record deleted successfully!'})
#   return render(request, 'DatabaseAdministrator_DepartmentSemester.html')  # Render a page if needed


def DatabaseAdministrator_TeacherData(request):
    TeacherData1 = TeacherData.objects.all()
    DepartmentandSemestre1 = DepartmentandSemestre.objects.values_list('Department_Name', flat=True).distinct()
    DatabaseAdministratorID = request.session.get('DatabaseAdministratorID')
    DatabaseAdministrator = get_object_or_404(DatabaseAdministratorList, DatabaseAdministratorID=DatabaseAdministratorID)
    if DatabaseAdministratorID:
        return render(request,'DatabaseAdministrator_TeacherData.html',{'TeacherData1':TeacherData1,'DatabaseAdministrator': DatabaseAdministrator,'DepartmentandSemestre':DepartmentandSemestre1})
    return render(request,'DatabaseAdministrator_TeacherData.html',{'TeacherData1':TeacherData1,'DatabaseAdministrator': DatabaseAdministrator,'DepartmentandSemestre':DepartmentandSemestre1})

def TeacherData_AddNew(request):
    if request.method == 'POST':
        TeacherID = request.POST.get('TeacherID')
        Teacher_Name = request.POST.get('Teacher_Name')
        CollageCode = request.POST.get('CollageCode')
        Department = request.POST.get('Department')
        Email = request.POST.get('Email')
        Mobile = request.POST.get('Mobile')
        Password = request.POST.get('Password')

        # Save data to the database
        TeacherData.objects.create(TeacherID=TeacherID, Teacher_Name=Teacher_Name, Department=Department,CollageCode=CollageCode, Email=Email, Mobile=Mobile, Password=Password)

        return redirect('DatabaseAdministrator_TeacherData')  # Redirect to a success page or another page
    return render(request, 'DatabaseAdministrator_TeacherData.html')  # Render a page if needed

def TeacherData_Updatedata(request):
    if request.method == 'POST':
        TeacherID = request.POST.get('TeacherID')
        Teacher_Name = request.POST.get('Teacher_Name')
        Department = request.POST.get('Department')
        Email = request.POST.get('Email')
        Mobile = request.POST.get('Mobile')

        UpdateData = get_object_or_404(TeacherData, TeacherID=TeacherID)

        try:
            if TeacherID is not None:
                if Teacher_Name is not None:
                   if Department is not None:
                        if Email is not None:
                            if Mobile is not None:
 
                                UpdateData.Teacher_Name = Teacher_Name
                                UpdateData.Department = Department
                                UpdateData.Email = Email
                                UpdateData.Mobile = Mobile
                                UpdateData.save()
                                return redirect('DatabaseAdministrator_TeacherData')
        except:
            return redirect('DatabaseAdministrator_TeacherData')


# View for deleting a record
def TeacherData_Deletedata(request, id):
    record = get_object_or_404(TeacherData, pk=id)
    record.delete()
    return JsonResponse({'message': 'Record deleted successfully!'})
    #return render(request, 'DatabaseAdministrator_TeacherData.html')  # Render a page if needed


def DatabaseAdministrator_StudentData(request): 
    StudentData1 = StudentData.objects.all()
    StudentRegistration1 = StudentData.objects.all()
    DepartmentandSemestre1 = DepartmentandSemestre.objects.values_list('Department_Name', flat=True).distinct()
    DatabaseAdministratorID = request.session.get('DatabaseAdministratorID')
    DatabaseAdministrator = get_object_or_404(DatabaseAdministratorList, DatabaseAdministratorID=DatabaseAdministratorID)
    if DatabaseAdministratorID:
        return render(request,'DatabaseAdministrator_StudentData.html',{'StudentData':StudentData1,'DepartmentandSemestre':DepartmentandSemestre1,'StudentRegistration':StudentRegistration1,'DatabaseAdministrator': DatabaseAdministrator})
    return render(request,'DatabaseAdministrator_StudentData.html',{'StudentData':StudentData1,'DepartmentandSemestre':DepartmentandSemestre1,'StudentRegistration':StudentRegistration1})

#def StudentData_Updatedata(request):
#    if request.method == 'POST':
#        StudentID = request.POST.get('StudentID')
#        Student_Name = request.POST.get('Student_Name')
#        Semestre = request.POST.get('Semestre')
#        Department = request.POST.get('Department')
#        Email = request.POST.get('Email')
#        Mobile = request.POST.get('Mobile')

#        UpdateData = get_object_or_404(StudentData, StudentID=StudentID)
#        if request.method == 'POST':
#            if request.FILES.get('Profile_Photo'):
#                UpdateData.Profile_Photo = request.FILES['Profile_Photo']
#                UpdateData.save()
#                return redirect('DatabaseAdministrator_StudentData')
#        try:
#            if StudentID is not None:
#                if Student_Name is not None:
#                   if Semestre is not None:
#                     if Department is not None:
#                        if Email is not None:
#                            if Mobile is not None:
 
#                                UpdateData.Student_Name = Student_Name
#                                UpdateData.Semestre = Semestre
#                                UpdateData.Department = Department
#                                UpdateData.Email = Email
#                                UpdateData.Mobile = Mobile
#                                UpdateData.save()
#                                return redirect('DatabaseAdministrator_StudentData')
#        except:
#            return redirect('DatabaseAdministrator_StudentData')

def StudentData_Updatedata(request):
    if request.method == 'POST':
        StudentID = request.POST.get('StudentID')
        Student_Name = request.POST.get('Student_Name')
        Semestre = request.POST.get('Semestre')
        Department = request.POST.get('Department')
        Email = request.POST.get('Email')
        Mobile = request.POST.get('Mobile')

        UpdateData = get_object_or_404(StudentData, StudentID=StudentID)

        if request.FILES.get('Profile_Photo'):
            UpdateData.Profile_Photo = request.FILES['Profile_Photo']

        UpdateData.Student_Name = Student_Name
        UpdateData.Semestre = Semestre
        UpdateData.Department = Department
        UpdateData.Email = Email
        UpdateData.Mobile = Mobile
        UpdateData.save()

        return redirect('DatabaseAdministrator_StudentData')

    return redirect('DatabaseAdministrator_StudentData')

def DatabaseAdministrator_StudentRegistration(request):
    Student_Data = StudentData.objects.values_list('StudentID', flat=True)
    Student_Registration = StudentRegistration.objects.all()
    annotated_students = [
        {
            'StudentID': registration.StudentID,
            'Student_Name': registration.Student_Name,
            'DateOfBirth': registration.DateOfBirth,
            'RegistrationDate': registration.RegistrationDate,
            'Email': registration.Email,
            'Mobile': registration.Mobile,
            'Department': registration.Department,
            #'Status': 'Yes' if registration.StudentID in Student_Data else 'No'
            'ExistsInStudentData': {
            'Status': 'Yes' if registration.StudentID in Student_Data else 'No',
            'color': 'green' if registration.StudentID in Student_Data else 'red'
        }
        }
        for registration in Student_Registration
    ]
    StudentData1 = StudentRegistration.objects.all()
    #StudentRegistration1 = StudentRegistration.objects.all()
    DepartmentandSemestre1 = DepartmentandSemestre.objects.values_list('Department_Name', flat=True).distinct()
    DatabaseAdministratorID = request.session.get('DatabaseAdministratorID')
    DatabaseAdministrator = get_object_or_404(DatabaseAdministratorList, DatabaseAdministratorID=DatabaseAdministratorID)
    if DatabaseAdministratorID:
        return render(request,'DatabaseAdministrator_StudentRegistration.html',{'StudentData':StudentData1,'DepartmentandSemestre':DepartmentandSemestre1,'DatabaseAdministrator': DatabaseAdministrator,'StudentDatas': annotated_students})
    return render(request,'DatabaseAdministrator_StudentRegistration.html',{'StudentData':StudentData1,'DepartmentandSemestre':DepartmentandSemestre1,'StudentDatas': annotated_students})
    #    return render(request,'DatabaseAdministrator_StudentRegistration.html',{'StudentData': annotated_students})
    #return render(request,'DatabaseAdministrator_StudentRegistration.html',{'StudentDatas': annotated_students})

def StudentData_Deletedata(request, id):
    record = get_object_or_404(StudentData, pk=id)
    record.delete()
    return JsonResponse({'message': 'Record deleted successfully!'})
    #return render(request, 'DatabaseAdministrator_StudentData.html')  # Render a page if needed

def StudentRegistration_AddNew(request):
    if request.method == 'POST':
        StudentID = request.POST.get('StudentID')
        Student_Name = request.POST.get('Student_Name')
        CollageCode = request.POST.get('CollageCode')
        DateOfBirth = request.POST.get('DateOfBirth')
        Department = request.POST.get('Department')
        Email = request.POST.get('Email')
        Mobile = request.POST.get('Mobile')

        current_datetime = datetime.now()
        RegistrationDate = current_datetime.strftime('%Y-%m-%d')

        # Save data to the database
        StudentRegistration.objects.create(StudentID=StudentID, Student_Name=Student_Name, DateOfBirth=DateOfBirth, CollageCode=CollageCode, Department=Department, Email=Email, Mobile=Mobile ,RegistrationDate=RegistrationDate)

        return redirect('DatabaseAdministrator_StudentRegistration')  # Redirect to a success page or another page
    return render(request, 'DatabaseAdministrator_StudentRegistration.html')  # Render a page if needed

def StudentRegistration_Updatedata(request):
    if request.method == 'POST':
        StudentID = request.POST.get('StudentID')
        Student_Name = request.POST.get('Student_Name')
        Department = request.POST.get('Department')

        UpdateData = get_object_or_404(StudentRegistration, StudentID=StudentID)
        UpdateStudentData = get_object_or_404(StudentData, StudentID=StudentID)
        try:
            if StudentID is not None:
                if Student_Name is not None:
                   if Department is not None:
                        UpdateData.Student_Name = Student_Name
                        UpdateData.Department = Department
                        UpdateStudentData.Department = Department
                        UpdateStudentData.save()
                        UpdateData.save()
                        return redirect('DatabaseAdministrator_StudentRegistration')
        except:
            return redirect('DatabaseAdministrator_StudentRegistration')  
        
def StudentRegistration_Deletedata(request, id):
    record = get_object_or_404(StudentRegistration, pk=id)
    record.delete()
    return JsonResponse({'message': 'Record deleted successfully!'})
    #return render(request, 'DatabaseAdministrator_StudentRegistration.html')  # Render a page if needed
    

def DatabaseAdministrator_SubjectData(request): 
    SubjectData1 = SubjectData.objects.all()
    DepartmentandSemestre1 = DepartmentandSemestre.objects.values_list('Department_Name', flat=True).distinct()
    return render(request,'DatabaseAdministrator_SubjectData.html',{'SubjectData':SubjectData1,'DepartmentandSemestre':DepartmentandSemestre1})

def SubjectData_AddNew(request):
    if request.method == 'POST':
        Subject_Name = request.POST.get('Subject_Name')
        Subject_Code = request.POST.get('Subject_Code')
        Department = request.POST.get('Department')
        Semestre = request.POST.get('Semestre')

        # Save data to the database
        SubjectData.objects.create(Subject_Name=Subject_Name, Subject_Code=Subject_Code, Department=Department, Semestre=Semestre)

        return redirect('DatabaseAdministrator_SubjectData')  # Redirect to a success page or another page
    return render(request, 'DatabaseAdministrator_SubjectData.html')  # Render a page if needed

def SubjectData_Updatedata(request):
    if request.method == 'POST':
        SubjectDataID = request.POST.get('SubjectDataID')
        Subject_Name = request.POST.get('Subject_Name')
        Subject_Code = request.POST.get('Subject_Code')
        Semestre = request.POST.get('Semestre')
        Department = request.POST.get('Department')

        UpdateData = get_object_or_404(SubjectData, SubjectDataID=SubjectDataID)
        try:
            if SubjectDataID is not None:
                if Subject_Name is not None:
                    if Department is not None:
                        if Semestre is not None:
                            UpdateData.Subject_Name = Subject_Name
                            UpdateData.Subject_Code = Subject_Code
                            UpdateData.Department = Department
                            UpdateData.Semestre = Semestre
                            UpdateData.save()
                            return redirect('DatabaseAdministrator_SubjectData')
        except:
            return redirect('DatabaseAdministrator_SubjectData') 

def SubjectData_Deletedata(request, id):
    record = get_object_or_404(SubjectData, pk=id)
    record.delete()
    return JsonResponse({'message': 'Record deleted successfully!'})
    #return render(request, 'DatabaseAdministrator_StudentData.html')  # Render a page if needed

def DatabaseAdministrator_TeacherLectureData(request):
    TeacherLectureDataList = TeacherLectureData.objects.all()
    return render(request,'DatabaseAdministrator_TeacherLectureData.html',{'TeacherLectureDataList': TeacherLectureDataList})

def DatabaseAdministrator_List(request):
    DatabaseAdministratorList1 = DatabaseAdministratorList.objects.all()
    DatabaseAdministratorID = request.session.get('DatabaseAdministratorID')
    DatabaseAdministrator = get_object_or_404(DatabaseAdministratorList, DatabaseAdministratorID=DatabaseAdministratorID)
    if DatabaseAdministratorID:
        return render(request, 'DatabaseAdministrator_List.html', {'DatabaseAdministratorList':DatabaseAdministratorList1,'DatabaseAdministrator': DatabaseAdministrator})
    return render(request,'DatabaseAdministrator_List.html',{'DatabaseAdministratorList':DatabaseAdministratorList1})

def DatabaseAdministrator_AddNew(request):
    #DatabaseAdministratorID = request.session.get('DatabaseAdministratorID')
    #DatabaseAdministrator = get_object_or_404(DatabaseAdministratorList, DatabaseAdministratorID=DatabaseAdministratorID)
    #if DatabaseAdministratorID:
    #    return render(request, 'DatabaseAdministrator_Home.html', {'DatabaseAdministrator': DatabaseAdministrator})
    if request.method == 'POST':
        DatabaseAdministratorID = request.POST.get('DatabaseAdministratorID')
        DatabaseAdministrator_Name = request.POST.get('DatabaseAdministrator_Name')
        DatabaseAdministrator_Code = request.POST.get('DatabaseAdministrator_Code')
        DatabaseAdministrator_CollageCode = request.POST.get('DatabaseAdministrator_CollageCode')
        DatabaseAdministrator_Email = request.POST.get('DatabaseAdministrator_Email')
        DatabaseAdministrator_Mobile = request.POST.get('DatabaseAdministrator_Mobile')
        Password = request.POST.get('Password')
        print(DatabaseAdministrator_CollageCode)

        # Save data to the database
        DatabaseAdministratorList.objects.create(DatabaseAdministratorID=DatabaseAdministratorID, DatabaseAdministrator_Name=DatabaseAdministrator_Name, DatabaseAdministrator_Code=DatabaseAdministrator_Code,DatabaseAdministrator_CollageCode=DatabaseAdministrator_CollageCode, DatabaseAdministrator_Email=DatabaseAdministrator_Email, DatabaseAdministrator_Mobile=DatabaseAdministrator_Mobile, Password=Password)

        return redirect('DatabaseAdministrator_List')  # Redirect to a success page or another page
    return render(request, 'DatabaseAdministrator_List.html')  # Render a page if needed

def DatabaseAdministrator_Updatedata(request):
    if request.method == 'POST':
        DatabaseAdministratorID = request.POST.get('DatabaseAdministratorID')
        DatabaseAdministrator_Name = request.POST.get('DatabaseAdministrator_Name')
        DatabaseAdministrator_Code = request.POST.get('DatabaseAdministrator_Code')
        DatabaseAdministrator_Email = request.POST.get('DatabaseAdministrator_Email')
        DatabaseAdministrator_Mobile = request.POST.get('DatabaseAdministrator_Mobile')
        #Mobile = request.POST.get('Mobile')

        UpdateData = get_object_or_404(DatabaseAdministratorList, DatabaseAdministratorID=DatabaseAdministratorID)

        try:
            if DatabaseAdministratorID is not None:
                if DatabaseAdministrator_Name is not None:
                    if DatabaseAdministrator_Code is not None:
                        if DatabaseAdministrator_Email is not None:
                            if DatabaseAdministrator_Mobile is not None:
 
                                UpdateData.DatabaseAdministrator_Name = DatabaseAdministrator_Name
                                UpdateData.DatabaseAdministrator_Code = DatabaseAdministrator_Code
                                UpdateData.DatabaseAdministrator_Email = DatabaseAdministrator_Email
                                UpdateData.DatabaseAdministrator_Mobile = DatabaseAdministrator_Mobile
                                UpdateData.save()
                                return redirect('DatabaseAdministrator_List')
        except:
            return redirect('DatabaseAdministrator_List')

def DatabaseAdministrator_Deletedata(request, id):
    record = get_object_or_404(DatabaseAdministratorList, pk=id)
    record.delete()
    return JsonResponse({'message': 'Record deleted successfully!'})