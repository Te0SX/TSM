from django.urls import path
from . import views

# urls that created through the Django member application for the user
urlpatterns = [
    path('login_user', views.login_user, name="login"),
    path('login_user/<username>', views.login_user_again, name="login-again"),
    path('logout_user', views.logout_user, name='logout'),

    path('register_user', views.register_user, name='register-user'),
    path('user_profile/<user_id>', views.user_profile, name='user-profile'),
    path('user_password/<user_id>', views.user_password, name='user-password'),

    path('user_list',views.user_list, name='user-list'),
    path('user_info/<user_id>', views.user_info, name='user-info'),
    path('user_role/<user_id>', views.user_role, name='user-role'),

]