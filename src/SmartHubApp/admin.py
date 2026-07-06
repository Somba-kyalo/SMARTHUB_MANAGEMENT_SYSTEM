from django.contrib import admin
from .models import Fee
from .models import LecturerEvaluation

#admin.site.register(Fee)
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

from django.contrib import admin
from .models import Student

@admin.register(Student)
class StudentAdmin(admin.ModelAdmin):

    list_display = ("registration_number", "first_name", "last_name", "institution_email", "course", "year")

    search_fields = ("registration_number", "first_name", "last_name", "institution_email", "username")

    list_filter = ("course", "year", "department")


@admin.register(Unit)
class UnitAdmin(admin.ModelAdmin):
    list_display = (
        "unit_code",
        "unit_name",
        "course",
        "year",
        "semester",
        "credit_hours",
    )

    search_fields = (
        "unit_code",
        "unit_name",
        "course",
    )

    list_filter = (
        "course",
        "year",
        "semester",
    )


@admin.register(UnitRegistration)
class UnitRegistrationAdmin(admin.ModelAdmin):
    list_display = (
        "student",
        "unit",
        "registered_at",
    )

    search_fields = (
        "student__registration_number",
        "student__first_name",
        "student__last_name",
        "unit__unit_code",
        "unit__unit_name",
    )

    list_filter = (
        "unit__course",
        "unit__year",
        "unit__semester",
        "registered_at",
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
        "student",
        "total_fee",
        "amount_paid",
        "balance",
        "completion",
        "updated_at",
    )

    search_fields = (
        "student__registration_number",
        "student__first_name",
        "student__last_name",
    )

    readonly_fields = (
        "student",
        "total_fee",
        "balance",
        "completion",
        "updated_at",
    )

    # this ensures admin cannot create duplicate fee records
    def has_add_permission(self, request):
        return False   

@admin.register(LecturerEvaluation)
class LecturerEvaluationAdmin(admin.ModelAdmin):

    list_display = (
        'student',
        'lecturer_name',
        'unit_code',
        'teaching_rating',
        'submitted_at'
    )

    search_fields = (
        'lecturer_name',
        'unit_code'
    )

    list_filter = (
        'teaching_rating',
        'submitted_at'
    )