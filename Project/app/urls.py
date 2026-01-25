from django.urls import path
from .views import signup_view, login_view, logout_view,home_view

urlpatterns = [
    # Home
    path("", home_view, name="home"),

    # Authentication
    path("login/", login_view, name="login"),
    path("signup/", signup_view, name="signup"),
    path("logout/", logout_view, name="logout"),

]