import datetime

from django.contrib.auth import authenticate, login
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User
from django.contrib.messages import add_message, ERROR, get_messages
from django.core.paginator import Paginator
from django.core.serializers import serialize
from django.db.models import Sum
from django.http import Http404
from django.shortcuts import get_object_or_404, redirect, render, reverse
from django.urls import reverse_lazy
from django.views.generic import CreateView, TemplateView, View
# from formtools.wizard.views import SessionWizardView

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


# Alternatywna droga do formularzy kilku krokowych

# class AddDonationView(SessionWizardView):
#     template_name = "form.html"
#     form_list = [DonationForm1, DonationForm2, DonationForm3, DonationForm4]
#
#     def done(self, form_list, **kwargs):
#         do_something_with_the_form_data(form_list)
#         return render(self.request, 'form-confirmation.html', {
#             'form_data': [form.cleaned_data for form in form_list],
#         })


class AddDonationView(LoginRequiredMixin, View):
    template_name = "form.html"
    context = {}

    def get(self, request, *args, **kwargs):
        self.context['category_list'] = Category.objects.all()
        self.context['institution_list'] = Institution.objects.all()
        self.context['categories'] = serialize(
            'json', Category.objects.all())
        self.context['institutions'] = serialize(
            'json',
            Institution.objects.all(), fields=['name', 'categories'])
        return render(request, self.template_name, self.context)

    def post(self, request, *args, **kwargs):
        data = {
            'quantity': request.POST.get("bags"),
            'institution': request.POST.get("organization"),
            'address': request.POST.get("address"),
            'phone_number': request.POST.get("phone"),
            'city': request.POST.get("city"),
            'zip_code': request.POST.get("postcode"),
            'pick_up_date': request.POST.get("data"),
            'pick_up_time': request.POST.get("time"),
            'user': request.user,
        }
        categories = request.POST.getlist("categories")

        if "" in [val for key, val in data.items()]:
            add_message(
                request, ERROR,
                "Uzupełnij wymagane pola. Uwagi dla kuriera nie są wymagane.")
            return redirect(reverse('add-donation'))

        data['pick_up_comment'] = request.POST.get("more_info")

        if len(data['phone_number']) != 9:
            add_message(
                request, ERROR,
                "Pole z numerem telefonu wymaga podania 9 cyfr.")

        try:
            data['quantity'] = int(data['quantity'])
            categories = [int(i) for i in categories]
            data['institution'] = int(data['institution'])
            data['phone_number'] = int(data['phone_number'])
        except ValueError:
            add_message(request, ERROR,
                        "Błędy w formularzu. Wypełnij jeszcze raz.")

        if len(data['zip_code']) == 6 and data['zip_code'][2] == '-':
            zipcode_numbers_str = data['zip_code'].split("-")
            try:
                _ = [int(i) for i in zipcode_numbers_str]
            except ValueError:
                add_message(request, ERROR, "Zły format kodu pocztowego.")
        else:
            add_message(request, ERROR, "Zły format kodu pocztowego.")

        if data['address'].isalpha():
            add_message(request, ERROR, "Podaj numer budynku w polu adresu.")

        if len(data['address']) > 128:
            add_message(request, ERROR,
                        "Adres jest za długi (max. 128 znaków).")

        if len(data['city']) > 64:
            add_message(request, ERROR,
                        "Za długa nazwa miasta (max. 64 znaki).")

        if len(data['pick_up_date']) == 10 and data['pick_up_date'
        ][4] == '-' and data['pick_up_date'][7] == '-':
            el_data_str = data['pick_up_date'].split("-")
            try:
                el_data_int = [int(i) for i in el_data_str]
                data['pick_up_date'] = datetime.date(*el_data_int)
            except (ValueError, TypeError,):
                add_message(request, ERROR, "Zły format daty.")
        else:
            add_message(request, ERROR, "Zły format daty.")

        if data['pick_up_date'] <= datetime.date.today():
            add_message(request, ERROR, "Proszę wybrać inną datę.")

        if len(data['pick_up_time']) == 5 and data['pick_up_time'][2] == ':':
            el_time_str = data['pick_up_time'].split(":")
            try:
                el_time_int = [int(i) for i in el_time_str]
                data['pick_up_time'] = datetime.time(*el_time_int, second=0)
            except (ValueError, TypeError,):
                add_message(request, ERROR, "Zły format godziny.")
        else:
            add_message(request, ERROR, "Zły format godziny.")

        try:
            data['institution'] = get_object_or_404(Institution,
                                                    pk=data['institution'])
        except (Http404, ValueError, ):
            add_message(request, ERROR, "Nie wybrałeś instytucji.")

        if data['pick_up_comment'] == "":
            data['pick_up_comment'] = "Brak uwag."

        storage = get_messages(request)
        if len(storage):
            return redirect(reverse('add-donation'))

        new_donation = Donation.objects.create(**data)
        new_donation.categories.set(categories)
        return redirect(reverse('confirm'))


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


class ProfileView(LoginRequiredMixin, TemplateView):
    template_name = "profile_details.html"


class ConfirmDonationView(TemplateView):
    template_name = "form-confirmation.html"
