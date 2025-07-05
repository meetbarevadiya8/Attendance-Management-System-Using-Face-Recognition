from django.contrib import admin
from .models import StudentData ,TeacherData ,AttendanceData ,SubjectData ,DepartmentandSemestre ,DatabaseAdministratorList ,StudentRegistration ,TeacherLectureData

# Register your models here.
admin.site.register(StudentData)
admin.site.register(TeacherData)
admin.site.register(AttendanceData)
admin.site.register(SubjectData)
admin.site.register(DepartmentandSemestre)
admin.site.register(DatabaseAdministratorList)
admin.site.register(StudentRegistration)
admin.site.register(TeacherLectureData)