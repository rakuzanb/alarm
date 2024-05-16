from django.urls import path, include
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    path('', views.LandingPageView.as_view(), name='landing'),
    path('home/', views.HomePageView.as_view(), name='home'),
    path('signup/', views.signup, name='signup'),
    path('profile/', views.ProfileUpdate.as_view(), name='profile'),
    path('alarm/create/', views.AlarmCreate.as_view(), name='alarm_create'),
    path('alarm/<int:pk>/update/', views.AlarmUpdate.as_view(), name='alarm_update'),
    path('alarm/<int:pk>/delete/', views.AlarmDelete.as_view(), name='alarm_delete'),
    path('login/', auth_views.LoginView.as_view(template_name='login.html'), name='login'),
    path('alarms/alarms', views.AlarmsView.as_view(), name='alarms_list'),
    
]
