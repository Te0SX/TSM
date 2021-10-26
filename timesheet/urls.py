from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name="home"),
    path('home', views.home, name="home"),
    path('timesheets', views.all_timesheets, name="list-timesheets"),
]