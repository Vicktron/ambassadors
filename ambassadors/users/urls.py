from django.contrib import admin
from django.urls import path, include
from .views import main_view, signup_view, dashboard

app_name = "users"

urlpatterns = [
    path('', main_view, name='main-view'),
    path('signup/', signup_view, name='signup'),
    path('dashboard/', dashboard, name='recommendations'),
    path('<str:ref_code>/', main_view, name='main-view'),
]
