from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("search", views.search, name="search"),
    path("new", views.new, name="new"),
    path("random", views.random, name="random"),
    path("<str:title>", views.title, name="title"),     #variable name in <> determines the variable parameter link to views.py
    path("edit/<str:title>", views.edit, name="edit")
]
