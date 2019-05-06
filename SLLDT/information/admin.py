from django.contrib import admin

# Register your models here.
from information.models import User, Class, Student, Subject, Teacher, Check_in, TimeTable, Absence, MarkSheet

admin.site.register(User)
admin.site.register(Class)
admin.site.register(Student)
admin.site.register(Subject)
admin.site.register(Teacher)
admin.site.register(Check_in)
admin.site.register(TimeTable)
admin.site.register(Absence)
admin.site.register(MarkSheet)
