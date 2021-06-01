from django.contrib.auth.models import User
from django.core.paginator import Paginator
from django.db.models import Sum
from django.shortcuts import redirect, render
from django.urls import reverse_lazy
from django.views.generic import CreateView, TemplateView

from put_in_good_hands_app.forms import RegisterForm
from put_in_good_hands_app.models import Donation, Institution


class LandingPageView(TemplateView):
    template_name = "index.html"

    def get_context_data(self, **kwargs):
        per_page = 5
        obj_list_1 = Institution.objects.filter(type=0).order_by('name')
        obj_list_2 = Institution.objects.filter(type=1).order_by('name')
        obj_list_3 = Institution.objects.filter(type=2).order_by('name')
        page = self.request.GET.get('page')
        paginator_foundations = Paginator(obj_list_1, per_page)
        paginator_organizations = Paginator(obj_list_2, per_page)
        paginator_collection = Paginator(obj_list_3, per_page)
        foundations = paginator_foundations.get_page(page)
        organizations = paginator_organizations.get_page(page)
        local_collection = paginator_collection.get_page(page)
        return {
            'counter_bags': Donation.objects.aggregate(
                sum_bag=Sum('quantity'))[
                'sum_bag'] if Donation.objects.all() else 0,
            'counter_organization': Donation.objects.values(
                'institution').count(),
            'foundations': foundations,
            'non_governmental_organizations': organizations,
            'local_collection': local_collection,
        }


class AddDonationView(TemplateView):
    template_name = "form.html"


class LoginView(TemplateView):
    template_name = "login.html"


class RegisterView(CreateView):
    model = User
    template_name = "register.html"
    success_url = reverse_lazy('login')
    form_class = RegisterForm

# strongPassword100%
