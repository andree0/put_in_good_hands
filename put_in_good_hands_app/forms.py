import datetime

from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

from put_in_good_hands_app.models import Category, Donation, Institution
from put_in_good_hands_app.validators import (
    validate_address,
    validate_pick_up_date,
    validate_zip_code,
    validate_password,
)


class RegisterForm(UserCreationForm):
    email = forms.EmailField(widget=forms.EmailInput(attrs={
        'placeholder': "Email"}), required=True)
    password1 = forms.CharField(widget=forms.PasswordInput(attrs={
        'placeholder': 'Hasło'}), validators=[validate_password, ])
    password2 = forms.CharField(widget=forms.PasswordInput(attrs={
        'placeholder': 'Potwierdź hasło'}))

    class Meta:
        model = User
        fields = (
            'first_name',
            'last_name',
            'email',
            'password1',
            'password2',
        )
        widgets = {
            'first_name': forms.TextInput(attrs={'placeholder': 'Imię'}),
            'last_name': forms.TextInput(attrs={'placeholder': 'Nazwisko'}),
        }

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email):
            self.add_error(
                'email',
                "Konto o podanym emailu już istnieje !"
            )
        return email

    def save(self, commit=True):
        user = super().save(commit=False)
        user.username = self.cleaned_data['email']
        user.first_name = self.cleaned_data['first_name']
        user.last_name = self.cleaned_data['last_name']
        user.email = self.cleaned_data['email']
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()
        return user


# class DonationForm1(forms.ModelForm):

#     class Meta:
#         model = Donation
#         fields = ('categories', )
#         widgets = {
#             'categories': forms.CheckboxSelectMultiple
#         }


# class DonationForm2(forms.ModelForm):

#     class Meta:
#         model = Donation
#         fields = ('quantity', )
#         widgets = {
#             'quantity': forms.NumberInput(attrs={
#                 'min': 1
#             })
#         }


# class DonationForm3(forms.ModelForm):

#     class Meta:
#         model = Donation
#         fields = ('institution', )
#         widgets = {
#             'institution': forms.RadioSelect
#         }


# class DonationForm4(forms.ModelForm):

#     class Meta:
#         model = Donation
#         fields = ('address', 'city', 'zip_code', 'phone_number',
#                   'pick_up_date', 'pick_up_time', 'pick_up_comment', )
#         widgets = {
#             'address': forms.TextInput(attrs={
#                 'maxlength': 128
#             }),
#             'city': forms.TextInput(attrs={
#                 'maxlength': 64
#             }),
#             'zip_code': forms.NumberInput(attrs={
#                 'pattern': "[0-9]{2}-[0-9]{3}"
#             }),
#             'phone_number': forms.NumberInput(attrs={
#                 'type': 'tel',
#                 'pattern': "[0-9]{3}[0-9]{3}[0-9]{3}"
#             }),
#             'pick_up_date': forms.SelectDateWidget,
#             'pick_up_time': forms.TimeInput,
#             'pick_up_comment': forms.Textarea(attrs={
#                  'maxlength': 255
#             })
#         }
