from django.urls import path

from .views import index

app_name = "dalle"
urlpatterns = [
    path("", view=index, name="index"),
]
