from django.urls import path
from timetable import views
from django.views.generic import (
    CreateView, DetailView, ListView, UpdateView, DeleteView, TemplateView)
from absence.views import (AbsenceListView, NewAbsenceView, PrivateAbsenceListView)
app_name = 'absence'
 
urlpatterns = [
    path('', AbsenceListView.as_view(), name='absencelist'),
    path('<int:sid>', PrivateAbsenceListView.as_view(), name='privateabsencelist'),
    path('newabsence', NewAbsenceView.as_view(), name='newabsence'),
] 
