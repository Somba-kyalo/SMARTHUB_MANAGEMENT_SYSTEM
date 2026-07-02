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


def signup(request):

    if request.method == 'POST':

        if Student.objects.filter(
            institution_email=request.POST['institution_email']
        ).exists():

            return render(request,
                          'SmartHubApp/signup.html',
                          {'error': 'Email already exists.'})

        student = Student(
            first_name=request.POST['first_name'],
            middle_name=request.POST['middle_name'],
            last_name=request.POST['last_name'],
            dob=request.POST['dob'],
            gender=request.POST['gender'],
            nationality=request.POST['nationality'],
            phone_number=request.POST['phone_number'],
            address=request.POST['address'],
            county=request.POST['county'],
            postal_code=request.POST['postal_code'],
            faculty=request.POST['faculty'],
            department=request.POST['department'],
            course=request.POST['course'],
            admission_number=request.POST['admission_number'],
            year_of_study=request.POST['year_of_study'],
            study_mode=request.POST['study_mode'],
            guardian_name=request.POST['guardian_name'],
            guardian_phone=request.POST['guardian_phone'],
            personal_email=request.POST['personal_email'],
            institution_email=request.POST['institution_email'],
            username=request.POST['username'],
            password=request.POST['password']
        )

        if 'profile_photo' in request.FILES:
            student.profile_photo = request.FILES['profile_photo']

        student.save()

        return redirect('login')

    return render(request, 'SmartHubApp/signup.html')


def student_login(request):

    if request.method == 'POST':

        email = request.POST['institution_email']
        password = request.POST['password']

        try:
            student = Student.objects.get(
                institution_email=email
            )

            if check_password(password,
                              student.password):

                request.session['student_id'] = student.id

                return redirect('dashboard')

        except Student.DoesNotExist:
            pass

        return render(
            request,
            'SmartHubApp/login.html',
            {'error': 'Invalid email or password'}
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

    student = Student.objects.get(
        id=request.session['student_id']
    )

    units = Unit.objects.all()

    if request.method == 'POST':

        selected_units = request.POST.getlist(
            'units'
        )

        for unit_id in selected_units:

            unit = Unit.objects.get(
                id=unit_id
            )

            UnitRegistration.objects.get_or_create(
                student=student,
                unit=unit
            )

        return redirect('dashboard')

    return render(
        request,
        'SmartHubApp/unit_registration.html',
        {
            'student': student,
            'units': units
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

    student = Student.objects.get(
        id=request.session['student_id']
    )

    fee = Fee.objects.filter(
        student=student
    ).first()

    return render(
        request,
        'SmartHubApp/payment.html',
        {
            'student': student,
            'fee': fee,
        }
    )


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