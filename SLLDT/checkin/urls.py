from django.urls import path
from timetable import views
from django.views.generic import (
    CreateView, DetailView, ListView, UpdateView, DeleteView, TemplateView)
from checkin.views import (CheckinView, PrivateCheckinView )
app_name = 'checkin'
 
urlpatterns = [
    path('', CheckinView.as_view(), name='checkin'),
    path('<int:sid>', PrivateCheckinView.as_view(), name='privatecheckin'), 
] 
