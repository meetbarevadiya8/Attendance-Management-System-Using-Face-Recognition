from django.db import models

# Create your models here.
class StudentData(models.Model):
    StudentID = models.CharField(max_length=20,primary_key=True,default=0)
    Student_Name = models.CharField(max_length=150,default=0)
    CollageCode = models.CharField(max_length=30,default=0)
    Semestre = models.CharField(max_length=5,default=0)
    Department = models.CharField(max_length=20,default=0)
    Email = models.EmailField(unique=True,default=0)
    Mobile = models.CharField(max_length=10,unique=True,default=0,null=True)
    Password = models.CharField(max_length=128)  # Consider hashing passwords in a real app
    Profile_Photo = models.ImageField(upload_to='Student_Profile_Photos/',blank=True, null=True, default='Student_Profile_Photos/default-profile.png')

    def __str__(self):
        return self.StudentID
    

class TeacherData(models.Model):
    TeacherID = models.CharField(max_length=20,primary_key=True,default=0)
    Teacher_Name = models.CharField(max_length=150,default=0)
    CollageCode = models.CharField(max_length=30,default=0)
    Department = models.CharField(max_length=20,default=0)
    Email = models.EmailField(unique=True,default=0)
    Mobile = models.CharField(max_length=10,unique=True,default=0)
    Password = models.CharField(max_length=128)  # Consider hashing passwords in a real app
    Profile_Photo = models.ImageField(upload_to='Teacher_Profile_Photos/',blank=True, null=True,default='Teacher_Profile_Photos/default-profile.png')

    def __str__(self):
        return self.TeacherID
    

class AttendanceData(models.Model):
    AttendanceDataID = models.CharField(max_length=50,primary_key=True,default=0)
    StudentID = models.CharField(max_length=20,default=0)
    Subject_Name = models.CharField(max_length=30,default=0)
    Subject_Code = models.CharField(max_length=30,default=0)
    TeacherID = models.CharField(max_length=20,default=0)
    CollageCode = models.CharField(max_length=30,default=0)
    AttendanceTime = models.TimeField(null=True, blank=True)  # Add a time field
    AttendanceDay = models.CharField(max_length=20,default=0)
    AttendanceDate = models.DateField(default=0)
    
    class Meta:
        unique_together = ('StudentID', 'Subject_Name', 'AttendanceDate', 'AttendanceTime')
    def __str__(self):
        return self.AttendanceDataID

class TeacherLectureData(models.Model):
    TeacherLectureDataID = models.CharField(max_length=20,primary_key=True,default=0)
    TeacherID = models.CharField(max_length=20,default=0)
    Teacher_Name = models.CharField(max_length=150,default=0)
    Department = models.CharField(max_length=20,default=0)
    Semestre = models.CharField(max_length=10,default=0)
    Subject_Name = models.CharField(max_length=30,default=0)
    Subject_Code = models.CharField(max_length=30,default=0)
    LectureDate = models.DateField(default=0)
    LectureDay = models.CharField(max_length=20,default=0)
    LectureStartingTime = models.TimeField(null=True, blank=True)  # Add a time field
    LectureEndingTime = models.TimeField(null=True, blank=True)  # Add a time field
    LectureTime = models.TimeField(null=True, blank=True)  # Add a time field

    def __str__(self):
        return self.TeacherLectureDataID
    

# Database

class DepartmentandSemestre(models.Model):
    DepartmentandSemestreID = models.CharField(max_length=20,primary_key=True,default=0)
    Department_Code = models.CharField(max_length=150,default=0)
    Department_Name = models.CharField(max_length=20,default=0)
    Semestre = models.CharField(max_length=10,default=0)

    def __str__(self):
        return self.DepartmentandSemestreID
    
    
class DatabaseAdministratorList(models.Model):
    DatabaseAdministratorID = models.CharField(max_length=50,primary_key=True,default=0)
    DatabaseAdministrator_Name = models.CharField(max_length=30,default=0)
    DatabaseAdministrator_Code = models.CharField(max_length=30,default=0)
    DatabaseAdministrator_CollageCode = models.CharField(max_length=30,default=0)
    DatabaseAdministrator_Email = models.EmailField(unique=True,default=0)
    DatabaseAdministrator_Mobile = models.CharField(max_length=10,unique=True,default=0)
    Password = models.CharField(max_length=128)  # Consider hashing passwords in a real app
    LoginStatus = models.BooleanField(default=False) 

    def __str__(self):
        return self.DatabaseAdministratorID
    
class StudentRegistration(models.Model):
    StudentID = models.CharField(max_length=20,primary_key=True,default=0)
    Student_Name = models.CharField(max_length=150,default=0)
    CollageCode = models.CharField(max_length=30,default=0)
    Department = models.CharField(max_length=20,default=0)
    DateOfBirth = models.DateField(default=0, null=True)
    Email = models.EmailField(unique=True,default=0)
    Mobile = models.CharField(max_length=10,unique=True,default=0)
    RegistrationDate = models.DateField(default=0, null=True)

    def __str__(self):
        return self.StudentID

class SubjectData(models.Model):
    SubjectDataID = models.CharField(max_length=20,primary_key=True,default=0)
    Subject_Name = models.CharField(max_length=150,default=0)
    Subject_Code = models.CharField(max_length=30,default=0)
    Department = models.CharField(max_length=20,default=0)
    Semestre = models.CharField(max_length=5,default=0)


    def __str__(self):
        return self.SubjectDataID