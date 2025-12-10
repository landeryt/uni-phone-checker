from django.urls import path
from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("api/phone/count", views.count, name="count"),

    # API route
    path("api/phone/validate", views.validate, name="validate"),
    path("api/registration", views.index, name="registration")
]
