from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

from put_in_good_hands_app.validators import validate_password


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


class UserSettingsForm(forms.ModelForm):

    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'email',)