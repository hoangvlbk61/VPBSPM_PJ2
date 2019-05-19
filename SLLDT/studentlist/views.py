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
from information.models import User, Student, Class, TimeTable

class StudentListView(LoginRequiredMixin, TemplateView):
    template_name = "studentlist/studentlist.html"

    def get(self, request, *args, **kwargs):
        usr = request.user
        myStudent = usr.getMyStudents() #Get students list 
        firststd = myStudent[0] 
        firstClass = firststd.class_id 
        studentlist = firstClass.getClassStudentList()
        context = {'user': usr, 'myStudent': myStudent, 'studentlist': studentlist}
        return render(request, 'studentlist/studentlist.html', context)


class PrivateStudentListView(LoginRequiredMixin, TemplateView):
    template_name = "studentlist/studentlist.html"

    def get(self, request, *args, **kwargs): 
        usr = request.user
        myStudent = usr.getMyStudents()  # Get students list
        student_id = kwargs.get('sid', None)
        selectedstd = Student.objects.get(pk=student_id)
        firstClass = selectedstd.class_id
        studentlist = firstClass.getClassStudentList()
        context = {'user': usr, 'myStudent': myStudent, 'firstClass': firstClass, 'studentlist': studentlist }
        return render(request, 'studentlist/studentlist.html', context)
