from django.contrib.auth import authenticate

from rest_framework import generics, status
from rest_framework.authtoken.models import Token
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import Student, StageOffer

from .serializers import (
    StageOfferSerializer,
    StudentRegisterSerializer,
    CompanyRegisterSerializer,
    StudentProfileSerializer,
)


class StageOfferListAPIView(generics.ListAPIView):

    queryset = StageOffer.objects.all().order_by("-created_at")

    serializer_class = StageOfferSerializer


class LoginAPIView(APIView):

    def post(self, request):

        username = request.data.get("username")
        password = request.data.get("password")

        if not username or not password:
            return Response(
                {
                    "error": "Username and password are required."
                },
                status=status.HTTP_400_BAD_REQUEST
            )

        user = authenticate(
            username=username,
            password=password
        )

        if user is None:
            return Response(
                {
                    "error": "Invalid username or password."
                },
                status=status.HTTP_401_UNAUTHORIZED
            )

        token, created = Token.objects.get_or_create(
            user=user
        )

        return Response(
            {
                "token": token.key,
                "username": user.username,
            },
            status=status.HTTP_200_OK
        )


class StudentRegisterAPIView(APIView):

    def post(self, request):

        serializer = StudentRegisterSerializer(
            data=request.data
        )

        if serializer.is_valid():

            student = serializer.save()

            token, created = Token.objects.get_or_create(
                user=student.user
            )

            return Response(
                {
                    "message": "Student account created successfully.",
                    "token": token.key,
                    "username": student.user.username,
                    "student_id": student.id,
                },
                status=status.HTTP_201_CREATED
            )

        return Response(
            serializer.errors,
            status=status.HTTP_400_BAD_REQUEST
        )


class CompanyRegisterAPIView(APIView):

    def post(self, request):

        serializer = CompanyRegisterSerializer(
            data=request.data
        )

        if serializer.is_valid():

            company = serializer.save()

            token, created = Token.objects.get_or_create(
                user=company.user
            )

            return Response(
                {
                    "message": "Company account created successfully.",
                    "token": token.key,
                    "username": company.user.username,
                    "company_id": company.id,
                },
                status=status.HTTP_201_CREATED
            )

        return Response(
            serializer.errors,
            status=status.HTTP_400_BAD_REQUEST
        )


class StudentProfileAPIView(APIView):

    permission_classes = [
        IsAuthenticated
    ]

    def get(self, request):

        try:
            student = Student.objects.get(
                user=request.user
            )

        except Student.DoesNotExist:

            return Response(
                {
                    "error": "Student profile not found."
                },
                status=status.HTTP_404_NOT_FOUND
            )

        serializer = StudentProfileSerializer(
            student,
            context={
                "request": request
            }
        )

        return Response(
            serializer.data,
            status=status.HTTP_200_OK
        )