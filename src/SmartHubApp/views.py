from django.shortcuts import render, redirect
from django.contrib.auth.hashers import check_password
from .models import Student
from .models import Unit, UnitRegistration
from .models import Result
from .models import Election, Candidate, Vote
from statistics import mean
from .models import Announcement
from .models import Timetable, UnitRegistration
from .models import Fee



def home(request):
    return render(request, 'SmartHubApp/home.html')


def about(request):
    return render(request, 'SmartHubApp/about.html')


def contact(request):
    return render(request, 'SmartHubApp/contact.html')


def departments(request):
    return render(request, 'SmartHubApp/departments.html')


def courses(request):
    return render(request, 'SmartHubApp/courses.html')


def help_support(request):
    return render(request, 'SmartHubApp/help_support.html')

def lecturer_evaluation(request):
    return render(request, 'SmartHub/lecturer_evaluation')


def academic_calendar(request):
    return render(request, 'SmartHubApp/academic_calendar.html')


from django.shortcuts import render
from .models import Student
from datetime import datetime

def generate_registration_number(course):

    if course == "Computer Science": prefix = "CS"
    elif course == "Information Technology": prefix = "IT"
    else: prefix = "SE"

    total = Student.objects.filter(course=course).count() + 1
    number = total * 10
    year = datetime.now().year

    return f"{prefix}221-{number:04d}/{year}"


def generate_username(first_name, last_name):

    username = f"{first_name.lower()}{last_name.lower()}"

    if not Student.objects.filter(username=username).exists():
        return username

    count = 1

    while Student.objects.filter(username=f"{username}{count}").exists():
        count += 1

    return f"{username}{count}"


def generate_institution_email(first_name, last_name):

    email = f"{first_name.lower()}.{last_name.lower()}@smarthub.com"

    if not Student.objects.filter(institution_email=email).exists():
        return email

    count = 1

    while Student.objects.filter(institution_email=f"{first_name.lower()}.{last_name.lower()}{count}@smarthub.com").exists():
        count += 1

    return f"{first_name.lower()}.{last_name.lower()}{count}@smarthub.com"
    
def signup(request):

    if request.method == "POST":

        if request.POST["password"] != request.POST["confirm_password"]:
            return render(request, "SmartHubApp/signup.html", {"error": "Passwords do not match."})

        registration_number = generate_registration_number(request.POST["course"])
        username = generate_username(request.POST["first_name"], request.POST["last_name"])
        institution_email = generate_institution_email(request.POST["first_name"], request.POST["last_name"])

        student = Student(
            first_name=request.POST["first_name"],
            middle_name=request.POST["middle_name"],
            last_name=request.POST["last_name"],
            dob=request.POST["dob"],
            gender=request.POST["gender"],
            nationality=request.POST["nationality"],
            phone=request.POST["phone"],
            county=request.POST["county"],
            address=request.POST["address"],
            postal_code=request.POST["postal_code"],
            faculty=request.POST["faculty"],
            department=request.POST["department"],
            course=request.POST["course"],
            year=request.POST["year"],
            study_mode=request.POST["study_mode"],
            guardian_name=request.POST["guardian_name"],
            guardian_phone=request.POST["guardian_phone"],
            personal_email=request.POST["personal_email"],
            registration_number=registration_number,
            institution_email=institution_email,
            username=username,
            password=request.POST["password"]
        )

        student.save()

        

        if student.course == "Information Technology":
            total_fee = 200000
        elif student.course == "Computer Science":
            total_fee = 225000
        elif student.course == "Software Engineering":
            total_fee = 250000
        else:
            total_fee = 200000

        Fee.objects.create(
            student=student,
            total_fee=total_fee,
            amount_paid=0
        )

        return render(request, "SmartHubApp/success.html", {"student": student})

    return render(request, "SmartHubApp/signup.html")


from django.db.models import Q
from django.contrib.auth.hashers import check_password

def student_login(request):

    if request.method == 'POST':

        login = request.POST['login']
        password = request.POST['password']

        try:

            student = Student.objects.get(
                Q(registration_number=login) | Q(institution_email=login)
            )

            if check_password(password, student.password):

                request.session['student_id'] = student.id

                return redirect('dashboard')

        except Student.DoesNotExist:
            pass

        return render(
            request,
            'SmartHubApp/login.html',
            {'error': 'Invalid registration number, email or password.'}
        )

    return render(request, 'SmartHubApp/login.html')

def dashboard(request):

    if 'student_id' not in request.session:
        return redirect('login')

    student = Student.objects.get(
        id=request.session['student_id']
    )

    return render(
        request,
        'SmartHubApp/dashboard.html',
        {'student': student}
    )


def logout_view(request):
    request.session.flush()
    return redirect('login')



def profile(request):

    if 'student_id' not in request.session:
        return redirect('login')

    student = Student.objects.get(
        id=request.session['student_id']
    )

    return render(
        request,
        'SmartHubApp/profile.html',
        {
            'student': student
        }
    )


def unit_registration(request):

    if 'student_id' not in request.session:
        return redirect('login')

    student = Student.objects.get(id=request.session['student_id'])

    units = Unit.objects.filter(course=student.course, year=student.year)

    registered_units = UnitRegistration.objects.filter(student=student)

    if request.method == 'POST':

        if registered_units.exists():
            return redirect('unit_registration')

        selected_units = request.POST.getlist('units')

        for unit_id in selected_units:

            unit = Unit.objects.get(id=unit_id)

            UnitRegistration.objects.create(student=student, unit=unit)

        return redirect('unit_registration')

    return render(
        request,
        'SmartHubApp/unit_registration.html',
        {
            'student': student,
            'units': units,
            'registered_units': registered_units
        }
    )


def results(request):

    if 'student_id' not in request.session:
        return redirect('login')

    student = Student.objects.get(
        id=request.session['student_id']
    )

    results = Result.objects.filter(
        student=student
    )

    totals = [r.total for r in results]

    average = 0

    if totals:
        average = round(mean(totals), 2)

    return render(
        request,
        'SmartHubApp/results.html',
        {
            'student': student,
            'results': results,
            'average': average
        }
    )


from .models import Election, Candidate, Vote


def elections(request):

    if 'student_id' not in request.session:
        return redirect('login')

    student = Student.objects.get(
        id=request.session['student_id']
    )

    election = Election.objects.filter(
        active=True
    ).first()

    candidates = Candidate.objects.filter(
        election=election
    )

    if request.method == "POST":

        candidate_id = request.POST.get(
            'candidate'
        )

        candidate = Candidate.objects.get(
            id=candidate_id
        )

        already_voted = Vote.objects.filter(
            student=student,
            candidate__position=candidate.position
        ).exists()

        if not already_voted:

            Vote.objects.create(
                student=student,
                candidate=candidate
            )

            candidate.votes += 1
            candidate.save()

        return redirect('elections')

    return render(
        request,
        'SmartHubApp/elections.html',
        {
            'election': election,
            'candidates': candidates
        }
    )


def announcements(request):

    if 'student_id' not in request.session:
        return redirect('login')

    student = Student.objects.get(
        id=request.session['student_id']
    )

    announcements = Announcement.objects.all()

    return render(
        request,
        'SmartHubApp/announcements.html',
        {
            'student': student,
            'announcements': announcements
        }
    )



def timetable(request):

    if 'student_id' not in request.session:
        return redirect('login')

    student = Student.objects.get(
        id=request.session['student_id']
    )

    registered_units = UnitRegistration.objects.filter(
        student=student
    ).values_list(
        'unit',
        flat=True
    )

    timetable = Timetable.objects.filter(
        unit__in=registered_units
    )

    return render(
        request,
        'SmartHubApp/timetable.html',
        {
            'student': student,
            'timetable': timetable
        }
    )


def payment(request):

    if 'student_id' not in request.session:
        return redirect('login')

    student = Student.objects.get(id=request.session['student_id'])

    fee = Fee.objects.filter(student=student).first()

    if not fee:
        fee = Fee.objects.create(
            student=student,
            total_fee=0,
            amount_paid=0
        )

    balance = fee.balance
    percentage = fee.completion

    if percentage == 0:
        remark = "No payment made yet"
    elif percentage < 50:
        remark = "Payment is in progress"
    elif percentage < 100:
        remark = "Almost complete"
    else:
        remark = "Fully paid"

    return render(request, "SmartHubApp/payment.html", {
        "student": student,
        "fee": fee,
        "balance": balance,
        "percentage": percentage,
        "remark": remark
    })
    return render(request, "SmartHubApp/payment.html", context)


def lecturer_evaluation(request):

    if 'student_id' not in request.session:
        return redirect('login')

    student = Student.objects.get(
        id=request.session['student_id']
    )

    if request.method == 'POST':

        LecturerEvaluation.objects.create(
            student=student,
            lecturer_name=request.POST['lecturer_name'],
            unit_code=request.POST['unit_code'],
            teaching_rating=request.POST['teaching_rating'],
            communication_rating=request.POST['communication_rating'],
            punctuality_rating=request.POST['punctuality_rating'],
            remarks=request.POST['remarks']
        )

        return render(
            request,
            'SmartHubApp/lecturer_evaluation.html',
            {
                'success':
                'Evaluation submitted successfully.'
            }
        )

    return render(
        request,
        'SmartHubApp/lecturer_evaluation.html'
    )

