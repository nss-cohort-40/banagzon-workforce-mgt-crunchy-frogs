from django.urls import path
from django.conf.urls import include
from hrapp import views
from .views import *

app_name = 'hrapp'
urlpatterns = [
    path('', home, name='home'),
    path('accounts/', include('django.contrib.auth.urls')),
    path('logout/', logout_user, name='logout'),
    path('employees/', employee_list, name='employee_list'),
    path('trainings/', trainings_list, name='trainings_list'),
    path('trainings/form', trainings_list, name='trainings_list'),
    path('departments/', department_list, name='department_list'),
    path('departments/form', department_form, name='department_form'),
]
