from django.urls import path
from hello import views

urlpatterns = [
    path("", views.home, name="home"),
    path("getDrones", views.getNewDrones, name="newDrones"),
    path("getDronesFromDB", views.getDronesFromDB, name="oldDrones"),
]