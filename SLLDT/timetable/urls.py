from django.urls import path
from timetable import views
from django.views.generic import (
    CreateView, DetailView, ListView, UpdateView, DeleteView, TemplateView)
from timetable.views import (TimetableView, PrivateTimeTableView)
app_name = 'timetable'
 
urlpatterns = [
    path('', TimetableView.as_view(), name='timetable'),
    path('<int:sid>', PrivateTimeTableView.as_view(), name='privatetimetable'), 
] 
