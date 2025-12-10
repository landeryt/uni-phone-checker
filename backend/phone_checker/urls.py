from django.urls import path
from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("phone/count", views.count, name="count"),

    # API route
    path("phone/validate", views.validate, name="validate"),
    path("registration", views.index, name="registration")
]
