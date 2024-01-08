from django.urls import path
from panel import views

urlpatterns = [
    path("dashboard", views.PanelView.as_view(), name="dashboard"),
    path("profile", views.ProfileView.as_view(), name="profile"),
]
