from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("inactive", views.inactive, name="inactive"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("create", views.create, name="create"),
    path("watching", views.watching, name="watching"),
    path("<str:title>/close_listing", views.close_listing, name="close_listing"),
    path("<str:title>/bid", views.bid, name="bid"),
    path("<str:title>/watch", views.watch, name="watch"),
    path("<str:title>/unwatch", views.unwatch, name="unwatch"),
    path("<int:list_id>", views.listing, name="listing"),
    path("<str:title>/comment", views.comment, name="comment")
]
