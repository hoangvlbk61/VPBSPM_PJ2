from django.urls import path
from timetable import views
from django.views.generic import (
    CreateView, DetailView, ListView, UpdateView, DeleteView, TemplateView)
from teacherlist.views import (TeacherListView, PrivateTeacherListView)
app_name = 'teacherlist'
 
urlpatterns = [
    path('', TeacherListView.as_view(), name='teacherlist'),
    path('<int:sid>', PrivateTeacherListView.as_view(), name='privateteacherlist'), 
] 
