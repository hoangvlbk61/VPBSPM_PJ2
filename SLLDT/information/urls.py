from django.urls import path
from information import views
from django.views.generic import (
    CreateView, DetailView, ListView, UpdateView, DeleteView, TemplateView)
from information.views import (LoginView, IndexView, ForgotPasswordView, LogoutView,   ProfileView,
                          EditProfileView, ChangePasswordView,
                          UserListView)
app_name = 'information' 

urlpatterns = [
    
    path('login', LoginView.as_view(), name='login'),
    path('logout', LogoutView.as_view(), name='logout'),
    path('', IndexView.as_view(), name='index'),
    path('forgot_password', ForgotPasswordView.as_view(), name='forgot_password'),

    path('change_password', ChangePasswordView.as_view(), name='change_password'),
    path('profile', ProfileView.as_view(), name='profile'),
    path('editprofile', EditProfileView.as_view(), name='editprofile'),

    #USER BAR
    path('userlist', UserListView.as_view(), name='userlist'),

]


