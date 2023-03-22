from django.contrib import admin

from put_in_good_hands_app.models import Category, Donation, Institution


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    fields = ("name",)


@admin.register(Institution)
class InstitutionAdmin(admin.ModelAdmin):
    fields = (
        "name",
        "description",
        "type",
        "categories",
    )


@admin.register(Donation)
class DonationAdmin(admin.ModelAdmin):
    fields = (
        "quantity",
        "categories",
        "institution",
        "address",
        "phone_number",
        "city",
        "zip_code",
        "pick_up_date",
        "pick_up_time",
        "pick_up_comment",
        "user",
    )
