from django.shortcuts import render
from django.views.generic import CreateView, TemplateView


class LandingPageView(TemplateView):
    pass


class AddDonationView(CreateView):
    pass


class LoginView(TemplateView):
    pass


class RegisterView(TemplateView):
    pass
