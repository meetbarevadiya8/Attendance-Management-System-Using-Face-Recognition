from django.contrib import admin
from django.conf import settings
from django.urls import path,include
from faceattendancesystem import views
from django.conf.urls.static import static
from django.contrib.auth.views import LogoutView


urlpatterns = [
    path("",views.Login_Base,name="Login_Base"),
    path("Student_Login",views.Student_Login,name="Student_Login"),
    path("Teacher_Login",views.Teacher_Login,name="Teacher_Login"),
    path("Student_Registration",views.Student_Registration,name="Student_Registration"),
    path("Student_Password_Forget",views.Student_Password_Forget1,name="Student_Password_Forget"),
    path("Student_Password_Forget_New",views.Student_Password_Forget_New,name="Student_Password_Forget_New"),
    path("Student_Home_Base",views.Student_Home_Base,name="Student_Home_Base"),
    path("Student_Home",views.Student_Home,name="Student_Home"),
    path("Student_Home_Profile",views.Student_Home_Profile,name="Student_Home_Profile"),
    path("Student_Home_Profile_Update",views.Student_Home_Profile_Update,name="Student_Home_Profile_Update"),
    path("Student_Home_Profile_Password_Change",views.Student_Home_Profile_Password_Change,name="Student_Home_Profile_Password_Change"),
    path("Student_Home_Attendance_Show",views.Student_Home_Attendance_Show,name="Student_Home_Attendance_Show"),
    path("Student_Home_Subject_Attendance",views.Student_Home_Subject_Attendance,name="Student_Home_Subject_Attendance"),
    path("Teacher_Home_Base",views.Teacher_Home_Base,name="Teacher_Home_Base"),
    path("Teacher_Home",views.Teacher_Home,name="Teacher_Home"),
    path("Teacher_Home_Student_Data",views.Teacher_Home_Student_Data,name="Teacher_Home_Student_Data"),
    path("Teacher_Home_Student_Data_Show/<str:StudentID>/",views.Teacher_Home_Student_Data_Show,name="Teacher_Home_Student_Data_Show"),
    path('Teacher_Home_Student_Data_Show', views.Teacher_Home_Student_Data_Show, name='Teacher_Home_Student_Data_Show'),
    #path('Teacher_Home_Attendance_Data/<str:StudentID>/', views.Teacher_Home_Attendance_Data, name='Teacher_Home_Attendance_Data'),
    path('Teacher_Home_Attendance_Data', views.Teacher_Home_Attendance_Data, name='Teacher_Home_Attendance_Data'),
    path('Teacher_Home_New_Attendance', views.Teacher_Home_New_Attendance, name='Teacher_Home_New_Attendance'),
    path('video_feed/', views.video_feed, name='video_feed'),
    path("stop_feed/", views.stop_feed, name="stop_feed"),
    path('gen_frames', views.gen_frames, name='gen_frames'),
    path('Teacher_Home_New_Attendance_Select', views.Teacher_Home_New_Attendance_Select, name='Teacher_Home_New_Attendance_Select'),
    path('Teacher_Home_LectureData', views.Teacher_Home_LectureData, name='Teacher_Home_LectureData'),
    #path('Teacher_Home_New_Attendance_Live', views.Teacher_Home_New_Attendance_Live, name='Teacher_Home_New_Attendance_Live'),

    path('DatabaseAdministrator_Base', views.DatabaseAdministrator_Base, name='DatabaseAdministrator_Base'),
    path('DatabaseAdministrator_Login', views.DatabaseAdministrator_Login, name='DatabaseAdministrator_Login'),
    path('DatabaseAdministrator_Home', views.DatabaseAdministrator_Home, name='DatabaseAdministrator_Home'),
    path('DatabaseAdministrator_DepartmentSemester', views.DatabaseAdministrator_DepartmentSemester, name='DatabaseAdministrator_DepartmentSemester'),
    path('DepartmentandSemestre_AddNew', views.DepartmentandSemestre_AddNew, name='DepartmentandSemestre_AddNew'),
    path('DepartmentandSemestre_Updatedata', views.DepartmentandSemestre_Updatedata, name='DepartmentandSemestre_Updatedata'),
    path('DepartmentandSemestre_Deletedata/<int:id>/', views.DepartmentandSemestre_Deletedata, name='DepartmentandSemestre_Deletedata'),
    path('DepartmentandSemestre_Deletedata', views.DepartmentandSemestre_Deletedata, name='DepartmentandSemestre_Deletedata'),
    
    path('DatabaseAdministrator_TeacherData', views.DatabaseAdministrator_TeacherData, name='DatabaseAdministrator_TeacherData'),
    path('TeacherData_AddNew', views.TeacherData_AddNew, name='TeacherData_AddNew'),
    path('TeacherData_Updatedata', views.TeacherData_Updatedata, name='TeacherData_Updatedata'),
    path('TeacherData_Deletedata/<int:id>/', views.TeacherData_Deletedata, name='TeacherData_Deletedata'),
    path('TeacherData_Deletedata', views.TeacherData_Deletedata, name='TeacherData_Deletedata'),

    path('DatabaseAdministrator_StudentData', views.DatabaseAdministrator_StudentData, name='DatabaseAdministrator_StudentData'),
    path('StudentData_Updatedata', views.StudentData_Updatedata, name='StudentData_Updatedata'),
    path('StudentData_Deletedata/<int:id>/', views.StudentData_Deletedata, name='StudentData_Deletedata'),
    path('StudentData_Deletedata', views.StudentData_Deletedata, name='StudentData_Deletedata'),

    path('DatabaseAdministrator_SubjectData', views.DatabaseAdministrator_SubjectData, name='DatabaseAdministrator_SubjectData'),
    path('SubjectData_AddNew', views.SubjectData_AddNew, name='SubjectData_AddNew'),
    path('SubjectData_Updatedata', views.SubjectData_Updatedata, name='SubjectData_Updatedata'),
    path('SubjectData_Deletedata/<int:id>/', views.SubjectData_Deletedata, name='SubjectData_Deletedata'),
    path('SubjectData_Deletedata', views.SubjectData_Deletedata, name='SubjectData_Deletedata'),

    path('DatabaseAdministrator_StudentRegistration', views.DatabaseAdministrator_StudentRegistration, name='DatabaseAdministrator_StudentRegistration'),
    path('StudentRegistration_AddNew', views.StudentRegistration_AddNew, name='StudentRegistration_AddNew'),
    path('StudentRegistration_Updatedata', views.StudentRegistration_Updatedata, name='StudentRegistration_Updatedata'),
    path('StudentRegistration_Deletedata/<int:id>/', views.StudentRegistration_Deletedata, name='StudentRegistration_Deletedata'),
    path('StudentRegistration_Deletedata', views.StudentRegistration_Deletedata, name='StudentRegistration_Deletedata'),

    path('DatabaseAdministrator_TeacherLectureData', views.DatabaseAdministrator_TeacherLectureData, name='DatabaseAdministrator_TeacherLectureData'),

    path('DatabaseAdministrator_List', views.DatabaseAdministrator_List, name='DatabaseAdministrator_List'),
    path('DatabaseAdministrator_AddNew', views.DatabaseAdministrator_AddNew, name='DatabaseAdministrator_AddNew'),
    path('DatabaseAdministrator_Updatedata', views.DatabaseAdministrator_Updatedata, name='DatabaseAdministrator_Updatedata'),
    path('DatabaseAdministrator_Deletedata/<int:id>/', views.DatabaseAdministrator_Deletedata, name='DatabaseAdministrator_Deletedata'),
    path('DatabaseAdministrator_Deletedata', views.DatabaseAdministrator_Deletedata, name='DatabaseAdministrator_Deletedata'),

    path('logout/', LogoutView.as_view(next_page='DatabaseAdministrator_Login'), name='logout'),
    path('Teacherlogout/', LogoutView.as_view(next_page='Teacher_Login'), name='Teacherlogout'),
    path('Studentlogout/', LogoutView.as_view(next_page='Student_Login'), name='Studentlogout'),

    #path('logout/', views.logout_view, name='logout'),

]

#if settings.DEBUG:
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)