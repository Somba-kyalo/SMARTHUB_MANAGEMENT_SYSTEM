from django.contrib import admin
from .models import Fee
from .models import (
    Student,
    Unit,
    UnitRegistration,
    Result,
    Lecturer,
    Venue,
    Timetable,
    Announcement,
    Election,
    Candidate,
    Vote,
)


@admin.register(Student)
class StudentAdmin(admin.ModelAdmin):
    list_display = (
        'first_name',
        'last_name',
        'institution_email',
        'course',
        'admission_number',
        'year_of_study',
    )

    search_fields = (
        'first_name',
        'last_name',
        'institution_email',
        'admission_number',
    )

    list_filter = (
        'course',
        'year_of_study',
        'department',
    )


@admin.register(Unit)
class UnitAdmin(admin.ModelAdmin):
    list_display = (
        'unit_code',
        'unit_name',
        'course',
        'year',
        'semester',
    )

    search_fields = (
        'unit_code',
        'unit_name',
    )


@admin.register(UnitRegistration)
class UnitRegistrationAdmin(admin.ModelAdmin):
    list_display = (
        'student',
        'unit',
        'registered_at',
    )


@admin.register(Result)
class ResultAdmin(admin.ModelAdmin):
    list_display = (
        'student',
        'unit',
        'cat',
        'exam',
        'total',
        'grade',
    )

    list_filter = (
        'grade',
        'semester',
    )


@admin.register(Lecturer)
class LecturerAdmin(admin.ModelAdmin):
    list_display = (
        'first_name',
        'last_name',
        'email',
    )


@admin.register(Venue)
class VenueAdmin(admin.ModelAdmin):
    list_display = (
        'name',
        'building',
    )


@admin.register(Timetable)
class TimetableAdmin(admin.ModelAdmin):
    list_display = (
        'unit',
        'lecturer',
        'venue',
        'day',
        'start_time',
        'end_time',
    )


@admin.register(Announcement)
class AnnouncementAdmin(admin.ModelAdmin):
    list_display = (
        'title',
        'posted_by',
        'important',
        'created_at',
    )


@admin.register(Election)
class ElectionAdmin(admin.ModelAdmin):
    list_display = (
        'title',
        'start_date',
        'end_date',
        'active',
    )


@admin.register(Candidate)
class CandidateAdmin(admin.ModelAdmin):
    list_display = (
        'student_name',
        'position',
        'election',
        'votes',
    )


@admin.register(Vote)
class VoteAdmin(admin.ModelAdmin):
    list_display = (
        'student',
        'candidate',
        'voted_at',
    )


@admin.register(Fee)
class FeeAdmin(admin.ModelAdmin):

    list_display = (
        'student',
        'total_fee',
        'amount_paid',
        'balance',
        'semester',
    )

    list_filter = (
        'semester',
    )

    search_fields = (
        'student__first_name',
        'student__last_name',
        'student__admission_number',
    )