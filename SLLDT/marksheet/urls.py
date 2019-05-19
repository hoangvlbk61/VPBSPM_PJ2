from django.urls import path
from marksheet import views
from django.views.generic import (
    CreateView, DetailView, ListView, UpdateView, DeleteView, TemplateView)
from marksheet.views import (MarkSheetView, PrivateMarkSheetView)
app_name = 'marksheet'
 
urlpatterns = [
    path('', MarkSheetView.as_view(), name='marksheet'),
    path('<int:sid>', PrivateMarkSheetView.as_view(), name='privatemarksheet'), 
] 
