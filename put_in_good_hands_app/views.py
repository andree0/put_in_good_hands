from django.core.paginator import Paginator
from django.db.models import Sum
from django.shortcuts import render
from django.views.generic import CreateView, TemplateView

from put_in_good_hands_app.models import Donation, Institution


class LandingPageView(TemplateView):
    template_name = "index.html"

    def get_context_data(self, **kwargs):
        foundations = Institution.objects.filter(type=0)
        organizations = Institution.objects.filter(type=1)
        local_collection = Institution.objects.filter(type=2)
        paginator_foundations = Paginator(foundations, 5)
        paginator_organizations = Paginator(organizations, 5)
        paginator_collection = Paginator(local_collection, 5)
        return {
            'counter_bags': Donation.objects.aggregate(
                sum_bag=Sum('quantity'))[
                'sum_bag'] if Donation.objects.all() else 0,
            'counter_organization': Donation.objects.values(
                'institution').count(),
            'foundations': foundations,
            'non_governmental_organizations': organizations,
            'local_collection': local_collection,
            'paginator_foundations': paginator_foundations,
            'paginator_organizations': paginator_organizations,
            'paginator_collection': paginator_collection
        }


class AddDonationView(TemplateView):
    template_name = "form.html"


class LoginView(TemplateView):
    template_name = "login.html"


class RegisterView(TemplateView):
    template_name = "register.html"
