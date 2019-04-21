from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse, Http404, HttpResponseRedirect
from django.template import loader
from django.views.generic import (CreateView, DetailView, ListView, UpdateView, DeleteView)
from django.urls import reverse
from .models import Project, Task, User, Phase, Common_User_Project, Common_User_Task, Feedback, File, QA
from .forms import LoginForm, ProjectForm, TaskForm, PhaseForm, AddUserForm, AddUrlForm

def index(request, user_id):
    usr = User.objects.get(pk=user_id)
    return render(request, 'ProjectManagement/index.html',{'user':usr})

def login(request):
    if request.method == 'POST': 
        acc = request.POST.get('account')
        psw = request.POST.get('password')
        if User.objects.filter(Account=acc) :
            idc = User.objects.get(Account=acc) 
            if idc.Password == psw :       
                return HttpResponseRedirect(reverse('ProjectManagement:index',args=(idc.id,)))
            return HttpResponse("Wrong Password !!! ")
        return HttpResponse("Your Account Is Not Existed !!! ")
    form = LoginForm() 
    return render(request, 'ProjectManagement/login.html')


# def detail(request, project_id):
#     try:
#         project = Project.objects.get(pk=project_id)
#     except Project.DoesNotExist:
#         raise Http404("Question does not exist")
#     return render(request, 'ProjectManagement/detail.html', {'project': project})

def tasks(request, user_id, project_id, task_id):
    latest_phase_list = Phase.objects.order_by(Task_id=task_id)
    usr = User.objects.get(pk=user_id)
    tsk = Task.objects.get(pk=task_id)
    prj = Project.objects.get(pk=project_id)
    common_list = Common_User_Task.objects.filter(Task_id=task_id)
    latest_user_list = []
    for a in common_list:
        c = User.objects.get(pk=a.User_id)
        latest_user_list.append(c)
    context = {'latest_phase_list': latest_phase_list, 'user':usr, 'task':tsk, 'project': prj, 'latest_user_list':latest_user_list}
    return render(request, 'ProjectManagement/tasks.html', context)

def activity(request):
    return render(request, "ProjectManagement/activity.html")

def projectoverview(request, user_id):
    common_list = Common_User_Project.objects.filter(User=user_id)
    usr = User.objects.get(pk=user_id)
    latest_project_list = []
    for a in common_list:
        c = Project.objects.get(pk=a.Project_id)
        latest_project_list.append(c)
    context = {'latest_project_list': latest_project_list, 'user':usr}
    return render(request, 'ProjectManagement/projectoverview.html', context)

def newproject(request, user_id):
    usr = User.objects.get(pk=user_id)
    newpj = Project()
    if request.method == 'POST': 
        form = ProjectForm(request.POST)
        if form.is_valid():
            newpj.Name = request.POST['Name']
            newpj.Description = request.POST['Description']
            newpj.StartDate = request.POST['StartDate']
            newpj.DueDate = request.POST['DueDate']
            newpj.Done = request.POST['Done']
            newpj.Creator = usr
            newrl = Common_User_Project() 
            newrl.User = usr
            if not Project.objects.filter(Name=newpj.Name) and newpj.DueDate > newpj.StartDate:
                newpj.save() 
                newrl.Project = newpj
                newrl.save()
                response = HttpResponse()
                response.write("Your project: <b>" + request.POST['Name'] + "</b> has been created succesfully !!! </br>")
                response.write("<a href=\"projectoverview\"> Back to Project Overview </a> ")
                return response 
            # raise ProjectForm.ValidationError("Project existed or Time is invalid ! ")
            response = HttpResponse()
            response.write("<h1>You've tried to create a new project !</h1></br>")
            response.write("Your project: <b>" + request.POST['Name'] + "</b> has been existed or Dates are Invalid !!! </br>")
            response.write("Please back to previous page and check the infomations !")
            return response 
        return HttpResponseRedirect(reverse('ProjectManagement:projectoverview',args=(user_id,)))
    form = ProjectForm()
    return render(request, 'ProjectManagement/newproject.html', {'form' : form, 'user':usr}) 


def projects(request, project_id, user_id):
    try:
        project = Project.objects.get(pk=project_id)
        usr = User.objects.get(pk=user_id)
        common_list = Common_User_Project.objects.filter(Project=project_id)
        latest_user_list = []
        for a in common_list:
            c = User.objects.get(pk=a.User_id)
            latest_user_list.append(c)
        context = {'project': project, 'user':usr, 'latest_user_list':latest_user_list}
    except Project.DoesNotExist:
        raise Http404("Project does not exist")
    return render(request, 'ProjectManagement/projects.html', context)

def editproject(request, project_id, user_id):
    # try:
    #     project = Project.objects.get(pk=project_id)
    # except Project.DoesNotExist:
    #     raise Http404("Project does not exist")
    # return render(request, 'ProjectManagement/editproject.html', {'project': project})
    usr = User.objects.get(pk=user_id)
    project = Project.objects.get(pk=project_id)
    if request.method == 'POST' : 
        form = ProjectForm(request.POST)
        # if form.is_valid():
        # project.Name = request.POST['Name']
        project.Description = request.POST['Description']
        project.StartDate = request.POST['StartDate']
        project.DueDate = request.POST.get('DueDate')
        project.Done = request.POST['Done']
        if (not Project.objects.filter(Name=request.POST['Name']) or project.Name == request.POST['Name'] ) and project.DueDate > project.StartDate:
            project.Name = request.POST['Name']
            project.save() 
            response = HttpResponse()
            response.write("Your project: <b>" + request.POST['Name'] + "</b> has been edited succesfully !!! </br>")
            response.write("<a href=\".\"> Back to Project Overview </a> ")
            return response 
        response = HttpResponse()
        response.write("<h1>You've tried to create a new project !</h1></br>")
        response.write("Your project: <b>" + request.POST['Name'] + "</b> has been existed or Dates are Invalid !!! </br>")
        response.write("Please back to previous page check the informations !")
        return response 
        # response = HttpResponse()
        # response.write("Form Unvalid")
        # return response        
        # return render(request, 'ProjectManagement/editproject.html', {'project': project})
    form = ProjectForm()
    return render(request, 'ProjectManagement/editproject.html', {'form' : form, 'project': project, 'user':usr}) 

def newtask(request, user_id, project_id):
    project = Project.objects.get(pk=project_id)
    usr = User.objects.get(pk=user_id)
    if request.method == 'POST': 
        form = TaskForm(request.POST)
        if form.is_valid():
            newtask = Task()    
            newtask.Name = request.POST['Name']
            newtask.Description = request.POST['Description']
            newtask.StartDate = request.POST['StartDate']
            newtask.DueDate = request.POST['DueDate']
            newtask.Done = request.POST['Done']
            newtask.Project = project
            newtask.Status = request.POST['Status']
            newtask.Priority = request.POST.get('Priority',False)
            newtask.Assignee_id = request.POST.get('Assignee_id')
            if not Task.objects.filter(Name=newtask.Name)&Task.objects.filter(Project_id=project_id) and newtask.DueDate > newtask.StartDate:
                newtask.save() 
                newrl = Common_User_Task() 
                newrl.User_id = user_id 
                newrl.Task_id = newtask.id 
                newrl.save() 
                response = HttpResponse()
                response.write("Your task: <b>" + request.POST['Name'] + "</b> has been created succesfully !!! </br>")
                response.write("<a href=\".\"> Back to Project Overview </a> ")
                return response 
            # raise ProjectForm.ValidationError("Project existed or Time is invalid ! ")
            response = HttpResponse()
            response.write("<h1>You've tried to create a new task !</h1></br>")
            response.write("Your task: <b>" + request.POST['Name'] + "</b> has been existed or Dates are Invalid !!! </br>")
            response.write("Please back to previous page and check the infomations !")
            return response 
        return render(request, 'ProjectManagement/newtask.html', {'user':usr ,'project': project})
    form = TaskForm()
    return render(request, 'ProjectManagement/newtask.html', {'form' : form, 'project':project, 'user': usr }) 

def edittask(request, user_id, project_id, task_id):
    project = Project.objects.get(pk=project_id)
    task = Task.objects.get(pk=task_id)
    usr = User.objects.get(pk=user_id)
    if request.method == 'POST' : 
        form = TaskForm(request.POST)
        if form.is_valid():
            task.Name = request.POST['Name']
            task.Description = request.POST['Description']
            task.StartDate = request.POST['StartDate']
            task.DueDate = request.POST['DueDate']
            task.Done = request.POST['Done']
            task.Project = project
            task.Status = request.POST['Status']
            task.Priority = request.POST['Priority']
            task.Assignee_id = request.POST.get('Assignee_id')
            if (not Task.objects.filter(Name=request.POST['Name']&Task.objects.filter(Project_id=project_id)) or task.Name == request.POST['Name'] ) and task.DueDate > task.StartDate:
                task.Name = request.POST['Name']
                task.save() 
                response = HttpResponse()
                response.write("Your task: <b>" + request.POST['Name'] + "</b> has been edited succesfully !!! </br>")
                response.write("<a href=\".\"> Back to Project Overview </a> ")
                return response 
            response = HttpResponse()
            response.write("<h1>You've tried to create a new project !</h1></br>")
            response.write("Your task: <b>" + request.POST['Name'] + "</b> has been existed or Dates are Invalid !!! </br>")
            response.write("Please back to previous page check the informations !")
            return response 
        # response = HttpResponse()
        # response.write("Form Unvalid")
        # return response        
        # return render(request, 'ProjectManagement/editproject.html', {'project': project})
        return render(request, 'ProjectManagement/edittask.html', {'project': project, 'task': task})
    form = TaskForm()
    return render(request, 'ProjectManagement/edittask.html', {'form' : form, 'project': project, 'task' : task, 'user':usr}) 

def adduser(request, user_id, project_id):
    form = AddUserForm()
    usr = User.objects.get(pk=user_id)
    prj = Project.objects.get(pk=project_id)
    context = {'form':form, 'user':usr, 'project': prj}
    if request.method == 'POST' : 
        form = AddUserForm(request.POST)
        if form.is_valid():
            uid = request.POST.get('user') 
            common_u_p = Common_User_Project.objects.filter(Project_id=project_id)
            for a in common_u_p:
                if a.User_id == uid: 
                    return HttpResponse("User Has Already Been In This Project ! ") 
            newcommon = Common_User_Project() 
            newcommon.Project_id = project_id
            newcommon.User_id = uid 
            newcommon.save() 
            return HttpResponseRedirect(reverse('ProjectManagement:projects',args=(user_id, project_id)))
        return HttpResponse("The Form You Filled Was Invalid ! ")
    return render(request, "ProjectManagement/adduser.html",context) 

def addusertask(request, user_id, project_id, task_id):
    form = AddUserForm()
    usr = User.objects.get(pk=user_id)
    prj = Project.objects.get(pk=project_id)
    tsk = Task.objects.get(pk=task_id)
    context = {'form':form, 'user':usr, 'task': tsk, 'project': prj}
    if request.method == 'POST' : 
        form = AddUserForm(request.POST)
        if form.is_valid():
            uid = int(request.POST.get('user'))
            common_u_t = Common_User_Task.objects.filter(Task_id=task_id)
            for a in common_u_t:
                if a.User_id == uid:
                    return HttpResponse("User Has Already Been In This Task ! ") 
            common_u_p = Common_User_Project.objects.filter(Project_id=project_id)
            for a in common_u_p:
                if a.User_id == uid: 
                    newcommon = Common_User_Task() 
                    newcommon.Task_id = task_id
                    newcommon.User_id = uid 
                    newcommon.save()
                    return HttpResponseRedirect(reverse('ProjectManagement:tasks',args=(user_id, project_id , task_id)))
            return HttpResponse("The user must have been added to Project ! ")
        return HttpResponse("The Form You Filled Was Invalid ! ")
    return render(request, "ProjectManagement/addusertask.html",context) 

def newphase(request, user_id, project_id, task_id): 
    project = Project.objects.get(pk=project_id)
    usr = User.objects.get(pk=user_id)
    tsk = Task.objects.get(pk=task_id)
    if request.method == 'POST': 
        form = PhaseForm(request.POST)
        if form.is_valid():
            newphase = Phase()    
            newphase.Name = request.POST['Name']
            newphase.StartDate = request.POST.get('StartDate')
            newphase.DueDate = request.POST.get('DueDate')
            newphase.Done = request.POST.get('Done')
            newphase.Task = tsk
            newphase.Status = request.POST['Status']
            if not Phase.objects.filter(Name=newphase.Name)&Phase.objects.filter(Task_id=task_id) and newphase.DueDate > newphase.StartDate:
                newphase.save() 
                response = HttpResponse()
                response.write("Your phase: <b>" + request.POST['Name'] + "</b> has been created succesfully !!! </br>")
                response.write("<a href=\".\"> Back to last page </a> ")
                return response 
            # raise ProjectForm.ValidationError("Project existed or Time is invalid ! ")
            response = HttpResponse()
            response.write("<h1>You've tried to create a new phase !</h1></br>")
            response.write("Your phase: <b>" + request.POST['Name'] + "</b> has been existed or Dates are Invalid !!! </br>")
            response.write("Please back to previous page and check the infomations !")
            return response 
        return render(request, 'ProjectManagement/newphase.html', {'user':usr ,'project': project, 'task':tsk})
    form = PhaseForm()
    return render(request, 'ProjectManagement/newphase.html', {'form' : form, 'project':project, 'user': usr, 'task':tsk}) 

def news(request, user_id):
    return render(request, "ProjectManagement/news.html") 

def support(request, user_id):
    latest_user_list = User.objects.order_by('id')
    usr = User.objects.get(pk=user_id)
    return render(request, "ProjectManagement/support.html",{'user':usr, 'latest_user_list': latest_user_list }) 

def gantt(request, user_id):
    return render(request, "ProjectManagement/gantt.html") 

def forgot_password(request):
    return render(request, "ProjectManagement/forgot_password.html") 


def detail(request, project_id):
    project = get_object_or_404(Project, pk=project_id)
    return render(request, 'ProjectManagement/detail.html', {'project': project})

# def tasks(request, project_id):
#     response = "You're looking at the tasks of project %s."
#     return HttpResponse(response % project_id)

def user(request, project_id):
    return HttpResponse("You're looking at users on project %s." % project_id)

def subindex(request):
    latest_project_list = Project.objects.order_by('-DueDate')[:5]
    context = {'latest_project_list': latest_project_list}
    return render(request, 'ProjectManagement/subindex.html', context)

def addurl(request, user_id, project_id): 
    form = AddUrlForm()
    usr = User.objects.get(pk=user_id)
    prj = Project.objects.get(pk=project_id)
    context = {'form':form, 'user':usr, 'project': prj}
    if request.method == 'POST' : 
        form = AddUrlForm(request.POST)
        if form.is_valid():
            url = request.POST.get('url') 
            prj.Url = url 
            prj.save() 
            return HttpResponseRedirect(reverse('ProjectManagement:projectoverview',args=(user_id,)))
        return HttpResponse("The Form You Filled Was Invalid ! ")
    return render(request, "ProjectManagement/addurl.html",context) 