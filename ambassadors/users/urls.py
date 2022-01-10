from django.urls import path
from . import views

app_name = "users"

urlpatterns = [
    path('', views.main_view, name='main-view'),
    path('sign-up/', views.signup_view, name='signup'),
    path('sign-in/', views.login_page, name="sign-in"),
    path('logout/', views.logout, name='logout'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('<str:ref_code>/', views.main_view, name='main-view'),
]
