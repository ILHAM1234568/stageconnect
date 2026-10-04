from django.urls import path
from . import views


urlpatterns = [

    path(
        "",
        views.home,
        name="home"
    ),

    path(
        "stage/<int:offer_id>/",
        views.stage_detail,
        name="stage_detail"
    ),

    path(
        "stage/<int:offer_id>/apply/",
        views.apply_stage,
        name="apply_stage"
    ),

    path(
        "login/",
        views.login_student,
        name="login_student"
    ),

    path(
        "register/",
        views.register_student,
        name="register_student"
    ),

    path(
        "register-company/",
        views.register_company,
        name="register_company"
    ),

    path(
        "logout/",
        views.logout_student,
        name="logout_student"
    ),

    path(
        "dashboard/",
        views.student_dashboard,
        name="student_dashboard"
    ),

    path(
        "profil/",
        views.profile,
        name="profile"
    ),

    path(
        "mes-candidatures/",
        views.my_applications,
        name="my_applications"
    ),

    path(
        "company-dashboard/",
        views.company_dashboard,
        name="company_dashboard"
    ),

    path(
        "add-offer/",
        views.add_offer,
        name="add_offer"
    ),

    path(
        "company-applications/",
        views.company_applications,
        name="company_applications"
    ),

    path(
        "offer/<int:offer_id>/applications/",
        views.offer_applications,
        name="offer_applications"
    ),

    path(
        "application/<int:application_id>/status/",
        views.update_application_status,
        name="update_application_status"
    ),

    path(
        "offer/<int:offer_id>/edit/",
        views.edit_offer,
        name="edit_offer"
    ),

    path(
        "offer/<int:offer_id>/delete/",
        views.delete_offer,
        name="delete_offer"
    ),

    path(
        "notifications/",
        views.notifications,
        name="notifications"
    ),

    path(
        "notifications/read/",
        views.mark_notifications_read,
        name="mark_notifications_read"
    ),

    path(
        "company-profile/",
        views.company_profile,
        name="company_profile"
    ),
]