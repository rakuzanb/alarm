from django.shortcuts import render
from django.views.generic import TemplateView,ListView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from django import forms
from alarms_project.models import Alarm
from django.contrib.auth.models import User
from alarms_project.forms import AlarmForm, SignUpForm, ProfileForm
from django.contrib.auth import login, authenticate
from django.contrib.auth.models import Group
from django.shortcuts import render, redirect
from django.contrib.auth.mixins import LoginRequiredMixin
from rules.contrib.views import PermissionRequiredMixin

#
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib.auth.forms import AuthenticationForm
from django.views.generic import ListView
from .models import Alarm  # Ensure you have an Alarm model

class AlarmsView(ListView):
    model = Alarm
    template_name = 'alarms/alarms_list.html'  # Ensure you have this template
    context_object_name = 'alarms'
def custom_login(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                # Redirect to a success page.
                return redirect('/alarms/alarms')
            else:
                # Return an 'invalid login' error message.
                form.add_error(None, 'Username or password is not correct')
    else:
        form = AuthenticationForm()
    return render(request, 'registration/login.html', {'form': form})

#
# Create your views here.
def signup(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            my_group = Group.objects.get(name='AlarmGroup') 
            my_group.user_set.add(user)
            login(request, user)
            return redirect('/alarms/alarms')
    else:
        form = SignUpForm()
    return render(request, 'registration/signup.html', {'form': form})

class LandingPageView(TemplateView):
    template_name = 'landing.html'

class HomePageView(LoginRequiredMixin,ListView):
    login_url = '/account/login'
    redirect_field_name = 'redirect_to'
    model = Alarm
    context_object_name = 'alarm_list'
    paginate_by = 6
    template_name = 'home.html'

    def get_queryset(self):
        return Alarm.objects.filter(creator = self.request.user)

class AlarmCreate(LoginRequiredMixin,CreateView):
    login_url = '/account/login'
    redirect_field_name = 'redirect_to'
    model = Alarm
    form_class = AlarmForm
    success_url = '/alarms/alarms'
    def get_context_data(self, **kwargs):
        ctx = super(AlarmCreate, self).get_context_data(**kwargs)
        ctx['title'] = 'Add new alarm'
        return ctx
    def form_valid(self, form):
        form.instance.creator = self.request.user
        return super(AlarmCreate, self).form_valid(form)

class AlarmUpdate(LoginRequiredMixin,PermissionRequiredMixin,UpdateView):
    login_url = '/account/login'
    redirect_field_name = 'redirect_to'
    model = Alarm
    permission_required = 'alarm.edit_alarm'
    form_class = AlarmForm
    success_url = '/alarms/alarms'
    def get_context_data(self, **kwargs):
        ctx = super(AlarmUpdate, self).get_context_data(**kwargs)
        ctx['title'] = 'Update alarm'
        return ctx
    def form_valid(self, form):
        form.instance.creator = self.request.user
        return super(AlarmUpdate, self).form_valid(form)

class AlarmDelete(LoginRequiredMixin,PermissionRequiredMixin,DeleteView):
    login_url = '/account/login'
    redirect_field_name = 'redirect_to'
    model = Alarm
    permission_required = 'alarm.edit_alarm'
    success_url = '/alarms/alarms'
    def get(self, *args, **kwargs):
        return self.post(*args, **kwargs)

class ProfileUpdate(LoginRequiredMixin,UpdateView):
    login_url = '/account/login'
    redirect_field_name = 'redirect_to'
    model = User
    form_class = ProfileForm
    success_url = '/alarms/alarms'
    def get_context_data(self, **kwargs):
        ctx = super(ProfileUpdate, self).get_context_data(**kwargs)
        ctx['title'] = 'Update Profile'
        return ctx
    def get_object(self):
        return self.request.user