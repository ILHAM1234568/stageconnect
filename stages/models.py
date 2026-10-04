from django.db import models
from django.contrib.auth.models import User


class Student(models.Model):
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        null=True,
        blank=True
    )

    name = models.CharField(
        max_length=100
    )

    email = models.EmailField(
        unique=True
    )

    school = models.CharField(
        max_length=150
    )

    field = models.CharField(
        max_length=100
    )

    cv = models.FileField(
        upload_to="cvs/",
        blank=True,
        null=True
    )

    def __str__(self):
        return self.name


class Company(models.Model):
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        null=True,
        blank=True
    )
    name = models.CharField(max_length=150)
    email = models.EmailField(unique=True)
    description = models.TextField(blank=True)
    location = models.CharField(max_length=150)

    def __str__(self):
        return self.name


class StageOffer(models.Model):
    title = models.CharField(max_length=200)
    company = models.ForeignKey(
        Company,
        on_delete=models.CASCADE
    )
    description = models.TextField()
    location = models.CharField(max_length=150)
    field = models.CharField(max_length=100)
    duration = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title


class Application(models.Model):
    student = models.ForeignKey(
        Student,
        on_delete=models.CASCADE
    )
    stage_offer = models.ForeignKey(
        StageOffer,
        on_delete=models.CASCADE
    )
    message = models.TextField(blank=True)
    status = models.CharField(
        max_length=20,
        choices=[
            ("pending", "Pending"),
            ("accepted", "Accepted"),
            ("rejected", "Rejected"),
        ],
        default="pending"
    )
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.student} - {self.stage_offer}"


class Notification(models.Model):

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE
    )

    message = models.CharField(
        max_length=255
    )

    is_read = models.BooleanField(
        default=False
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    def __str__(self):
        return f"{self.user.username} - {self.message}"