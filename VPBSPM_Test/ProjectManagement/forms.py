from django import forms 
import re 
from .models import User, Project, Task, Phase 
from django.core.exceptions import ObjectDoesNotExist 

class LoginForm(forms.Form):
    account = forms.CharField(label = 'Id', max_length = 30 )
    password = forms.CharField(label = 'Password', max_length= 30)

    def clean_username(self): 
        account = self.cleaned_data['account']
        try:
            User.objects.get(Account = account)
        except ObjectDoesNotExist:
            raise forms.ValidationError("Account does not exist !")

    def clean_password(self):     
        cleaned_data = super().clean() 
        password = cleaned_data.get("password")
        account = cleaned_data.get("account")
        p = User.objects.get(Account = account)
        if p.Password != password:
            raise forms.ValidationError("Wrong Password !") 

class ProjectForm(forms.Form):
    Name = forms.CharField(max_length=60)
    Description = forms.CharField(max_length=300)
    StartDate = forms.DateField()
    DueDate = forms.DateField()
    Done = forms.IntegerField()

    # def clean_Name(self): 
    #     if 'Name' in self.cleaned_data: 
    #         Name = self.cleaned_data['Name']
    #         if Name not in Project.objects.all(): 
    #             return Name 
    #         raise forms.ValidationError('The project has existed ! ')
    #     raise forms.ValidationError('The forms is failed ! ')

        # if 'Name' in self.cleaned_data:
        #     Name = self.cleaned_data.get['Name']
        #     if Name not in Project.objects.all():
        #         raise forms.ValidationError('The Project has existed !')
        # return Name

    # def clean_DueDate(self):
    #     StartDate = self.cleaned_data['StartDate']
    #     DueDate = self.cleaned_data['DueDate']
    #     if DueDate <= StartDate:
    #         raise forms.ValidationError('The DueDate can not be earlier than StartDate ! ')
    #     return self.cleaned_data['DueDate']

    def save(self): 
        Project.objects.create_project(
            Name = self.cleaned_data['name'],
            Description = self.cleaned_data['description'],
            StartDate = self.cleaned_data['startDate'],
            DueDate = self.cleaned_data['dueDate'],
            Done = self.cleaned_data['done'],
            )
    
    def delete(self): 
        cleaned_data = super().clean() 
        pname = cleaned_data.get("name") 
        Project.objects.remove(pname) 


class TaskForm(forms.Form):
    Name = forms.CharField(max_length=60)
    Description = forms.CharField(max_length=300)
    StartDate = forms.DateField()
    DueDate = forms.DateField()
    Done = forms.IntegerField()
    Status = forms.CharField()
    Priority = forms.CharField()
    Assignee_id = forms.IntegerField()
    
    def clean_task(self): 
        cleaned_data = super().clean() 
        tname = cleaned_data.get("Name")
        if tname not in Project.objects.all():
            raise forms.ValidationError("Task has been existed !")
    
    def clean_DueDate(self):
        cleaned_data = super().clean()
        sd = cleaned_data.get("StartDate")
        dd = cleaned_data.get("DueDate")
        if dd>=sd: 
            raise forms.ValidationError("Due date can not be ealier than start date !")

    def save(self): 
        Task.objects.create_task(
            Name = self.cleaned_data['name'],
            Description = self.cleaned_data['description'],
            StartDate = self.cleaned_data['startDate'],
            DueDate = self.cleaned_data['dueDate'],
            Done = self.cleaned_data['done'],
        )

    def delete(self): 
        cleaned_data = super().clean() 
        tname = cleaned_data.get("name") 
        Task.objects.remove(tname) 

class PhaseForm(forms.Form): 
    Name = forms.CharField(max_length=60)
    StartDate = forms.DateField()
    DueDate = forms.DateField()
    Done = forms.IntegerField()
    Status = forms.CharField()

    # def clean_phase(self): 
    #     cleaned_data = super().clean() 
    #     phasename = cleaned_data.get("Name")
    #     if phasename not in Phase.objects.all():
    #         raise forms.ValidationError("Phase has been existed !")
    
    # def clean_DueDate(self):
    #     cleaned_data = super().clean()
    #     sd = cleaned_data.get("StartDate")
    #     dd = cleaned_data.get("DueDate")
    #     if dd >= sd : 
    #         raise forms.ValidationError("Due date can not be ealier than start date !")

    # def save(self): 
    #     Phase.objects.create_task(
    #         Name = self.cleaned_data['Name'],
    #         StartDate = self.cleaned_data['StartDate'],
    #         DueDate = self.cleaned_data['DueDate'],
    #         Done = self.cleaned_data['Done'],
    #     )

    # def delete(self): 
    #     cleaned_data = super().clean() 
    #     tname = cleaned_data.get("Name") 
    #     Phase.objects.remove(tname) 

class AddUserForm(forms.Form): 
    user = forms.IntegerField()

class AddUrlForm(forms.Form): 
    url = forms.URLField()