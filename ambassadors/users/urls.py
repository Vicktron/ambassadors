from django.contrib import admin
from django.urls import path, include
from .views import (
    login_page, main_view, signup_view, dashboard
)

app_name = "users"

urlpatterns = [
    path('', main_view, name='main-view'),
    path('sign-up/', signup_view, name='signup'),
    path('sign-in/', login_page, name="sign-in"),
    path('dashboard/', dashboard, name='dashboard'),
    path('<str:ref_code>/', main_view, name='main-view'),
]
