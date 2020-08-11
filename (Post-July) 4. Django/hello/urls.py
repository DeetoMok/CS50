from django.urls import path

# from current directory, import views python file
from . import views

# List of all allowable urls that can be accessed by hello app
urlpatterns = [
    path("", views.index1, name="index"),
    # variable of name is created and then passed to views.greet1\
    path("<str:name>", views.greet1, name="greet"),
    path("brian", views.brian, name="brian"),
    path("david", views.david, name="david"),
]
