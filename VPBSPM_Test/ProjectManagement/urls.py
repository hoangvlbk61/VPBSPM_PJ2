from django.urls import path
from ProjectManagement import views

app_name = 'ProjectManagement'
urlpatterns = [
    #Lv0 App
    path('', views.login, name='login'),    #GIANG
    #Lv1 User 
    path('<int:user_id>/index',views.index, name='index'), 
    path('<int:user_id>/projectoverview',views.projectoverview, name='projectoverview'),
    path('<int:user_id>/activity',views.activity, name='activity'),
    path('<int:user_id>/gantt',views.gantt, name='gantt'),
    # path('projects',views.projects, name='projects'),
    path('<int:user_id>/newproject',views.newproject, name='newproject'),  #TRANG  

    #Lv2 User/Project 
    path('<int:user_id>/<int:project_id>/',views.projects, name='projects'),
    path('<int:user_id>/<int:project_id>/editproject',views.editproject, name='editproject'), 
    path('<int:user_id>/<int:project_id>/<int:task_id>/',views.tasks,name='tasks'), #TAI
    path('<int:user_id>/<int:project_id>/<int:task_id>/edittask',views.edittask, name='edittask'), 
    path('<int:user_id>/<int:project_id>/newtask',views.newtask, name='newtask'), #THANH
    path('<int:user_id>/<int:project_id>/adduser',views.adduser, name='adduser'), 
    path('<int:user_id>/<int:project_id>/<int:task_id>/addusertask',views.addusertask,name='addusertask'), 
    path('<int:user_id>/<int:project_id>/addurl',views.addurl, name='addurl'),
    
    #Lv3 User/Project/Task
    path('<int:user_id>/<int:project_id>/<int:task_id>/newphase',views.newphase, name='newphase'), 
    
    #Lv4 User/Project/Task/Phase
    path('<int:user_id>/news',views.news, name='news'), 
    path('login',views.login, name='login'), 
    path('<int:user_id>/support',views.support, name='support'),  
    path('forgot_password',views.forgot_password, name='forgot_password'), 
]