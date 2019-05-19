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
from information.models import User, Student, Class, TimeTable, Check_in

class CheckinView(LoginRequiredMixin, TemplateView):
    template_name = "checkin/checkin.html"

    def get(self, request, *args, **kwargs):
        usr = request.user
        myStudent = usr.getMyStudents() #Get students list 
        firststd = myStudent[0] 
        checkInList = firststd.getCheckIn()
        context = {'user': usr, 'myStudent': myStudent, 'checkInList': checkInList}
        return render(request, 'checkin/checkin.html', context)


class PrivateCheckinView(LoginRequiredMixin, TemplateView):
    template_name = "checkin/checkin.html"

    def get(self, request, *args, **kwargs): 
        usr = request.user
        myStudent = usr.getMyStudents()  # Get students list
        student_id = request.body.sid 
        selectedstd = Student.objects.get(pk=student_id)
        checkInList = selectedstd.getCheckIn()
        context = {'user': usr, 'myStudent': myStudent, 'checkInList': checkInList,'selectedstd': selectedstd }
        return render(request, 'checkin/checkin.html', context)
