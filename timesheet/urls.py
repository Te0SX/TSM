from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name="home"),
    path('home', views.home, name="home"),
    path('about', views.about, name="about"),
    path('support', views.support, name="support"),

    path('shifts', views.shifts, name="shifts"),
    path('all_shifts', views.shifts, name="all-shifts"),
    path('add_shift', views.add_shift, name="add-shift"),

    path('shifts_csv', views.shifts_csv, name='shift-csv'),
    path('salaries_csv', views.salaries_csv, name='salaries-csv'),

    path('update_shift/<shift_id>', views.update_shift, name='update-shift'),
    path('delete_shift/<shift_id>', views.delete_shift, name='delete-shift'),
    path('verify_shift/<shift_id>', views.verify_shift, name='verify-shift'),
    path('pay_shift/<shift_id>', views.pay_shift, name='pay-shift'),

    path('salary/<user_id>', views.salary, name='salary'),
    path('pay_salary/<user_id>', views.pay_salary, name='pay-salary'),
    path('user_salary_list', views.user_salary_list, name='user-salary-list'),

    path('shifts/<user_id>', views.shifts_of, name='shifts-of'),
    path('user_timesheets_list', views.user_timesheets_list, name='user-timesheets-list'),

    path('send_message/<user_id>/<shift_id>', views.send_message, name='send-message'),
    path('read_message/<message_id>', views.read_message, name='read-message'),
    path('delete_message/<message_id>', views.delete_message, name='delete-message'),
    path('resolve/<message_id>', views.resolve, name='resolve'),
    path('inbox', views.inbox, name='inbox'),

]