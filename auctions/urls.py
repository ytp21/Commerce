from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("watchlist", views.watchlist, name="watchlist"),
    path("my_listing", views.my_listing, name="my_listing"),
    path("closed_listing", views.closed_listing, name="closed_listing"),
    path("listing/<int:pk>", views.listing, name="listing"),
    path("listing/<int:pk>/bid", views.bid, name="bid"),
    path("listing/<int:pk>/comment", views.comment, name="comment"),
    path("listing/<int:pk>/status", views.status, name="status"),
    path("category/<str:cat>", views.category, name="category"),
    path("create_listing", views.create_listing, name="create_listing"),
    path("watchlist_button/<str:view>/<int:pk>", views.watchlist_button, name="watchlist_button"),
]

