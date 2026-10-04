from django.urls import path

from .api_views import (
    StageOfferListAPIView,
    LoginAPIView,
    StudentRegisterAPIView,
    CompanyRegisterAPIView,
    StudentProfileAPIView,
)


urlpatterns = [

    path(
        "offers/",
        StageOfferListAPIView.as_view(),
        name="api_offers"
    ),

    path(
        "login/",
        LoginAPIView.as_view(),
        name="api_login"
    ),

    path(
        "register/student/",
        StudentRegisterAPIView.as_view(),
        name="api_register_student"
    ),

    path(
        "register/company/",
        CompanyRegisterAPIView.as_view(),
        name="api_register_company"
    ),

    path(
        "student/profile/",
        StudentProfileAPIView.as_view(),
        name="api_student_profile"
    ),

]