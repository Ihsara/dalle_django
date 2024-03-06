from os import environ

import requests
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.shortcuts import HttpResponse
from django.shortcuts import render
from django.urls import reverse
from django.utils.translation import gettext_lazy as _
from django.views.generic import CreateView
from django.views.generic import DetailView
from django.views.generic import RedirectView
from django.views.generic import UpdateView

from dalle_django.users.models import DalleParams
from dalle_django.users.models import User

from .forms import DalleParam


class UserDetailView(LoginRequiredMixin, DetailView):
    model = User
    slug_field = "username"
    slug_url_kwarg = "username"


user_detail_view = UserDetailView.as_view()


class UserUpdateView(LoginRequiredMixin, SuccessMessageMixin, UpdateView):
    model = User
    fields = ["name"]
    success_message = _("Information successfully updated")

    def get_success_url(self):
        # for mypy to know that the user is authenticated
        assert self.request.user.is_authenticated
        return self.request.user.get_absolute_url()

    def get_object(self):
        return self.request.user


user_update_view = UserUpdateView.as_view()


class UserRedirectView(LoginRequiredMixin, RedirectView):
    permanent = False

    def get_redirect_url(self):
        return reverse("users:detail", kwargs={"username": self.request.user.username})


user_redirect_view = UserRedirectView.as_view()


class DalleParamsCreateView(CreateView):
    model = DalleParams
    fields = ["test", "one", "two"]


dalle_param_create_view = DalleParamsCreateView.as_view()


class DalleParamsUpdateView(UpdateView):
    model = DalleParams
    fields = ["test", "one", "two"]

    def post(self, request, *args, **kwargs):
        # if this is a POST request we need to process the form data
        if request.method == "POST":
            form = DalleParam(request.POST)
            if form.is_valid():
                trees_amount = form.cleaned_data["trees_amount"]
                hangar_size = form.cleaned_data["hangar_size"]

                auth_token = environ.get("OPENAITOKEN")
                headers = {
                    "Authorization": f"Bearer {auth_token}",
                    "Content-Type": "application/json",
                }

                data = {
                    "model": "dall-e-3",
                    "prompt": f"{hangar_size} cute baby sea otter in around {trees_amount} trees",
                    "n": 1,
                    "size": "1024x1024",
                }

                url = "https://api.openai.com/v1/images/generations"

                response = requests.post(url, json=data, headers=headers)
                pic_url = response.json()["data"][0]["url"]

                return HttpResponse(
                    f"trees_amount: {trees_amount}\n\nhangar_size: {hangar_size} response: {pic_url}"
                )
        else:
            form = DalleParam()
        return render(request, "home.html", {"form": form})


dalle_param_update_view = DalleParamsUpdateView.as_view()
