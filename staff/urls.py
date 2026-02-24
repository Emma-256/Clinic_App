from django.urls import path
from . import views

app_name = "staff"

urlpatterns = [
    path("register/", views.register_staff, name="register_staff"),
]

