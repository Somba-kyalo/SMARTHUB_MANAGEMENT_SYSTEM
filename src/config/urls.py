from django.contrib import admin
from django.urls import path

from SmartHubApp.views import (
    home,
    about,
    contact,
    courses,
    departments,
    signup,
    student_login,
    help_support,
    dashboard,
    logout_view,
    profile,
    unit_registration,
    results,
    elections,
    announcements,
    payment,
    lecturer_evaluation,
    timetable,
    academic_calendar
)

urlpatterns = [
    path('admin/', admin.site.urls),

    path('', home, name='home'),
    path('about/', about, name='about'),
    path('contact/', contact, name='contact'),
    path('courses/', courses, name='courses'),
    path('departments/', departments, name='departments'),

    path('signup/', signup, name='signup'),
    path('login/', student_login, name='login'),
    path('logout/', logout_view, name='logout'),

    path('help_support/', help_support, name='help_support'),
    path('dashboard/', dashboard, name='dashboard'),
    path('profile/', profile, name='profile'),
    path('unit_registration/',unit_registration, name='unit_registration'),
    path('results/' ,results, name='results'),
    path('elections/', elections, name='elections'),
    path('announcements/', announcements, name='announcements'),
    path('payment/', payment, name='payment'),
    path('lecturer_evaluation/', lecturer_evaluation, name='lecturer_evaluation'),
    path('timetable/', timetable, name='timetable'),
    path('academic_calendar/', academic_calendar, name='academic_calendar'),

]
