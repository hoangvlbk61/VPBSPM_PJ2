""" Create models table for db """
import time 
from django.utils import timezone
import datetime
from datetime import date 
from information.utils import DAY_TYPES, SCORE_TYPE
from django.db import models    
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, UserManager
# from common.utils import USER_TYPE_CHOICES


# Create your models here.

def img_url(self, filename):
    hash_ = int(time.time())
    return "%s/%s/%s" % ("profile_pics", hash_, filename)


class User(AbstractBaseUser, PermissionsMixin):
    file_prepend = "users/profile_pics"
    username = models.CharField(max_length=100, unique=True)
    first_name = models.CharField(max_length=150, blank=True)
    last_name = models.CharField(max_length=150, blank=True)
    email = models.EmailField(max_length=255, unique=True)
    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    date_joined = models.DateTimeField(('date joined'), auto_now_add=True)
    role = models.CharField(max_length=50)
    # user_type = models.PositiveSmallIntegerField(
    #     choices=USER_TYPE_CHOICES, default=5)
    profile_pic = models.FileField(
        max_length=1000, upload_to=img_url, null=True, blank=True)
    
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username', ]

    objects = UserManager()


class Class(models.Model):
    name = models.CharField(max_length=10)
    # monitor_id = models.ForeignKey(Student, on_delete=models.CASCADE, related_name='monitor')
    # vice_monitor_id = models.ForeignKey(Student, on_delete=models.CASCADE, related_name='vice_monitor')
    secretary = models.ForeignKey(User, on_delete=models.CASCADE, related_name='secretary')
    
    class Meta: 
        ordering = ('name',)
    
    def __str__(self): 
        return self.name 

class Student(models.Model): 
    name = models.CharField(max_length = 100 )
    dob = models.DateField(default=date.today ) 
    class_id = models.ForeignKey(Class, on_delete=models.CASCADE, related_name='students') 
    user_id = models.ForeignKey(User, on_delete=models.CASCADE, related_name='children')

    class Meta: 
        ordering = ('name', )
    def __str__(self): 
        return self.name 
    
class Subject(models.Model): 
    name = models.CharField(max_length= 100 ) 

    def __str__(self): 
        return self.name 

class Teacher(models.Model): 
    name = models.CharField(max_length = 100 ) 
    dob = models.DateField(default=date.today) 
    class_list = models.ManyToManyField(Class, related_name='teachers') 
    isHeadTeacher = models.BooleanField(default=True) 
    subjects = models.ManyToManyField(Subject, related_name='teachers') 
    degree = models.CharField(max_length = 100 ) 
    email = models.EmailField(max_length=255, blank=True)
    phone = models.CharField('Số điện thoại', max_length=20) 

    class Meta: 
        ordering = ('name', )
    
    def __str__(self): 
        return self.name

class Check_in(models.Model): 
    date = models.DateField(default = date.today ) 
    student_id = models.ForeignKey(Student, on_delete=models.CASCADE)

    class Meta: 
        ordering = ('date', )

    def __str__(self): 
        return "Ngày " + self.date + " học sinh " + self.student_id.name + " nghỉ học !"

class TimeTable(models.Model): 
    classes = models.ForeignKey(Class, on_delete=models.CASCADE, related_name='class_belong')
    days = models.CharField("Thứ", choices=DAY_TYPES, max_length=50) 
    lesson = models.ManyToManyField(Subject, related_name='lesson') 
    
    def __str__(self): 
        return self.class_id.name 
    
class Absence (models.Model): 
    time = models.DateField(default=date.today )
    reason = models.CharField(default="Phụ huynh chưa điền thông tin nghỉ phép", max_length= 200)
    student_id = models.ForeignKey(Student, on_delete=models.CASCADE) 

    def __str__(self): 
        return self.time 

class MarkSheet(models.Model): 
    time = models.DateField(default=date.today)
    student_id = models.ForeignKey(Student, on_delete=models.CASCADE)
    score = models.PositiveSmallIntegerField(default=0) 
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE) 
    mark_type = models.CharField('Loại điểm', choices=SCORE_TYPE, max_length = 40 )
    multi = models.SmallIntegerField(default=1)
    
    def __str__(self):
         return self.student_id + " đạt điểm " + self.score + " " + self.mark_type + " môn " + self.subject + " vào ngày " + self.time  
