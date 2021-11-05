from django.urls import path
from . import views

urlpatterns = [
    path('login_user', views.login_user, name="login"),
    path('logout_user', views.logout_user, name='logout'),

    path('register_user', views.register_user, name='register-user'),

    path('user_list',views.user_list, name='user-list'),
    path('user_info/<user_id>', views.user_info, name='user-info'),

]