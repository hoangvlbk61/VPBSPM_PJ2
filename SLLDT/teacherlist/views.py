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
from information.models import User, Student, Class, TimeTable, Teacher

class TeacherListView(LoginRequiredMixin, TemplateView):
    template_name = "teacherlist/teacherlist.html"

    def get(self, request, *args, **kwargs):
        usr = request.user
        myStudent = usr.getMyStudents() #Get students list 
        firststd = myStudent[0] 
        firstClass = firststd.class_id 
        teacherlist = firstClass.getTeacherList()
        context = {'user': usr, 'myStudent': myStudent, 'teacherlist': teacherlist}
        return render(request, 'teacherlist/teacherlist.html', context)


class PrivateTeacherListView(LoginRequiredMixin, TemplateView):
    template_name = "teacherlist/teacherlist.html"

    def get(self, request, *args, **kwargs): 
        usr = request.user
        myStudent = usr.getMyStudents()  # Get students list
        student_id = kwargs.get('sid', None)
        selectedstd = Student.objects.get(pk=student_id)
        firstClass = selectedstd.class_id
        teacherlist = firstClass.getTeacherList()
        context = {'user': usr, 'myStudent': myStudent, 'firstClass': firstClass, 'teacherlist': teacherlist, 'selectedstd': selectedstd }
        return render(request, 'teacherlist/teacherlist.html', context)
