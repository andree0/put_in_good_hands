from django.db.models import Sum
from django.shortcuts import render
from django.views.generic import CreateView, TemplateView

from put_in_good_hands_app.models import Donation, Institution


class LandingPageView(TemplateView):
    template_name = "index.html"

    def get_context_data(self, **kwargs):
        return {
            'counter_bags': Donation.objects.aggregate(
                sum_bag=Sum('quantity'))[
                'sum_bag'] if Donation.objects.all() else 0,
            'counter_organization': Institution.objects.all().count()
        }


class AddDonationView(TemplateView):
    template_name = "form.html"


class LoginView(TemplateView):
    template_name = "login.html"


class RegisterView(TemplateView):
    template_name = "register.html"
