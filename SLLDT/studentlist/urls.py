from django.urls import path
from timetable import views
from django.views.generic import (
    CreateView, DetailView, ListView, UpdateView, DeleteView, TemplateView)
from studentlist.views import (StudentListView, PrivateStudentListView)
app_name = 'studentlist'
 
urlpatterns = [
    path('', StudentListView.as_view(), name='studentlist'),
    path('<int:sid>', PrivateStudentListView.as_view(), name='privatestudentlist'), 
] 
