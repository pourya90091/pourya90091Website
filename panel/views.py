from django.shortcuts import render
from django.contrib.auth import get_user_model
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from django.http import Http404, HttpRequest
from django.views import View
from panel.forms import getProfileForm
from utils.authorize import check_user_logged_in


User = get_user_model()


class PanelView(View):
    @check_user_logged_in
    def get(self, req: HttpRequest):
        return render(req, "panel/dashboard.html", {})


class ProfileView(APIView):
    @check_user_logged_in
    def get(self, req: HttpRequest):
        return render(req, "panel/profile.html", {
            "profile_form": getProfileForm(req.user.username, req.user.email),
            "user": req.user
        })

    @check_user_logged_in
    def post(self, req: HttpRequest):
        pass
