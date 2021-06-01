from django.contrib.auth.models import User
from django import forms

from put_in_good_hands_app.validators import validate_password


class RegisterForm(forms.ModelForm):
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={'placeholder': 'Hasło'}),
        validators=[validate_password, ]
    )
    password2 = forms.CharField(widget=forms.PasswordInput(
        attrs={'placeholder': 'Powtórz hasło'}
    ))

    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'email', 'password', )
        widgets = {
            'first_name': forms.TextInput(attrs={'placeholder': 'Imię'}),
            'last_name': forms.TextInput(attrs={'placeholder': 'Nazwisko'}),
            'email': forms.EmailInput(attrs={'placeholder': 'Email'}),
        }

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if get_user_model().objects.filter(email=email):
            self.add_error(
                'email',
                "User with the given email already exists !"
            )
        return email

    def clean_password2(self):
        password2 = self.cleaned_data.get('password2')
        password = self.cleaned_data.get('password')
        if password:
            if password2 != password:
                self.add_error(
                    'password2',
                    "Passwords do not match !"
                )
        return password2

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password"])
        if commit:
            user.save()
        return user
