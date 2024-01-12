from django.urls import path
from accounts import views

urlpatterns = [
    path("signup", views.SignUpView.as_view(), name="signup"),
    path("login", views.LoginView.as_view(), name="login"),
    path("logout", views.LogoutView.as_view(), name="logout"),
    path("verification", views.EmailVerificationView.as_view(), name="email_verification"),
    path("activate/<str:activate_code>", views.ActivateView.as_view(), name="activate_account"),
]
