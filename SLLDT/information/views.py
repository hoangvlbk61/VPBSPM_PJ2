from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse, Http404, HttpResponseRedirect
from django.template import loader
from django.views.generic import (
    CreateView, DetailView, ListView, UpdateView, DeleteView, View, TemplateView)
from django.urls import reverse
from .models import User, Class, Student, Subject, Teacher, Check_in, TimeTable, Absence, MarkSheet, Notification
from .forms import LoginForm, EditProfileForm, ChangePasswordForm 
from django.contrib.auth.mixins import LoginRequiredMixin, AccessMixin
from django.contrib.auth import logout, authenticate, login, hashers
from datetime import datetime, date
import datetime
import re


class LoginView(TemplateView):
    template_name = "information/login.html"

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return HttpResponseRedirect('/')
        return super(LoginView, self).dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):

        form = LoginForm(request.POST, request=request)
        if form.is_valid():
            user = authenticate(username=request.POST.get(
                'username'), password=request.POST.get('password'))
            if user is not None:
                if user.is_active:
                    login(request, user)
                    if user.is_superuser:
                        return HttpResponseRedirect((reverse('information:index')))
                    else:
                        return HttpResponseRedirect((reverse('information:employee')))
                else:
                    return render(request, 'information/login.html', {
                        "error": True,
                        "message": "<b>Your Account is InActive. Please Contact Administrator</b>"
                    })
            else:
                return render(request, 'information/login.html', {
                    "error": True,
                    "message": "Your Account is not Found. Please Contact Administrator"
                })
        else:
            return render(request, 'information/login.html', {
                "error": True,
                "message": "Tên đăng nhập và mật khẩu không chính xác. Vui lòng thử lại !"
            })


class IndexView(LoginRequiredMixin, TemplateView):
    template_name = "information/index.html"

    def get(self, request, *args, **kwargs):
        usr = request.user
        if not usr.is_superuser:
            return HttpResponseRedirect((reverse('information:employee')))

        # numberofemployee = Employee.objects.all().count()
        # numberofdevice = Device.objects.all().count()
        # today = date.today()
        # numberofabsence_future = Absence.objects.filter(
        #     start_time__gte=today).count()
        # numberoflogtime_today = Logtime.objects.filter(
        #     start_time__contains=today).count()
        numberofemployee= 10 
        numberofdevice= 10 
        numberofabsence_future = 10 
        numberoflogtime_today= 10 
        context = {'user': usr, 'numberofemployee': numberofemployee,
                   'numberofdevice': numberofdevice,
                                'numberofabsence_future': numberofabsence_future,
                                'numberoflogtime_today': numberoflogtime_today}
        return render(request, 'information/index.html', context)


class ForgotPasswordView(TemplateView):
    template_name = "information/forgot_password.html"


class ChangePasswordView(TemplateView):
    template_name = "information/change_password.html"

    def get(self, request, *args, **kwargs):
        usr = request.user
        context = {'user': usr}
        return render(request, 'information/change_password.html', context)

    def post(self, request, *args, **kwargs):
        form = ChangePasswordForm(request.POST)
        usr = request.user
        if form.is_valid():
            old_password = request.POST['old_password']
            new_password = request.POST['new_password']
            new_password_2 = request.POST['new_password_2']
            if usr.check_password(old_password):
                if new_password == new_password_2:
                    if (not re.search(r'^\w+$', new_password)) or len(new_password) < 6 or len(new_password) > 20:
                        return render(request, 'information/change_password.html', {
                            "error": True,
                            "message": "Mật khẩu không được chứa kí tự đặc biệt và phải từ 6-20 ký tự!"
                        })
                    else:
                        if old_password == new_password:
                            return render(request, 'information/change_password.html', {
                                "error": True,
                                "message": "Xin chọn mật khẩu khác mật khẩu cũ của bạn !"
                            })
                        else:
                            usr.set_password(new_password)
                            usr.save()
                            login(request, usr)
                            return render(request, 'information/change_password.html', {
                                "error": True,
                                "message": "Đổi mật khẩu thành công !"
                            })
                else:
                    return render(request, 'information/change_password.html', {
                        "error": True,
                        "message": "Mật khẩu mới không khớp !"
                    })
            else:
                return render(request, 'information/change_password.html', {
                    "error": True,
                    "message": "Mật khẩu cũ không chính xác !"
                })
        else:
            return render(request, 'information/change_password.html', {
                "error": True,
                "message": "Lỗi đã xảy ra ! Hãy thử lại."
            })


class LogoutView(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        logout(request)
        request.session.flush()
        return redirect("information:login")


# class EmployeeView(LoginRequiredMixin, TemplateView):
#     template_name = "common/employee.html"

#     def get_queryset(self):
#         queryset = Employee.objects.all().order_by("id")
#         return queryset

#     def get_context_data(self, **kwargs):
#         context = super(EmployeeView, self).get_context_data(**kwargs)
#         context["employees"] = self.get_queryset()
#         context["per_page"] = 3
#         return context


# class EmployeeDetailView(LoginRequiredMixin, TemplateView):
#     template_name = "employeedetail.html"

#     def get(self, request, *args, **kwargs):
#         usr = request.user
#         eid = self.kwargs['employee_id']
#         epl = Employee.objects.get(id=eid)
#         next_abs = Absence.objects.filter(employee=epl).filter(
#             start_time__gte=date.today()).order_by('start_time').first()
#         if next_abs:
#             list_absences = next_abs.list_next_rest_day
#         else:
#             list_absences = []
#         list_logtime = Logtime.objects.filter(
#             employee=epl).order_by('start_time')
#         list_explanations = Explanation.objects.filter(
#             employee=epl).order_by('create_on')
#         context = {'list_absences': list_absences, 'list_logtime': list_logtime,
#                    'list_explanations': list_explanations, 'user': usr, 'employee': epl}
#         return render(request, 'common/employeedetail.html', context)


# class ContactsView(LoginRequiredMixin, TemplateView):
#     template_name = "contacts.html"

#     def get(self, request, *args, **kwargs):
#         usr = request.user
#         eid = self.kwargs['employee_id']
#         epl = Employee.objects.get(id=eid)
#         list_contacts = Contact.objects.filter(employee=epl)
#         context = {'list_contacts': list_contacts,
#                    'user': usr, 'employee': epl}
#         return render(request, 'common/contacts.html', context)


class ProfileView(LoginRequiredMixin, TemplateView):
    template_name = "profile.html"

    def get(self, request, *args, **kwargs):
        usr = request.user
        context = {'user': usr}
        return render(request, 'information/profile.html', context)


class EditProfileView(LoginRequiredMixin , UpdateView):
    template_name = "information/editprofile.html"
    form_class = EditProfileForm

    def dispatch(self, request, *args, **kwargs):
        self.user = User.objects.filter(is_active=True).order_by('pk')
        return super(EditProfileView, self).dispatch(request, *args, **kwargs)

    def get_form_kwargs(self):
        kwargs = super(EditProfileView, self).get_form_kwargs()
        return kwargs

    def get(self, request, *args, **kwargs):
        usr = request.user
        form = EditProfileForm(user=usr)
        context = {'user': usr, 'form': form}
        # context = { 'user':usr }
        return render(request, 'information/editprofile.html', context)

    def post(self, request, *args, **kwargs):
        usr = request.user
        form = EditProfileForm( usr, request.POST)
        new_fname = request.POST['first_name']
        new_lname = request.POST['last_name']
        new_email = request.POST['email']
        usr.first_name = new_fname
        usr.last_name = new_lname
        usr.email = new_email
        usr.save()
        context = {'user': usr, 'form': form}
        # context = { 'user':usr }
        return render(request, 'information/editprofile.html', context)

# USER LIST VIEW

class UserListView(LoginRequiredMixin, TemplateView):
    template_name = "userlist.html"

    def get(self, request, *args, **kwargs):
        usr = request.user
        context = {'user': usr}
        if not usr.is_superuser:
            message = "Bạn không được cấp quyền xem danh sách user !"
            context += message
            return render(request, 'information/userlist.html', context)
        else:
            user_list = User.objects.all()
            context = {'user': usr, 'user_list': user_list}
            return render(request, 'information/userlist.html', context)


