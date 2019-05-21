from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse, Http404, HttpResponseRedirect
from django.template import loader
from django.urls import reverse
from django.contrib.auth.mixins import LoginRequiredMixin, AccessMixin
from django.contrib.auth import logout, authenticate, login, hashers
from datetime import datetime, date
import datetime
import re
from django.views.generic import (
    CreateView, DetailView, ListView, UpdateView, DeleteView, View, TemplateView)
from information.models import User, Student, Class, TimeTable, Check_in, Absence

class AbsenceListView(LoginRequiredMixin, TemplateView):
    template_name = "absence/absence.html"

    def get(self, request, *args, **kwargs):
        usr = request.user
        myStudent = usr.getMyStudents() #Get students list 
        firststd = myStudent[0] 
        absenceList = firststd.getAbsenceList()
        context = {'user': usr, 'myStudent': myStudent, 'absenceList': absenceList}
        return render(request, 'absence/absence.html', context)


class PrivateAbsenceListView(LoginRequiredMixin, TemplateView):
    template_name = "absence/absence.html"

    def get(self, request, *args, **kwargs): 
        usr = request.user
        myStudent = usr.getMyStudents()  # Get students list
        student_id = kwargs.get('sid', None)
        selectedstd = Student.objects.get(pk=student_id)
        absenceList = selectedstd.getAbsenceList()
        context = {'user': usr, 'myStudent': myStudent, 'absenceList': absenceList,'selectedstd': selectedstd }
        return render(request, 'absence/absence.html', context)

class NewAbsenceView( LoginRequiredMixin, TemplateView): 
    template_name = "absence/newabsence.html" 

    def get(self, request, *args, **kwargs): 
        usr = request.user
        myStudent = usr.getMyStudents()
        context = {'user': usr,'myStudent': myStudent }
        return render(request, 'absence/newabsence.html', context) 

    def post(self, request, *args, **kwargs): 
        usr = request.user 
        newabs = Absence() 
        student_id= request.POST["student"] 
        print(student_id)
        std_id = Student.objects.get(id=student_id)
        newabs.student_id = std_id
        newabs.reason = request.POST["reason"]
        newabs.save()
        return redirect('/absence/'+ str(std_id.id) )