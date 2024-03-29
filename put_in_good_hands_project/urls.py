"""put_in_good_hands_project URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.contrib.auth.views import LogoutView
from django.urls import path

from put_in_good_hands_app import views as v


urlpatterns = [
    path("admin/", admin.site.urls),
    path("", v.LandingPageView.as_view(), name="landing_page"),
    path("login/", v.CustomLoginView.as_view(), name="login"),
    path("logout/", LogoutView.as_view(), name="logout"),
    path("register/", v.RegisterView.as_view(), name="register"),
    path("add-donation/", v.AddDonationView.as_view(), name="add-donation"),
    path("profile-details/", v.ProfileView.as_view(), name="profile-details"),
    path("confirm/", v.ConfirmDonationView.as_view(), name="confirm"),
    path("my-donation/", v.MyDonationView.as_view(), name="my-donation"),
]
