from django.urls import path
from panel import views

urlpatterns = [
    path("dashboard/", views.DashboardView.as_view(), name="dashboard"),
    path("edit-profile/", views.EditProfileView.as_view(), name="edit-profile"),
]
