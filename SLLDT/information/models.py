""" Create models table for db """
import time 
from django.utils import timezone
import datetime
from datetime import date 
from information.utils import DAY_TYPES, SCORE_TYPE, SUBJECT_TYPE
from django.db import models    
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, UserManager
from django.contrib.postgres.fields import ArrayField
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

    def getMyNumberStudents(self): 
        return Student.objects.filter(user_id=self.id).count()  

    def getMyStudents(self): 
        return Student.objects.filter(user_id=self.id) 

    def getNotification(self): 
        StudentList = self.getYourStudents() 
        NotifyList = []
        for std in StudentList: 
            NotifyList.append(std.getNotification()) 
        return NotifyList
    
class Class(models.Model):
    name = models.CharField(max_length=10)
    # monitor_id = models.ForeignKey(Student, on_delete=models.CASCADE, related_name='monitor')
    # vice_monitor_id = models.ForeignKey(Student, on_delete=models.CASCADE, related_name='vice_monitor')
    secretary = models.ForeignKey(User, on_delete=models.CASCADE, related_name='secretary')
    study_time = models.CharField(default="2019-2022", max_length=11)
    class Meta: 
        ordering = ('name',)
    
    
    def __str__(self): 
        return self.name 

    def getTimeTableList(self):
        TTList = TimeTable.objects.filter(classes=self)
        firstLesssonList = []
        secondLesssonList = []
        thirdLesssonList = []
        fourthLesssonList = []
        fifthLesssonList = []
        for Weekdays in TTList:
            firstLesssonList.append(Weekdays.lesson1)
            secondLesssonList.append(Weekdays.lesson2)
            thirdLesssonList.append(Weekdays.lesson3)
            fourthLesssonList.append(Weekdays.lesson4)
            fifthLesssonList.append(Weekdays.lesson5)
        context = [firstLesssonList, secondLesssonList, thirdLesssonList, fourthLesssonList, fifthLesssonList]
        return context 
    def getClassStudentList(self):
        studentList = Student.objects.filter(class_id=self) 
        return StudentList     
    def getTeacherList(self): 
        return Teacher.objects.filter(class_id=self) 



class Student(models.Model): 
    name = models.CharField(max_length = 100 )
    dob = models.DateField(default=date.today ) 
    class_id = models.ForeignKey(Class, on_delete=models.CASCADE, related_name='students') 
    user_id = models.ForeignKey(User, on_delete=models.CASCADE, related_name='children') 

    class Meta: 
        ordering = ('name', )

    def __str__(self): 
        return self.name 

    def getTimeTable(self): 
        _class = Class.objects.get(id=class_id) 
        return _class.getTimeTableList 

    def getClassStudentList(self): 
        _class = Class.objects.get(id=class_id)
        return _class.getClassStudentList

    def getNotification(self):
        return Notification.objects.filter(student_id=self, is_seen=False)

    def getMarkSheet(self): 
        StudentScore = MarkSheet.objects.filter(student_id=self) 
        listSinh = StudentScore.filter(subject_id=1)
        listToan = StudentScore.filter(subject_id=2)
        listSu = StudentScore.filter(subject_id=3)
        listDia = StudentScore.filter(subject_id=4)
        listLy = StudentScore.filter(subject_id=5)
        listHoa = StudentScore.filter(subject_id=6)
        listVan = StudentScore.filter(subject_id=7)
        listNgoai = StudentScore.filter(subject_id=8)
        listTheDuc = StudentScore.filter(subject_id=9)
        listCongDan = StudentScore.filter(subject_id=10)
        listAmNhac = StudentScore.filter(subject_id=11)
        listMyThuat = StudentScore.filter(subject_id=12)
        listCongNghe = StudentScore.filter(subject_id=13)
        listTin = StudentScore.filter(subject_id=15)
        listScore = [listSinh, listToan, listSu, listDia, listLy, listHoa, listVan, listNgoai,
                    listTheDuc, listCongDan, listAmNhac, listMyThuat, listCongNghe, listTin ]
        return listScore

    def getCheckIn(self): 
        return Check_in.objects.fitler(student_id=self)[:30]

    def isNotified(self): 
        NotiList = Notification.objects.filter(student_id=self).filter(is_seen = False)
        NotiNum = NotiList.len() 
        if(NotiNum):
            return True 
        else:
            return False 
        
    def updateNotification(self): 
        myParent = User.objects.get(self.user_id)
        myScoreList = MarkSheet.objects.filter(student_id=self).filter(update_time__gte=myParent.last_login_start).filter(isNotified=False)
        myAbsenceList = Absence.objects.filter(student_id=self).filter(approved_time__gte=myParent.last_login_start).filter(isNotified=False)
        myCheckInList = Check_in.objects.filter(student_id=self).filter(update_time__gte=myParent.last_login_start).filter(isNotified=False)
        for sc in myScoreList: 
            sc.isNotified = True 
            newnoti = Notification()
            newnoti.content = sc.getNoti() 
            newnoti.student_id = self 
            newnoti.save() 
        for al in myAbsenceList: 
            al.isNotified = True
            newnoti = Notification()
            newnoti.content = al.getNoti()
            newnoti.student_id = self
            newnoti.save()
        for ck in myCheckInList: 
            ck.isNotified = True
            newnoti = Notification()
            newnoti.content = ck.getNoti()
            newnoti.student_id = self
            newnoti.save()
        
class Subject(models.Model): 
    name = models.CharField(max_length= 100, choices=SUBJECT_TYPE) 
    def __str__(self): 
        return self.name 

class Teacher(models.Model): 
    name = models.CharField(max_length = 100 ) 
    dob = models.DateField(default=date.today) 
    class_list = models.ManyToManyField(Class, related_name='teachers') 
    isHeadTeacher = models.BooleanField(default=True) 
    subjects = models.ForeignKey(Subject,on_delete=models.CASCADE, related_name='teachers', default=1) 
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
    update_time = models.DateTimeField(default=timezone.now)
    isNotified = models.BooleanField(default=False)
    class Meta:     
        ordering = ('date', )

    def __str__(self): 
        return "Ngày " + self.date + " học sinh " + self.student_id.name + " nghỉ học !"

class TimeTable(models.Model): 
    classes = models.ForeignKey(Class, on_delete=models.CASCADE, related_name='class_belong')
    days = models.CharField("Thứ", choices=DAY_TYPES, max_length=50) 
    lesson1 = models.ForeignKey(Subject, on_delete=models.CASCADE, related_name='lesson1', default='0')
    lesson2 = models.ForeignKey(Subject, on_delete=models.CASCADE, related_name='lesson2', default='1')
    lesson3 = models.ForeignKey(Subject, on_delete=models.CASCADE, related_name='lesson3', default='2')
    lesson4 = models.ForeignKey(Subject, on_delete=models.CASCADE, related_name='lesson4', default='3')
    lesson5 = models.ForeignKey(Subject, on_delete=models.CASCADE, related_name='lesson5', default='4') 
    # lesson = ArrayField(Subject)
    def __str__(self): 
        return self.classes.name + "_" + self.days
    
    
class Absence (models.Model): 
    time = models.DateField(default=date.today )
    reason = models.CharField(default="Phụ huynh chưa điền thông tin nghỉ phép", max_length= 200)
    student_id = models.ForeignKey(Student, on_delete=models.CASCADE)   
    approved_time = models.DateTimeField(default=timezone.now) 
    isNotified = models.BooleanField(default=False)
    def __str__(self): 
        return self.time 
    def getNoti(self): 
        return "Đơn xin nghỉ cho học sinh " + str(self.student_id) + " vào ngày " + str(self.time) + " đã được chấp thuận vào lúc " + str(self.approved_time)

class MarkSheet(models.Model): 
    time = models.DateField(default=date.today)
    student_id = models.ForeignKey(Student, on_delete=models.CASCADE)
    score = models.FloatField(default=0) 
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE) 
    mark_type = models.CharField('Loại điểm', choices=SCORE_TYPE, max_length = 40 )
    multi = models.PositiveSmallIntegerField(default=1)
    update_time = models.DateTimeField(default=timezone.now)
    isNotified = models.BooleanField(default=False)
    
    def __str__(self):
        return self.mark_type
    def getNoti(self):
        return str(self.student_id) + " đạt điểm " + str(self.score) + " " + str(self.mark_type) + " môn " + str(self.subject) + " vào ngày " + str(self.time)

class Notification(models.Model): 
    time = models.DateTimeField(default=timezone.now) 
    student_id = models.ForeignKey(Student, on_delete=models.CASCADE) 
    content = models.CharField(max_length=300, default="") 
    is_seen = models.BooleanField(default=False)  
