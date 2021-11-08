from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name="home"),
    path('home', views.home, name="home"),
    path('shifts', views.shifts, name="shifts"),
    path('all_shifts', views.shifts, name="all-shifts"),
    path('add_shift', views.add_shift, name="add-shift"),
    path('verified_shifts', views.verified_shifts, name="verified-shifts"),

    path('shifts_csv', views.shifts_csv, name='shift-csv'),

    path('update_shift/<shift_id>', views.update_shift, name='update-shift'),
    path('delete_shift/<shift_id>', views.delete_shift, name='delete-shift'),
    path('verify_shift/<shift_id>', views.verify_shift, name='verify-shift'),
    path('pay_shift/<shift_id>', views.pay_shift, name='pay-shift'),

    path('salary/<user_id>', views.salary, name='salary'),
    path('pay_salary/<user_id>', views.pay_salary, name='pay-salary'),
    path('user_salary_list', views.user_salary_list, name='user-salary-list'),


]