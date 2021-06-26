from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.forms import widgets

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
        fields = ('first_name', 'last_name', 'email', 'password', )
        widgets = {
            'password': forms.PasswordInput(),
        }


class CustomPasswordChangeForm(forms.Form):
    old_password = forms.CharField(
        label="Stare hasło", 
        widget=forms.PasswordInput)
    new_password1 = forms.CharField(
        label="Nowe hasło",
        widget=forms.PasswordInput,
        validators=[validate_password])
    new_password2 = forms.CharField(
        label="Powtórz nowe hasło",
        widget=forms.PasswordInput)

    def __init__(self, user, *args, **kwargs):
        self.user = user
        super().__init__(*args, **kwargs)    

    def clean_old_password(self):
        """
        Validates that the old_password field is correct.
        """
        
        old_password = self.cleaned_data["old_password"]
        if not self.user.check_password(old_password):
            self.add_error('old_password', 
            "Podane stare hasło jest niepoprawne. Proszę podać je jeszcze raz.")
        return old_password

    def clean_new_password2(self):
        password1 = self.cleaned_data.get('new_password1')
        password2 = self.cleaned_data.get('new_password2')
        if password1 and password2:
            if password1 != password2:
                self.add_error("new_password2",
                "Hasła w obu polach nie są zgodne")
        return password2

    def save(self, commit=True):
        self.user.set_password(self.cleaned_data['new_password1'])
        if commit:
            self.user.save()
        return self.user

# class CustomAuthenticatedForm(forms.Form):
#     password = forms.CharField(
#         widget=forms.PasswordInput(attrs={"placeholder": "Podaj hasło"}), 
#         label="",
#         )
    
#     def __init__(self, user, *args, **kwargs):
#         self.user = user
#         super().__init__(*args, **kwargs)    

#     def clean__password(self):        
#         password = self.cleaned_data["password"]
#         if not self.user.check_password(password):
#             self.add_error('', "Błędne hasło")
#         return password