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
    path('employees/form', employee_form, name='employee_form'),
    path('trainings/', trainings_list, name='trainings_list'),
    path('trainings/<int:training_id>/', training_details, name='training'),
    path('trainings/<int:training_id>/edit', training_edit_form, name='training_edit_form'),
    path('trainings/past', trainings_list_past, name='trainings_list_past'),
    path('trainings/form', training_form, name='training_form'),
    path('departments/', department_list, name='department_list'),
    path('department/form', department_form, name='department_form'),
    path('department/<int:department_id>/', department_details, name='department_details'),
]
