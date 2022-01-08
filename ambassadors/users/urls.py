from django.contrib import admin
from django.urls import path, include
from .views import (
    main_view, signup_view, dashboard, login
)

app_name = "users"

urlpatterns = [
    path('', main_view, name='main-view'),
    path('sign-up/', signup_view, name='signup'),
    path('sign-in/', login, name="sign-in"),
    path('dashboard/', dashboard, name='recommendations'),
    path('<str:ref_code>/', main_view, name='main-view'),
]
