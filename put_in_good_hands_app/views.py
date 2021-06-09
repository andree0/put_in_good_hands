from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User
from django.core.paginator import Paginator
from django.core.serializers import serialize
from django.db.models import Sum
from django.shortcuts import redirect, render
from django.urls import reverse_lazy
from django.views.generic import CreateView, TemplateView, View
from formtools.wizard.views import SessionWizardView

from put_in_good_hands_app.forms import (
    RegisterForm,
    DonationForm1,
    DonationForm2,
    DonationForm3,
    DonationForm4,
)
from put_in_good_hands_app.models import Category, Donation, Institution


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

#
# class AddDonationView(SessionWizardView):
#     template_name = "form.html"
#     form_list = [DonationForm1, DonationForm2, DonationForm3, DonationForm4]
#
#     # def get_context_data(self, **kwargs):
#     #     return {'category_list': Category.objects.all()}
#
#     def done(self, form_list, **kwargs):
#         do_something_with_the_form_data(form_list)
#         return render(self.request, 'form-confirmation.html', {
#             'form_data': [form.cleaned_data for form in form_list],
#         })


class AddDonationView(View):
    template_name = "form.html"
    context = {}

    def get(self, request, *args, **kwargs):
        self.context['category_list'] = Category.objects.all()
        self.context['institution_list'] = Institution.objects.all()
        self.context['categories'] = serialize(
            'json', Category.objects.all())
        self.context['institutions'] = serialize(
            'json',
            list(Institution.objects.all()), fields=['name', 'categories'])
        return render(request, self.template_name, self.context)

    def post(self, request, *args, **kwargs):
        data = {
            'quantity': request.POST.get("bags"),
            'categories': request.POST.get("categories"),
            'institution': request.POST.get("organization"),
            'address': request.POST.get("address"),
            'phone_number': request.POST.get("phone"),
            'city': request.POST.get("city"),
            'zip_code': request.POST.get("postcode"),
            'pick_up_date': request.POST.get("data"),
            'pick_up_time': request.POST.get("time"),
            'pick_up_comment': request.POST.get("more_info"),
            'user': request.user,
        }
        return render(request, 'form-confirmation.html')


class CustomLoginView(View):
    template_name = "login.html"
    context = {}

    def get(self, request, *args, **kwargs):
        return render(request, self.template_name)

    def post(self, request, *args, **kwargs):
        username = request.POST.get('email')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is None and User.objects.filter(username=username):
            self.context['message'] = "Nieprawidłowe hasło !"
            return render(request, self.template_name, self.context)
        elif user is not None:
            login(request, user)
            return redirect(reverse_lazy('landing_page'))
        else:
            return redirect(reverse_lazy('register'))


class RegisterView(CreateView):
    model = User
    template_name = "register.html"
    success_url = reverse_lazy('login')
    form_class = RegisterForm

# strongPassword100%


class ProfileView(TemplateView):
    template_name = "profile_details.html"