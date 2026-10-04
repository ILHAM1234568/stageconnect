from django.contrib.auth.models import User
from rest_framework import serializers

from .models import Company, StageOffer, Student


class CompanySerializer(serializers.ModelSerializer):

    class Meta:
        model = Company
        fields = [
            "id",
            "name",
            "description",
            "location",
        ]


class StageOfferSerializer(serializers.ModelSerializer):

    company = CompanySerializer(read_only=True)

    class Meta:
        model = StageOffer
        fields = [
            "id",
            "title",
            "company",
            "description",
            "location",
            "field",
            "duration",
            "created_at",
        ]


class StudentRegisterSerializer(serializers.Serializer):

    username = serializers.CharField(max_length=150)
    password = serializers.CharField(
        write_only=True,
        min_length=6
    )
    name = serializers.CharField(max_length=100)
    email = serializers.EmailField()
    school = serializers.CharField(max_length=150)
    field = serializers.CharField(max_length=100)

    def validate_username(self, value):

        if User.objects.filter(username=value).exists():
            raise serializers.ValidationError(
                "Username already exists."
            )

        return value

    def validate_email(self, value):

        if Student.objects.filter(email=value).exists():
            raise serializers.ValidationError(
                "Email already exists."
            )

        return value

    def create(self, validated_data):

        user = User.objects.create_user(
            username=validated_data["username"],
            password=validated_data["password"]
        )

        student = Student.objects.create(
            user=user,
            name=validated_data["name"],
            email=validated_data["email"],
            school=validated_data["school"],
            field=validated_data["field"]
        )

        return student


class CompanyRegisterSerializer(serializers.Serializer):

    username = serializers.CharField(max_length=150)
    password = serializers.CharField(
        write_only=True,
        min_length=6
    )
    name = serializers.CharField(max_length=150)
    email = serializers.EmailField()
    description = serializers.CharField(
        required=False,
        allow_blank=True
    )
    location = serializers.CharField(max_length=150)

    def validate_username(self, value):

        if User.objects.filter(username=value).exists():
            raise serializers.ValidationError(
                "Username already exists."
            )

        return value

    def validate_email(self, value):

        if Company.objects.filter(email=value).exists():
            raise serializers.ValidationError(
                "Email already exists."
            )

        return value


    def create(self, validated_data):

        user = User.objects.create_user(
            username=validated_data["username"],
            password=validated_data["password"]
        )

        company = Company.objects.create(
            user=user,
            name=validated_data["name"],
            email=validated_data["email"],
            description=validated_data.get(
                "description",
                ""
            ),
            location=validated_data["location"]
        )

        return company


class StudentProfileSerializer(serializers.ModelSerializer):

    username = serializers.CharField(
        source="user.username",
        read_only=True
    )

    class Meta:
        model = Student
        fields = [
            "id",
            "username",
            "name",
            "email",
            "school",
            "field",
            "cv",
        ]
        read_only_fields = [
            "id",
            "username",
        ]