from django.contrib import admin
from django.urls import path
from accounts.views import (
    login_user,
    home_view,
    register_user,
    create_user_profile,
    change_password
    )
from main.views import merchant_view, staff_view


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', home_view, name='home'),
    path('login/', login_user, name='login'),
    path('register/', register_user, name='register'),
    path('profile/', create_user_profile, name='create-profile'),
    path('staff/', staff_view, name='staff-view'),
    path('merchant/<int:id>', merchant_view, name='merchant-view'),
    path(
        'change-password/',
        change_password,
        name='change-password'
        )
]
