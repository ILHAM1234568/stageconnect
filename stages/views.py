from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib import messages

from .models import (
    Student,
    Company,
    StageOffer,
    Application,
    Notification,
)


# =========================================================
# HOME
# =========================================================

def home(request):

    search = request.GET.get(
        "search",
        ""
    ).strip()

    offers = StageOffer.objects.all().order_by(
        "-created_at"
    )

    if search:

        offers = offers.filter(
            title__icontains=search
        ) | offers.filter(
            field__icontains=search
        ) | offers.filter(
            location__icontains=search
        ) | offers.filter(
            description__icontains=search
        ) | offers.filter(
            company__name__icontains=search
        )

    unread_notifications = 0

    if request.user.is_authenticated:

        unread_notifications = Notification.objects.filter(
            user=request.user,
            is_read=False
        ).count()

    return render(
        request,
        "stages/home.html",
        {
            "offers": offers,
            "search": search,
            "unread_notifications": unread_notifications,
        }
    )


# =========================================================
# STAGE DETAIL
# =========================================================

def stage_detail(request, offer_id):

    offer = get_object_or_404(
        StageOffer,
        id=offer_id
    )

    student = None
    already_applied = False

    if request.user.is_authenticated:

        try:

            student = Student.objects.get(
                user=request.user
            )

            already_applied = Application.objects.filter(
                student=student,
                stage_offer=offer
            ).exists()

        except Student.DoesNotExist:
            pass

    return render(
        request,
        "stages/stage_detail.html",
        {
            "offer": offer,
            "student": student,
            "already_applied": already_applied,
        }
    )


# =========================================================
# APPLY TO STAGE
# =========================================================

@login_required(login_url="login_student")
def apply_stage(request, offer_id):

    offer = get_object_or_404(
        StageOffer,
        id=offer_id
    )

    try:

        student = Student.objects.get(
            user=request.user
        )

    except Student.DoesNotExist:

        messages.error(
            request,
            "Vous devez avoir un profil étudiant."
        )

        return redirect(
            "profile"
        )

    if request.method == "POST":

        message = request.POST.get(
            "message",
            ""
        ).strip()

        existing_application = Application.objects.filter(
            student=student,
            stage_offer=offer
        ).first()

        if existing_application:

            messages.warning(
                request,
                "Vous avez déjà candidaté à cette offre."
            )

            return redirect(
                "stage_detail",
                offer_id=offer.id
            )

        application = Application.objects.create(
            student=student,
            stage_offer=offer,
            message=message,
            status="pending"
        )

        if offer.company.user:

            Notification.objects.create(
                user=offer.company.user,
                message=(
                    f"Nouvelle candidature de "
                    f"{student.name} pour "
                    f"{offer.title}."
                )
            )

        messages.success(
            request,
            "Votre candidature a été envoyée avec succès."
        )

        return redirect(
            "my_applications"
        )

    return redirect(
        "stage_detail",
        offer_id=offer.id
    )


# =========================================================
# MY APPLICATIONS
# =========================================================

@login_required(login_url="login_student")
def my_applications(request):

    try:

        student = Student.objects.get(
            user=request.user
        )

    except Student.DoesNotExist:

        messages.error(
            request,
            "Profil étudiant introuvable."
        )

        return redirect(
            "profile"
        )

    applications = Application.objects.filter(
        student=student
    ).select_related(
        "stage_offer",
        "stage_offer__company"
    ).order_by(
        "-created_at"
    )

    unread_notifications = Notification.objects.filter(
        user=request.user,
        is_read=False
    ).count()

    return render(
        request,
        "stages/my_applications.html",
        {
            "student": student,
            "applications": applications,
            "unread_notifications": unread_notifications,
        }
    )


# =========================================================
# REGISTER STUDENT
# =========================================================

def register_student(request):

    if request.user.is_authenticated:

        return redirect(
            "student_dashboard"
        )

    if request.method == "POST":

        username = request.POST.get(
            "username",
            ""
        ).strip()

        password = request.POST.get(
            "password",
            ""
        )

        name = request.POST.get(
            "name",
            ""
        ).strip()

        email = request.POST.get(
            "email",
            ""
        ).strip()

        school = request.POST.get(
            "school",
            ""
        ).strip()

        field = request.POST.get(
            "field",
            ""
        ).strip()

        if not username or not password:

            messages.error(
                request,
                "Le nom d'utilisateur et le mot de passe sont obligatoires."
            )

            return redirect(
                "register_student"
            )

        if User.objects.filter(
            username=username
        ).exists():

            messages.error(
                request,
                "Ce nom d'utilisateur existe déjà."
            )

            return redirect(
                "register_student"
            )

        if Student.objects.filter(
            email=email
        ).exists():

            messages.error(
                request,
                "Cet email est déjà utilisé."
            )

            return redirect(
                "register_student"
            )

        user = User.objects.create_user(
            username=username,
            password=password
        )

        Student.objects.create(
            user=user,
            name=name,
            email=email,
            school=school,
            field=field
        )

        login(
            request,
            user
        )

        messages.success(
            request,
            "Votre compte étudiant a été créé avec succès."
        )

        return redirect(
            "student_dashboard"
        )

    return render(
        request,
        "stages/register.html"
    )


# =========================================================
# REGISTER COMPANY
# =========================================================

def register_company(request):

    if request.user.is_authenticated:

        return redirect(
            "company_dashboard"
        )

    if request.method == "POST":

        username = request.POST.get(
            "username",
            ""
        ).strip()

        password = request.POST.get(
            "password",
            ""
        )

        name = request.POST.get(
            "name",
            ""
        ).strip()

        email = request.POST.get(
            "email",
            ""
        ).strip()

        description = request.POST.get(
            "description",
            ""
        ).strip()

        location = request.POST.get(
            "location",
            ""
        ).strip()

        if not username or not password:

            messages.error(
                request,
                "Le nom d'utilisateur et le mot de passe sont obligatoires."
            )

            return redirect(
                "register_company"
            )

        if User.objects.filter(
            username=username
        ).exists():

            messages.error(
                request,
                "Ce nom d'utilisateur existe déjà."
            )

            return redirect(
                "register_company"
            )

        if Company.objects.filter(
            email=email
        ).exists():

            messages.error(
                request,
                "Cet email est déjà utilisé."
            )

            return redirect(
                "register_company"
            )

        user = User.objects.create_user(
            username=username,
            password=password
        )

        Company.objects.create(
            user=user,
            name=name,
            email=email,
            description=description,
            location=location
        )

        login(
            request,
            user
        )

        messages.success(
            request,
            "Votre compte entreprise a été créé avec succès."
        )

        return redirect(
            "company_dashboard"
        )

    return render(
        request,
        "stages/register_company.html"
    )


# =========================================================
# LOGIN
# =========================================================

def login_student(request):

    if request.user.is_authenticated:

        try:

            Student.objects.get(
                user=request.user
            )

            return redirect(
                "student_dashboard"
            )

        except Student.DoesNotExist:

            try:

                Company.objects.get(
                    user=request.user
                )

                return redirect(
                    "company_dashboard"
                )

            except Company.DoesNotExist:
                pass

    if request.method == "POST":

        username = request.POST.get(
            "username",
            ""
        ).strip()

        password = request.POST.get(
            "password",
            ""
        )

        user = authenticate(
            request,
            username=username,
            password=password
        )

        if user is not None:

            login(
                request,
                user
            )

            try:

                Student.objects.get(
                    user=user
                )

                return redirect(
                    "student_dashboard"
                )

            except Student.DoesNotExist:
                pass

            try:

                Company.objects.get(
                    user=user
                )

                return redirect(
                    "company_dashboard"
                )

            except Company.DoesNotExist:
                pass

            return redirect(
                "home"
            )

        messages.error(
            request,
            "Nom d'utilisateur ou mot de passe incorrect."
        )

    return render(
        request,
        "stages/login.html"
    )


# =========================================================
# LOGOUT
# =========================================================

@login_required
def logout_student(request):

    logout(
        request
    )

    messages.success(
        request,
        "Vous êtes déconnecté."
    )

    return redirect(
        "home"
    )


# =========================================================
# STUDENT PROFILE
# =========================================================

@login_required(login_url="login_student")
def profile(request):

    try:

        student = Student.objects.get(
            user=request.user
        )

    except Student.DoesNotExist:

        if Company.objects.filter(
            user=request.user
        ).exists():

            return redirect(
                "company_dashboard"
            )

        messages.error(
            request,
            "Profil étudiant introuvable."
        )

        return redirect(
            "home"
        )

    if request.method == "POST":

        name = request.POST.get(
            "name",
            ""
        ).strip()

        email = request.POST.get(
            "email",
            ""
        ).strip()

        school = request.POST.get(
            "school",
            ""
        ).strip()

        field = request.POST.get(
            "field",
            ""
        ).strip()

        if not name or not email or not school or not field:

            messages.error(
                request,
                "Veuillez remplir tous les champs obligatoires."
            )

            return redirect(
                "profile"
            )

        email_exists = Student.objects.filter(
            email=email
        ).exclude(
            id=student.id
        ).exists()

        if email_exists:

            messages.error(
                request,
                "Cet email est déjà utilisé par un autre étudiant."
            )

            return redirect(
                "profile"
            )

        student.name = name
        student.email = email
        student.school = school
        student.field = field

        cv_file = request.FILES.get(
            "cv"
        )

        if cv_file:

            allowed_extensions = [
                ".pdf",
                ".doc",
                ".docx",
            ]

            file_name = cv_file.name.lower()

            valid_extension = any(
                file_name.endswith(extension)
                for extension in allowed_extensions
            )

            if not valid_extension:

                messages.error(
                    request,
                    "Format CV non autorisé. Utilisez PDF, DOC ou DOCX."
                )

                return redirect(
                    "profile"
                )

            max_size = 5 * 1024 * 1024

            if cv_file.size > max_size:

                messages.error(
                    request,
                    "Le CV ne doit pas dépasser 5 MB."
                )

                return redirect(
                    "profile"
                )

            student.cv = cv_file

        student.save()

        messages.success(
            request,
            "Votre profil a été mis à jour avec succès."
        )

        return redirect(
            "profile"
        )

    edit_mode = request.GET.get(
        "edit"
    ) == "1"

    unread_notifications = Notification.objects.filter(
        user=request.user,
        is_read=False
    ).count()

    return render(
        request,
        "stages/profile.html",
        {
            "student": student,
            "unread_notifications": unread_notifications,
            "edit_mode": edit_mode,
        }
    )


# =========================================================
# STUDENT DASHBOARD
# =========================================================

@login_required(login_url="login_student")
def student_dashboard(request):

    try:

        student = Student.objects.get(
            user=request.user
        )

    except Student.DoesNotExist:

        try:

            Company.objects.get(
                user=request.user
            )

            return redirect(
                "company_dashboard"
            )

        except Company.DoesNotExist:

            messages.error(
                request,
                "Profil étudiant introuvable."
            )

            return redirect(
                "home"
            )

    applications = Application.objects.filter(
        student=student
    ).select_related(
        "stage_offer",
        "stage_offer__company"
    ).order_by(
        "-created_at"
    )

    total_applications = applications.count()

    accepted_applications = applications.filter(
        status="accepted"
    ).count()

    pending_applications = applications.filter(
        status="pending"
    ).count()

    rejected_applications = applications.filter(
        status="rejected"
    ).count()

    recent_applications = applications[:5]

    unread_notifications = Notification.objects.filter(
        user=request.user,
        is_read=False
    ).count()

    return render(
        request,
        "stages/student_dashboard.html",
        {
            "student": student,
            "applications": applications,
            "recent_applications": recent_applications,
            "total_applications": total_applications,
            "accepted_applications": accepted_applications,
            "pending_applications": pending_applications,
            "rejected_applications": rejected_applications,
            "unread_notifications": unread_notifications,
        }
    )


# =========================================================
# COMPANY DASHBOARD
# =========================================================

@login_required(login_url="login_student")
def company_dashboard(request):

    try:

        company = Company.objects.get(
            user=request.user
        )

    except Company.DoesNotExist:

        messages.error(
            request,
            "Compte entreprise introuvable."
        )

        return redirect(
            "student_dashboard"
        )

    offers = StageOffer.objects.filter(
        company=company
    ).order_by(
        "-created_at"
    )

    applications = Application.objects.filter(
        stage_offer__company=company
    ).select_related(
        "student",
        "stage_offer"
    ).order_by(
        "-created_at"
    )

    total_offers = offers.count()

    total_applications = applications.count()

    pending_applications = applications.filter(
        status="pending"
    ).count()

    accepted_applications = applications.filter(
        status="accepted"
    ).count()

    rejected_applications = applications.filter(
        status="rejected"
    ).count()

    unread_notifications = Notification.objects.filter(
        user=request.user,
        is_read=False
    ).count()

    return render(
        request,
        "stages/company_dashboard.html",
        {
            "company": company,
            "offers": offers,
            "applications": applications,
            "total_offers": total_offers,
            "total_applications": total_applications,
            "pending_applications": pending_applications,
            "accepted_applications": accepted_applications,
            "rejected_applications": rejected_applications,
            "pending_count": pending_applications,
            "accepted_count": accepted_applications,
            "rejected_count": rejected_applications,
            "unread_notifications": unread_notifications,
        }
    )


# =========================================================
# ADD OFFER
# =========================================================

@login_required(login_url="login_student")
def add_offer(request):

    try:

        company = Company.objects.get(
            user=request.user
        )

    except Company.DoesNotExist:

        messages.error(
            request,
            "Compte entreprise introuvable."
        )

        return redirect(
            "student_dashboard"
        )

    if request.method == "POST":

        title = request.POST.get(
            "title",
            ""
        ).strip()

        description = request.POST.get(
            "description",
            ""
        ).strip()

        location = request.POST.get(
            "location",
            ""
        ).strip()

        field = request.POST.get(
            "field",
            ""
        ).strip()

        duration = request.POST.get(
            "duration",
            ""
        ).strip()

        if not title or not description or not location or not field or not duration:

            messages.error(
                request,
                "Veuillez remplir tous les champs."
            )

            return redirect(
                "add_offer"
            )

        StageOffer.objects.create(
            title=title,
            company=company,
            description=description,
            location=location,
            field=field,
            duration=duration
        )

        messages.success(
            request,
            "L'offre a été créée avec succès."
        )

        return redirect(
            "company_dashboard"
        )

    return render(
        request,
        "stages/add_offer.html",
        {
            "company": company
        }
    )


# =========================================================
# COMPANY APPLICATIONS
# =========================================================

@login_required(login_url="login_student")
def company_applications(request):

    try:

        company = Company.objects.get(
            user=request.user
        )

    except Company.DoesNotExist:

        messages.error(
            request,
            "Profil entreprise introuvable."
        )

        return redirect(
            "home"
        )

    applications = Application.objects.filter(
        stage_offer__company=company
    ).select_related(
        "student",
        "stage_offer"
    ).order_by(
        "-created_at"
    )

    pending_count = applications.filter(
        status="pending"
    ).count()

    accepted_count = applications.filter(
        status="accepted"
    ).count()

    rejected_count = applications.filter(
        status="rejected"
    ).count()

    unread_notifications = Notification.objects.filter(
        user=request.user,
        is_read=False
    ).count()

    return render(
        request,
        "stages/company_applications.html",
        {
            "company": company,
            "applications": applications,
            "pending_count": pending_count,
            "accepted_count": accepted_count,
            "rejected_count": rejected_count,
            "unread_notifications": unread_notifications,
        }
    )


# =========================================================
# OFFER APPLICATIONS
# =========================================================

@login_required(login_url="login_student")
def offer_applications(request, offer_id):

    company = get_object_or_404(
        Company,
        user=request.user
    )

    offer = get_object_or_404(
        StageOffer,
        id=offer_id,
        company=company
    )

    applications = Application.objects.filter(
        stage_offer=offer
    ).select_related(
        "student",
        "stage_offer"
    ).order_by(
        "-created_at"
    )

    status_filter = request.GET.get(
        "status",
        "all"
    )

    if status_filter in [
        "pending",
        "accepted",
        "rejected"
    ]:

        applications = applications.filter(
            status=status_filter
        )

    total_count = Application.objects.filter(
        stage_offer=offer
    ).count()

    pending_count = Application.objects.filter(
        stage_offer=offer,
        status="pending"
    ).count()

    accepted_count = Application.objects.filter(
        stage_offer=offer,
        status="accepted"
    ).count()

    rejected_count = Application.objects.filter(
        stage_offer=offer,
        status="rejected"
    ).count()

    unread_notifications = Notification.objects.filter(
        user=request.user,
        is_read=False
    ).count()

    context = {
        "offer": offer,
        "applications": applications,
        "status_filter": status_filter,
        "total_count": total_count,
        "pending_count": pending_count,
        "accepted_count": accepted_count,
        "rejected_count": rejected_count,
        "unread_notifications": unread_notifications,
    }

    return render(
        request,
        "stages/offer_applications.html",
        context
    )


# =========================================================
# UPDATE APPLICATION STATUS
# =========================================================

@login_required(login_url="login_student")
def update_application_status(
    request,
    application_id
):

    try:

        company = Company.objects.get(
            user=request.user
        )

    except Company.DoesNotExist:

        messages.error(
            request,
            "Compte entreprise introuvable."
        )

        return redirect(
            "student_dashboard"
        )

    application = get_object_or_404(
        Application,
        id=application_id,
        stage_offer__company=company
    )

    if request.method == "POST":

        status = request.POST.get(
            "status"
        )

        allowed_statuses = [
            "pending",
            "accepted",
            "rejected",
        ]

        if status not in allowed_statuses:

            messages.error(
                request,
                "Statut invalide."
            )

            return redirect(
                "company_applications"
            )

        application.status = status

        application.save()

        if status == "accepted":

            message = (
                f"Votre candidature pour "
                f"{application.stage_offer.title} "
                f"a été acceptée."
            )

        elif status == "rejected":

            message = (
                f"Votre candidature pour "
                f"{application.stage_offer.title} "
                f"a été refusée."
            )

        else:

            message = (
                f"Le statut de votre candidature pour "
                f"{application.stage_offer.title} "
                f"a été mis à jour."
            )

        if application.student.user:

            Notification.objects.create(
                user=application.student.user,
                message=message
            )

        messages.success(
            request,
            "Le statut de la candidature a été mis à jour."
        )

    return redirect(
        "company_applications"
    )


# =========================================================
# NOTIFICATIONS
# =========================================================

@login_required(login_url="login_student")
def notifications(request):

    user_notifications = Notification.objects.filter(
        user=request.user
    ).order_by(
        "-created_at"
    )

    unread_notifications = user_notifications.filter(
        is_read=False
    ).count()

    return render(
        request,
        "stages/notifications.html",
        {
            "notifications": user_notifications,
            "unread_notifications": unread_notifications,
        }
    )


# =========================================================
# MARK NOTIFICATIONS AS READ
# =========================================================

@login_required(login_url="login_student")
def mark_notifications_read(request):

    Notification.objects.filter(
        user=request.user,
        is_read=False
    ).update(
        is_read=True
    )

    return redirect(
        "notifications"
    )


# =========================================================
# EDIT OFFER
# =========================================================

@login_required(login_url="login_student")
def edit_offer(
    request,
    offer_id
):

    try:

        company = Company.objects.get(
            user=request.user
        )

    except Company.DoesNotExist:

        messages.error(
            request,
            "Compte entreprise introuvable."
        )

        return redirect(
            "student_dashboard"
        )

    offer = get_object_or_404(
        StageOffer,
        id=offer_id,
        company=company
    )

    if request.method == "POST":

        offer.title = request.POST.get(
            "title",
            ""
        ).strip()

        offer.description = request.POST.get(
            "description",
            ""
        ).strip()

        offer.location = request.POST.get(
            "location",
            ""
        ).strip()

        offer.field = request.POST.get(
            "field",
            ""
        ).strip()

        offer.duration = request.POST.get(
            "duration",
            ""
        ).strip()

        offer.save()

        messages.success(
            request,
            "L'offre a été modifiée avec succès."
        )

        return redirect(
            "company_dashboard"
        )

    return render(
        request,
        "stages/edit_offer.html",
        {
            "offer": offer,
            "company": company,
        }
    )


# =========================================================
# DELETE OFFER
# =========================================================

@login_required(login_url="login_student")
def delete_offer(
    request,
    offer_id
):

    try:

        company = Company.objects.get(
            user=request.user
        )

    except Company.DoesNotExist:

        messages.error(
            request,
            "Compte entreprise introuvable."
        )

        return redirect(
            "student_dashboard"
        )

    offer = get_object_or_404(
        StageOffer,
        id=offer_id,
        company=company
    )

    if request.method == "POST":

        offer.delete()

        messages.success(
            request,
            "L'offre a été supprimée avec succès."
        )

    return redirect(
        "company_dashboard"
    )


# =========================================================
# COMPANY PROFILE
# =========================================================

@login_required(login_url="login_student")
def company_profile(request):

    try:

        company = Company.objects.get(
            user=request.user
        )

    except Company.DoesNotExist:

        messages.error(
            request,
            "Profil entreprise introuvable."
        )

        return redirect(
            "home"
        )

    if request.method == "POST":

        name = request.POST.get(
            "name",
            ""
        ).strip()

        email = request.POST.get(
            "email",
            ""
        ).strip()

        location = request.POST.get(
            "location",
            ""
        ).strip()

        description = request.POST.get(
            "description",
            ""
        ).strip()

        if not name or not email or not location:

            messages.error(
                request,
                "Veuillez remplir tous les champs obligatoires."
            )

            return redirect(
                "company_profile"
            )

        email_exists = Company.objects.filter(
            email=email
        ).exclude(
            id=company.id
        ).exists()

        if email_exists:

            messages.error(
                request,
                "Cet email est déjà utilisé par une autre entreprise."
            )

            return redirect(
                "company_profile"
            )

        company.name = name
        company.email = email
        company.location = location
        company.description = description

        company.save()

        messages.success(
            request,
            "Le profil de votre entreprise a été mis à jour avec succès."
        )

        return redirect(
            "company_profile"
        )

    edit_mode = request.GET.get(
        "edit"
    ) == "1"

    unread_notifications = Notification.objects.filter(
        user=request.user,
        is_read=False
    ).count()

    return render(
        request,
        "stages/company_profile.html",
        {
            "company": company,
            "edit_mode": edit_mode,
            "unread_notifications": unread_notifications,
        }
    )