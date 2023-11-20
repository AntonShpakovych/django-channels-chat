from django.urls import path
from django.contrib.auth.views import LoginView, LogoutView

from user.views import SignUpUserView


urlpatterns = [
    path(
        "login/",
        LoginView.as_view(
            template_name="user/registration/login.html"
        ),
        name="login"
    ),
    path(
        "logout/",
        LogoutView.as_view(),
        name="logout"
    ),
    path(
        "signup/",
        SignUpUserView.as_view(),
        name="signup"
    )
]

app_name = "user"
