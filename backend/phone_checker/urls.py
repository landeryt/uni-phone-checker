from django.urls import path
from . import views

urlpatterns = [
    path("phone/count", views.count, name="count"),

    # API route
    path("phone/validate", views.validate, name="validate"),
    path("registration", views.index, name="registration"),
    path("users", views.users, name="users")
]
