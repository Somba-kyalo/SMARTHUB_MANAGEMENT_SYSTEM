from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required


from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.paginator import Paginator
from django.db.models import Q


from SmartHubApp.models import (
    Student,
    Unit,
    UnitRegistration,
    Result,
    Election,
    Candidate,
    Vote,
    Announcement,
    Lecturer,
    Venue,
    Timetable,
    Fee,
    LecturerEvaluation,
)



from SmartHubApp.models import (
    Student,
    Lecturer,
    Unit,
    Fee,
    Announcement,
    Election,
)
def admin_login(request):

    # If already logged in, go directly to dashboard
    if request.user.is_authenticated:
        return redirect("admin_dashboard")

    if request.method == "POST":

        username = request.POST.get("username")
        password = request.POST.get("password")

        user = authenticate(
            request,
            username=username,
            password=password
        )

        # Only allow staff/superusers into the admin panel
        if user is not None and (user.is_staff or user.is_superuser):

            login(request, user)

            return redirect("admin_dashboard")

        return render(
            request,
            "adminpanel/admin_login.html",
            {
                "error": "Invalid administrator credentials."
            }
        )

    return render(
        request,
        "adminpanel/admin_login.html"
    )


@login_required(login_url="admin_login")
def admin_dashboard(request):

    # Extra protection
    if not (request.user.is_staff or request.user.is_superuser):
        logout(request)
        return redirect("admin_login")

    context = {

        "total_students": Student.objects.count(),

        "total_lecturers": Lecturer.objects.count(),

        "total_units": Unit.objects.count(),

        "total_fees": Fee.objects.count(),

        "total_announcements": Announcement.objects.count(),

        "total_elections": Election.objects.filter(
            active=True
        ).count(),

        "announcements": Announcement.objects.order_by(
            "-created_at"
        )[:5],

    }

    return render(
        request,
        "adminpanel/admin_dashboard.html",
        context
    )


@login_required(login_url="admin_login")
def admin_logout(request):

    logout(request)

    return redirect("admin_login")



@login_required(login_url="admin_login")
def students(request):

    search = request.GET.get("search")

    students = Student.objects.all().order_by("-id")

    if search:
        students = students.filter(
            Q(first_name__icontains=search) |
            Q(last_name__icontains=search) |
            Q(admission_number__icontains=search) |
            Q(course__icontains=search)
        )

    paginator = Paginator(students, 10)

    page = request.GET.get("page")

    students = paginator.get_page(page)

    context = {

        "students": students,

        "faculties": Student.objects.values(
            "faculty"
        ).distinct().count(),

        "courses": Student.objects.values(
            "course"
        ).distinct().count(),

        "active_students": Student.objects.count(),

    }

    return render(
        request,
        "adminpanel/students.html",
        context
    )



@login_required(login_url="admin_login")
def add_student(request):

    if request.method == "POST":

        student = Student(

            first_name=request.POST["first_name"],
            middle_name=request.POST["middle_name"],
            last_name=request.POST["last_name"],

            dob=request.POST["dob"],
            gender=request.POST["gender"],

            nationality=request.POST["nationality"],
            phone_number=request.POST["phone_number"],

            address=request.POST["address"],
            county=request.POST["county"],
            postal_code=request.POST["postal_code"],

            faculty=request.POST["faculty"],
            department=request.POST["department"],
            course=request.POST["course"],

            admission_number=request.POST["admission_number"],

            year_of_study=request.POST["year_of_study"],
            study_mode=request.POST["study_mode"],

            guardian_name=request.POST["guardian_name"],
            guardian_phone=request.POST["guardian_phone"],

            personal_email=request.POST["personal_email"],

            institution_email=request.POST["institution_email"],

            username=request.POST["username"],

            password=request.POST["password"]

        )

        if "profile_photo" in request.FILES:

            student.profile_photo = request.FILES["profile_photo"]

        student.save()

        messages.success(
            request,
            "Student added successfully."
        )

        return redirect("students")

    return render(
        request,
        "adminpanel/students.html"
    )



@login_required(login_url="admin_login")
def edit_student(request, id):

    student = get_object_or_404(
        Student,
        id=id
    )

    if request.method == "POST":

        student.first_name = request.POST["first_name"]
        student.middle_name = request.POST["middle_name"]
        student.last_name = request.POST["last_name"]

        student.phone_number = request.POST["phone_number"]

        student.course = request.POST["course"]

        student.department = request.POST["department"]

        student.year_of_study = request.POST["year_of_study"]

        student.personal_email = request.POST["personal_email"]

        student.institution_email = request.POST["institution_email"]

        if "profile_photo" in request.FILES:

            student.profile_photo = request.FILES[
                "profile_photo"
            ]

        student.save()

        messages.success(
            request,
            "Student updated successfully."
        )

        return redirect("students")

    return render(
        request,
        "adminpanel/students.html",
        {
            "student": student
        }
    )


@login_required(login_url="admin_login")
def delete_student(request, id):

    student = get_object_or_404(
        Student,
        id=id
    )

    student.delete()

    messages.success(
        request,
        "Student deleted successfully."
    )

    return redirect("adminpanel/students")



@login_required(login_url="admin_login")
def announcements(request):

    announcements = Announcement.objects.all().order_by("-created_at")

    context = {
        "announcements": announcements
    }

    return render(
        request,
        "adminpanel/announcements.html",
        context
    )




@login_required(login_url="admin_login")
def add_announcement(request):

    if request.method == "POST":

        Announcement.objects.create(

            title=request.POST["title"],

            message=request.POST["message"],

            posted_by=request.POST["posted_by"],

            important="important" in request.POST

        )

        messages.success(
            request,
            "Announcement added successfully."
        )

    return redirect("adminpanel/announcements.html")


@login_required(login_url="admin_login")
def edit_announcement(request, id):

    announcement = get_object_or_404(
        Announcement,
        id=id
    )

    if request.method == "POST":

        announcement.title = request.POST["title"]

        announcement.message = request.POST["message"]

        announcement.posted_by = request.POST["posted_by"]

        announcement.important = "important" in request.POST

        announcement.save()

        messages.success(
            request,
            "Announcement updated successfully."
        )

        return redirect("adminpanel/announcements.html")

    context = {
        "announcement": announcement
    }

    return render(
        request,
        "adminpanel/announcements.html",
        context
    )



@login_required(login_url="admin_login")
def delete_announcement(request, id):

    announcement = get_object_or_404(
        Announcement,
        id=id
    )

    announcement.delete()

    messages.success(
        request,
        "Announcement deleted successfully."
    )

    return redirect("adminpanel/announcements.html")


@login_required(login_url="admin_login")
def candidates(request):

    candidates = Candidate.objects.select_related(
        "election"
    ).all().order_by("-id")

    elections = Election.objects.all()

    context = {

        "candidates": candidates,

        "elections": elections,

    }

    return render(
        request,
        "adminpanel/candidates.html",
        context
    )

@login_required(login_url="admin_login")
def add_candidate(request):

    if request.method == "POST":

        election = get_object_or_404(
            Election,
            id=request.POST["election"]
        )

        candidate = Candidate(

            election=election,

            position=request.POST["position"],

            student_name=request.POST["student_name"],

            manifesto=request.POST["manifesto"]

        )

        if "photo" in request.FILES:

            candidate.photo = request.FILES["photo"]

        candidate.save()

        messages.success(
            request,
            "Candidate added successfully."
        )

    return redirect("adminpanel/candidates.html")

@login_required(login_url="admin_login")
def edit_candidate(request, id):

    candidate = get_object_or_404(
        Candidate,
        id=id
    )

    if request.method == "POST":

        candidate.election = get_object_or_404(
            Election,
            id=request.POST["election"]
        )

        candidate.position = request.POST["position"]

        candidate.student_name = request.POST["student_name"]

        candidate.manifesto = request.POST["manifesto"]

        if "photo" in request.FILES:

            candidate.photo = request.FILES["photo"]

        candidate.save()

        messages.success(
            request,
            "Candidate updated successfully."
        )

        return redirect("adminpanel/candidates.html")

    context = {

        "candidate": candidate,

        "elections": Election.objects.all()

    }

    return render(
        request,
        "adminpanel/candidates.html",
        context
    )

@login_required(login_url="admin_login")
def delete_candidate(request, id):

    candidate = get_object_or_404(
        Candidate,
        id=id
    )

    candidate.delete()

    messages.success(
        request,
        "Candidate deleted successfully."
    )

    return redirect("adminpanel/candidates.html")


@login_required(login_url="admin_login")
def elections(request):

    elections = Election.objects.all().order_by("-id")

    context = {
        "elections": elections,
    }

    return render(
        request,
        "adminpanel/elections.html",
        context
    )


@login_required(login_url="admin_login")
def add_election(request):

    if request.method == "POST":

        Election.objects.create(
            title=request.POST["title"],
            description=request.POST["description"],
            start_date=request.POST["start_date"],
            end_date=request.POST["end_date"],
            active="active" in request.POST
        )

        messages.success(
            request,
            "Election created successfully."
        )

    return redirect("adminpanel/elections.html")

@login_required(login_url="admin_login")
def edit_election(request, id):

    election = get_object_or_404(
        Election,
        id=id
    )

    if request.method == "POST":

        election.title = request.POST["title"]
        election.description = request.POST["description"]
        election.start_date = request.POST["start_date"]
        election.end_date = request.POST["end_date"]
        election.active = "active" in request.POST

        election.save()

        messages.success(
            request,
            "Election updated successfully."
        )

        return redirect("elections")

    context = {
        "election": election,
        "elections": Election.objects.all().order_by("-id"),
    }

    return render(
        request,
        "adminpanel/elections.html",
        context
    )


@login_required(login_url="admin_login")
def delete_election(request, id):

    election = get_object_or_404(
        Election,
        id=id
    )

    election.delete()

    messages.success(
        request,
        "Election deleted successfully."
    )

    return redirect("adminpanel/elections.html")

@login_required(login_url="admin_login")
def fees(request):

    fees = Fee.objects.select_related(
        "student"
    ).all().order_by("-id")

    students = Student.objects.all().order_by(
        "first_name",
        "last_name"
    )

    context = {

        "fees": fees,

        "students": students,

    }

    return render(
        request,
        "adminpanel/fees.html",
        context
    )

@login_required(login_url="admin_login")
def add_fee(request):

    if request.method == "POST":

        student = get_object_or_404(
            Student,
            id=request.POST["student"]
        )

        total_fee = float(request.POST["total_fee"])

        amount_paid = float(request.POST["amount_paid"])

        balance = total_fee - amount_paid

        Fee.objects.create(

            student=student,

            semester=request.POST["semester"],

            total_fee=total_fee,

            amount_paid=amount_paid,

            balance=balance

        )

        messages.success(
            request,
            "Fee record added successfully."
        )

    return redirect("adminpanel/fees.html")

@login_required(login_url="admin_login")
def edit_fee(request, id):

    fee = get_object_or_404(
        Fee,
        id=id
    )

    if request.method == "POST":

        fee.student = get_object_or_404(
            Student,
            id=request.POST["student"]
        )

        fee.semester = request.POST["semester"]

        fee.total_fee = float(
            request.POST["total_fee"]
        )

        fee.amount_paid = float(
            request.POST["amount_paid"]
        )

        fee.balance = (
            fee.total_fee -
            fee.amount_paid
        )

        fee.save()

        messages.success(
            request,
            "Fee record updated successfully."
        )

        return redirect("adminpanel/fees.html")

    context = {

        "fee": fee,

        "fees": Fee.objects.all(),

        "students": Student.objects.all()

    }

    return render(
        request,
        "adminpanel/fees.html",
        context
    )


@login_required(login_url="admin_login")
def delete_fee(request, id):

    fee = get_object_or_404(
        Fee,
        id=id
    )

    fee.delete()

    messages.success(
        request,
        "Fee record deleted successfully."
    )

    return redirect("adminpanel/fees.html")

@login_required(login_url="admin_login")
def lecturer_evaluations(request):

    evaluations = Lecturer_evaluation.objects.select_related(
        "student",
        "lecturer"
    ).all().order_by("-id")

    context = {

        "evaluations": evaluations,

    }

    return render(
        request,
        "adminpanel/lecturer_evaluations.html",
        context
    )

@login_required(login_url="admin_login")
def delete_evaluation(request, id):

    evaluation = get_object_or_404(
        LecturerEvaluation,
        id=id
    )

    evaluation.delete()

    messages.success(
        request,
        "Evaluation deleted successfully."
    )

    return redirect(
        "lecturer_evaluations"
    )


@login_required(login_url="admin_login")
def results(request):

    results = Result.objects.select_related(
        "student",
        "unit"
    ).order_by("-id")

    students = Student.objects.all().order_by(
        "first_name",
        "last_name"
    )

    units = Unit.objects.all().order_by(
        "unit_code"
    )

    context = {

        "results": results,

        "students": students,

        "units": units,

    }

    return render(
        request,
        "adminpanel/results.html",
        context
    )

@login_required(login_url="admin_login")
def add_result(request):

    if request.method == "POST":

        Result.objects.create(

            student=get_object_or_404(
                Student,
                id=request.POST["student"]
            ),

            unit=get_object_or_404(
                Unit,
                id=request.POST["unit"]
            ),

            cat=request.POST["cat"],

            exam=request.POST["exam"],

            semester=request.POST["semester"]

        )

        messages.success(
            request,
            "Result added successfully."
        )

    return redirect("results")

@login_required(login_url="admin_login")
def edit_result(request, id):

    result = get_object_or_404(
        Result,
        id=id
    )

    if request.method == "POST":

        result.student = get_object_or_404(
            Student,
            id=request.POST["student"]
        )

        result.unit = get_object_or_404(
            Unit,
            id=request.POST["unit"]
        )

        result.cat = request.POST["cat"]

        result.exam = request.POST["exam"]

        result.semester = request.POST["semester"]

        result.save()

        messages.success(
            request,
            "Result updated successfully."
        )

        return redirect("results")

    context = {

        "result": result,

        "results": Result.objects.select_related(
            "student",
            "unit"
        ),

        "students": Student.objects.all(),

        "units": Unit.objects.all(),

    }

    return render(
        request,
        "adminpanel/results.html",
        context
    )

@login_required(login_url="admin_login")
def delete_result(request, id):

    result = get_object_or_404(
        Result,
        id=id
    )

    result.delete()

    messages.success(
        request,
        "Result deleted successfully."
    )

    return redirect("results")

@login_required(login_url="admin_login")
def units(request):

    units = Unit.objects.all().order_by("unit_code")

    context = {
        "units": units,
    }

    return render(
        request,
        "adminpanel/units.html",
        context
    )

@login_required(login_url="admin_login")
def add_unit(request):

    if request.method == "POST":

        Unit.objects.create(

            unit_code=request.POST["unit_code"],

            unit_name=request.POST["unit_name"],

            course=request.POST["course"],

            year=request.POST["year"],

            semester=request.POST["semester"],

            credit_hours=request.POST["credit_hours"]

        )

        messages.success(
            request,
            "Unit added successfully."
        )

    return redirect("adminpanel/units.html")

@login_required(login_url="admin_login")
def edit_unit(request, id):

    unit = get_object_or_404(
        Unit,
        id=id
    )

    if request.method == "POST":

        unit.unit_code = request.POST["unit_code"]

        unit.unit_name = request.POST["unit_name"]

        unit.course = request.POST["course"]

        unit.year = request.POST["year"]

        unit.semester = request.POST["semester"]

        unit.credit_hours = request.POST["credit_hours"]

        unit.save()

        messages.success(
            request,
            "Unit updated successfully."
        )

        return redirect("units")

    context = {

        "unit": unit,

        "units": Unit.objects.all().order_by(
            "unit_code"
        )

    }

    return render(
        request,
        "adminpanel/units.html",
        context
    )

@login_required(login_url="admin_login")
def delete_unit(request, id):

    unit = get_object_or_404(
        Unit,
        id=id
    )

    unit.delete()

    messages.success(
        request,
        "Unit deleted successfully."
    )

    return redirect("adminpanel/units.html")

@login_required(login_url="admin_login")
def timetable(request):

    timetables = Timetable.objects.select_related("unit", "lecturer", "venue").all().order_by("day", "start_time")

    units = Unit.objects.all().order_by("unit_code")

    lecturers = Lecturer.objects.all().order_by("first_name")

    venues = Venue.objects.all().order_by("name")

    context = {
        "timetables": timetables,
        "units": units,
        "lecturers": lecturers,
        "venues": venues,
    }

    return render(request, "adminpanel/timetable.html", context)

@login_required(login_url="admin_login")
def add_timetable(request):

    if request.method == "POST":

        Timetable.objects.create(
            unit=get_object_or_404(Unit, id=request.POST["unit"]),
            lecturer=get_object_or_404(Lecturer, id=request.POST["lecturer"]),
            venue=get_object_or_404(Venue, id=request.POST["venue"]),
            day=request.POST["day"],
            start_time=request.POST["start_time"],
            end_time=request.POST["end_time"],
            semester=request.POST["semester"]
        )

        messages.success(request, "Timetable created successfully.")

    return redirect("adminpanel/timetable.html")

@login_required(login_url="admin_login")
def edit_timetable(request, id):

    timetable = get_object_or_404(Timetable, id=id)

    if request.method == "POST":

        timetable.unit = get_object_or_404(Unit, id=request.POST["unit"])
        timetable.lecturer = get_object_or_404(Lecturer, id=request.POST["lecturer"])
        timetable.venue = get_object_or_404(Venue, id=request.POST["venue"])
        timetable.day = request.POST["day"]
        timetable.start_time = request.POST["start_time"]
        timetable.end_time = request.POST["end_time"]
        timetable.semester = request.POST["semester"]

        timetable.save()

        messages.success(request, "Timetable updated successfully.")

        return redirect("adminpanel/timetable.html")

    context = {
        "timetable": timetable,
        "timetables": Timetable.objects.select_related("unit", "lecturer", "venue").all().order_by("day", "start_time"),
        "units": Unit.objects.all().order_by("unit_code"),
        "lecturers": Lecturer.objects.all().order_by("first_name"),
        "venues": Venue.objects.all().order_by("name"),
    }

    return render(request, "adminpanel/timetable.html", context)

@login_required(login_url="admin_login")
def delete_timetable(request, id):

    timetable = get_object_or_404(Timetable, id=id)

    timetable.delete()

    messages.success(request, "Timetable deleted successfully.")

    return redirect("adminpanel/timetable.html")

@login_required(login_url="admin_login")
def venues(request):

    venues = Venue.objects.all().order_by("building", "name")

    context = {
        "venues": venues,
    }

    return render(request, "adminpanel/venues.html", context)

@login_required(login_url="admin_login")
def add_venue(request):

    if request.method == "POST":

        Venue.objects.create(
            name=request.POST["name"],
            building=request.POST["building"]
        )

        messages.success(request, "Venue added successfully.")

    return redirect("adminpanel/venues.html")

@login_required(login_url="admin_login")
def edit_venue(request, id):

    venue = get_object_or_404(Venue, id=id)

    if request.method == "POST":

        venue.name = request.POST["name"]
        venue.building = request.POST["building"]

        venue.save()

        messages.success(request, "Venue updated successfully.")

        return redirect("venues")

    context = {
        "venue": venue,
        "venues": Venue.objects.all().order_by("building", "name"),
    }

    return render(request, "adminpanel/venues.html", context)

@login_required(login_url="admin_login")
def delete_venue(request, id):

    venue = get_object_or_404(Venue, id=id)

    venue.delete()

    messages.success(request, "Venue deleted successfully.")

    return redirect("adminpanel/venues.html")

@login_required(login_url="admin_login")
def venues(request):

    venues = Venue.objects.all().order_by("building", "name")

    context = {
        "venues": venues,
    }

    return render(request, "adminpanel/venues.html", context)


@login_required(login_url="admin_login")
def add_venue(request):

    if request.method == "POST":

        Venue.objects.create(
            name=request.POST["name"],
            building=request.POST["building"]
        )

        messages.success(request, "Venue added successfully.")

    return redirect("venues")


@login_required(login_url="admin_login")
def edit_venue(request, id):

    venue = get_object_or_404(Venue, id=id)

    if request.method == "POST":

        venue.name = request.POST["name"]
        venue.building = request.POST["building"]

        venue.save()

        messages.success(request, "Venue updated successfully.")

        return redirect("adminpanel/venues.html")

    context = {
        "venue": venue,
        "venues": Venue.objects.all().order_by("building", "name"),
    }

    return render(request, "adminpanel/venues.html", context)


@login_required(login_url="admin_login")
def delete_venue(request, id):

    venue = get_object_or_404(Venue, id=id)

    venue.delete()

    messages.success(request, "Venue deleted successfully.")

    return redirect("adminpanel/venues.html")

from SmartHubApp.models import Lecturer

@login_required(login_url="admin_login")
def lecturers(request):

    lecturers = Lecturer.objects.all().order_by("first_name")

    context = {
        "lecturers": lecturers
    }

    return render(request, "adminpanel/lecturers.html", context)


@login_required(login_url="admin_login")
def add_lecturer(request):

    if request.method == "POST":

        Lecturer.objects.create(
            first_name=request.POST["first_name"],
            last_name=request.POST["last_name"],
            email=request.POST["email"]
        )

        messages.success(request, "Lecturer added successfully.")

    return redirect("lecturers")


@login_required(login_url="admin_login")
def edit_lecturer(request, id):

    lecturer = get_object_or_404(Lecturer, id=id)

    if request.method == "POST":

        lecturer.first_name = request.POST["first_name"]
        lecturer.last_name = request.POST["last_name"]
        lecturer.email = request.POST["email"]

        lecturer.save()

        messages.success(request, "Lecturer updated successfully.")

        return redirect("lecturers")

    context = {
        "lecturer": lecturer,
        "lecturers": Lecturer.objects.all().order_by("first_name")
    }

    return render(request, "adminpanel/lecturers.html", context)

@login_required(login_url="admin_login")
def delete_lecturer(request, id):

    lecturer = get_object_or_404(Lecturer, id=id)

    lecturer.delete()

    messages.success(request, "Lecturer deleted successfully.")

    return redirect("lecturers")

@login_required(login_url="admin_login")
def lecturer_evaluation(request):

    evaluations = LecturerEvaluation.objects.select_related("student").all().order_by("-submitted_at")

    students = Student.objects.all().order_by("first_name")

    context = {
        "evaluations": evaluations,
        "students": students
    }

    return render(request, "adminpanel/lecturer_evaluation.html", context)

@login_required(login_url="admin_login")
def add_evaluation(request):

    if request.method == "POST":

        LecturerEvaluation.objects.create(
            student=get_object_or_404(Student, id=request.POST["student"]),
            lecturer_name=request.POST["lecturer_name"],
            unit_code=request.POST["unit_code"],
            teaching_rating=request.POST["teaching_rating"],
            communication_rating=request.POST["communication_rating"],
            punctuality_rating=request.POST["punctuality_rating"],
            remarks=request.POST["remarks"]
        )

        messages.success(request, "Evaluation submitted successfully.")

    return redirect("lecturer_evaluation")

@login_required(login_url="admin_login")
def edit_evaluation(request, id):

    evaluation = get_object_or_404(LecturerEvaluation, id=id)

    if request.method == "POST":

        evaluation.student = get_object_or_404(Student, id=request.POST["student"])
        evaluation.lecturer_name = request.POST["lecturer_name"]
        evaluation.unit_code = request.POST["unit_code"]
        evaluation.teaching_rating = request.POST["teaching_rating"]
        evaluation.communication_rating = request.POST["communication_rating"]
        evaluation.punctuality_rating = request.POST["punctuality_rating"]
        evaluation.remarks = request.POST["remarks"]

        evaluation.save()

        messages.success(request, "Evaluation updated successfully.")

        return redirect("lecturer_evaluation")

    return redirect("lecturer_evaluation")

@login_required(login_url="admin_login")
def edit_evaluation(request, id):

    evaluation = get_object_or_404(LecturerEvaluation, id=id)

    if request.method == "POST":

        evaluation.student = get_object_or_404(Student, id=request.POST["student"])
        evaluation.lecturer_name = request.POST["lecturer_name"]
        evaluation.unit_code = request.POST["unit_code"]
        evaluation.teaching_rating = request.POST["teaching_rating"]
        evaluation.communication_rating = request.POST["communication_rating"]
        evaluation.punctuality_rating = request.POST["punctuality_rating"]
        evaluation.remarks = request.POST["remarks"]

        evaluation.save()

        messages.success(request, "Evaluation updated successfully.")

        return redirect("lecturer_evaluation")

    return redirect("lecturer_evaluation")


@login_required(login_url="admin_login")
def evaluations(request):

    evaluations = LecturerEvaluation.objects.select_related("student").all().order_by("-submitted_at")

    students = Student.objects.all().order_by("first_name")

    context = {
        "evaluations": evaluations,
        "students": students
    }

    return render(request, "adminpanel/evaluations.html", context)


