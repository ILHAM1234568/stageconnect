
from django.contrib import admin

from .models import Student, Company, StageOffer, Application


class StudentAdmin(admin.ModelAdmin):
    pass


class CompanyAdmin(admin.ModelAdmin):
    list_display = (
        "name",
        "email",
        "location",
        "is_verified",
    )

    list_filter = (
        "is_verified",
    )

    search_fields = (
        "name",
        "email",
    )


class StageOfferAdmin(admin.ModelAdmin):
    pass


class ApplicationAdmin(admin.ModelAdmin):
    list_display = (
        "student",
        "stage_offer",
        "status",
        "created_at",
    )

    list_filter = (
        "status",
    )

    search_fields = (
        "student__name",
        "stage_offer__title",
    )


admin.site.register(Student, StudentAdmin)
admin.site.register(Company, CompanyAdmin)
admin.site.register(StageOffer, StageOfferAdmin)
admin.site.register(Application, ApplicationAdmin)

