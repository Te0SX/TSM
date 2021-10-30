from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name="home"),
    path('home', views.home, name="home"),
    path('shifts', views.shifts, name="shifts"),
    path('add_shift', views.add_shift, name="add-shift"),

]