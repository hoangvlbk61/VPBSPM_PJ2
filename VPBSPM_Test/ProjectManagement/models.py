import datetime
from django.db import models
from django.utils import timezone
from enum import Enum

#Time validation

# Task 
class TaskPriority (Enum): 
    "High"
    "Medium"
    "Low"

class TaskStatus(Enum): 
    "Ok"
    "Done"
    "Warning"

class User(models.Model): 
    #UID = models.IntergerField(default=0)
    Account = models.CharField(max_length=30 )  
    Password = models.CharField(max_length=30 ) 
    Email = models.EmailField(max_length=60)
    Fullname = models.CharField(max_length=60)
    DOB = models.DateField('Day Of Birth') 
    Gender = models.CharField(max_length=10) 
    Company = models.CharField(max_length=30) 
    Role = models.CharField(max_length=30)  
    def __str__(self):
        return self.Account
    def perm_createpj(self): 
        return  (self.Role == 'Team Leader' or self.Role == 'Manager')
    def perm_createtask(self):
        return self.Role == 'Team Leader' or self.Role == 'Manager' or self.Role == 'Developer'
    def perm_update_task(self): 
        return self.Role == 'Team Leader' or self.Role == 'Manager' or self.Role == 'Developer' or self.Role == 'Tester'

class Project(models.Model): 
    #PID = models.IntegerField(default=0)
    Name = models.CharField(max_length=60)
    Description = models.CharField(max_length=300, default="Description")
    StartDate = models.DateField('Start Date')
    DueDate = models.DateField('Due Date')
    Done = models.IntegerField(default=0)
    Creator = models.ForeignKey(User ,on_delete=models.CASCADE, default=1)
    Url = models.URLField()
    def __str__(self):
        return self.Name 
    def is_started(self): 
        return self.StartDate <= datetime.date.today()
    def is_late(self): 
        return 100*(datetime.date.today()-self.StartDate)/(self.DueDate-self.StartDate) > self.Done 
    def is_over(self):
        return self.DueDate < datetime.date.today() 
    def is_completed(self): 
        return self.Done == 100 
    def is_submited(self): 
        return self.Url != "0"
    
class Task(models.Model):
    Project = models.ForeignKey(Project, on_delete=models.CASCADE) 
    #TID = models.IntergerField(default=0)
    Name = models.CharField(max_length=30)
    Description = models.CharField(max_length = 300, default="Description") 
    Status = models.CharField(
        max_length=30,
        choices = [(status) for status in TaskStatus]
        )
    Priority = models.CharField(
        max_length = 30,
        choices = [(tag) for tag in TaskPriority]
        )
    # Assignee = models.CharField(max_length = 50)
    Assignee = models.ForeignKey(User,on_delete=models.CASCADE)
    StartDate = models.DateField('Start Date')
    DueDate = models.DateField('Due Date') 
    Done = models.IntegerField(default=0)
    def __str__(self):
        return self.Name
    def is_late(self): 
        return 100*(datetime.date.today()-self.StartDate)/(self.DueDate-self.StartDate) > self.Done 
    def is_over(self):  
        return self.DueDate > datetime.date.today() 
    def is_completed(self): 
        return self.Done == 100 

class Common_User_Task(models.Model): 
    #STT = models.IntergerField(default=0) 
    User = models.ForeignKey(User, on_delete=models.CASCADE)    
    Task = models.ForeignKey(Task, on_delete=models.CASCADE) 

class Common_User_Project(models.Model): 
    User = models.ForeignKey(User, on_delete=models.CASCADE)
    Project = models.ForeignKey(Project, on_delete=models.CASCADE)
    def __str__(self): 
        return self.Project_id

class File(models.Model): 
    #FID = models.IntergerField(default=0)  
    Filename = models.CharField(max_length=60)
    User = models.ForeignKey(User, on_delete=models.CASCADE)
    Task = models.ForeignKey(Task, on_delete=models.CASCADE)
    Description = models.CharField(max_length = 300 , default="Description")
    UploadTime = models.DateField(default=timezone.now)
    FilePath = models.URLField
    def __str__(self):
        return self.Filename

class QA(models.Model):
    #QID = models.IntergerField(default=0) 
    Question = models.CharField(max_length=300) 
    Answer = models.CharField(max_length=300) 
    User = models.ForeignKey(User, on_delete=models.CASCADE)
    Task = models.ForeignKey(Task, on_delete=models.CASCADE)
    def __str__(self):
        return self.Question 

class Feedback(models.Model): 
    #FBID = models.IntergerField(default=0) 
    Feedback = models.CharField(max_length=300) 
    Filename = models.ForeignKey(File, on_delete=models.CASCADE)
    User = models.ForeignKey(User, on_delete=models.CASCADE)
    Project = models.ForeignKey(Project, on_delete=models.CASCADE) 
    UploadTime = models.DateField(default=timezone.now) 
    def __str__(self):
        return self.Feedback
        
class Phase(models.Model):
    Task = models.ForeignKey(Task, on_delete=models.CASCADE) 
    #TID = models.IntergerField(default=0)
    Name = models.CharField(max_length=30)
    Status = models.CharField(
        max_length=30,
        choices = [(status) for status in TaskStatus]
        )
    StartDate = models.DateField('Start Date')
    DueDate = models.DateField('Due Date') 
    Done = models.IntegerField(default=0)
    def __str__(self):
        return self.Name 
    def is_started(self): 
        return self.StartDate <= datetime.date.today()
    def is_late(self): 
        return 100*(datetime.date.today()-self.StartDate)/(self.DueDate-self.StartDate) > self.Done 
    def is_over(self):
        return self.DueDate < datetime.date.today() 
    
    