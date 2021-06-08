from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

from put_in_good_hands_app.models import Category, Institution
from put_in_good_hands_app.validators import (
    validate_address,
    validate_pick_up_date,
    validate_zip_code,
)


class RegisterForm(UserCreationForm):
    email = forms.EmailField(widget=forms.EmailInput(attrs={
        'placeholder': "Email"}), required=True)
    password1 = forms.CharField(widget=forms.PasswordInput(attrs={
        'placeholder': 'Hasło'}))
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


class DonationForm1(forms.Form):
    categories = forms.ChoiceField(
        choices=[(cat.pk, cat.name) for cat in Category.objects.all()],
        widget=forms.CheckboxSelectMultiple)


class DonationForm2(forms.Form):
    quantity = forms.IntegerField(widget=forms.NumberInput(attrs={
        'min': 1
    }))


class DonationForm3(forms.Form):
    institution = forms.ChoiceField(
        choices=[(ins.pk, ins.name) for ins in Institution.objects.all()],
        widget=forms.RadioSelect
    )


class DonationForm4(forms.Form):
    address = forms.CharField(max_length=255, validators=[validate_address])
    city = forms.CharField(max_length=128)
    zip_code = forms.CharField(max_length=6, validators=[validate_zip_code])
    phone_number = forms.IntegerField(
        widget=forms.NumberInput(attrs={'min': 100000000, 'max': 999999999})
    )
    pick_up_date = forms.DateField(widget=forms.SelectDateWidget)
    pick_up_time = forms.TimeField(widget=forms.TimeInput)
    pick_up_comment = forms.CharField(max_length=255, widget=forms.Textarea)
