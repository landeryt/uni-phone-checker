from django.urls import path
from . import views

urlpatterns = [
    path("phone/count", views.count, name="count"),
    path("phone/validate", views.validate, name="validate"),
    path("registration", views.registration, name="registration"),
    path("users", views.users, name="users")
]
