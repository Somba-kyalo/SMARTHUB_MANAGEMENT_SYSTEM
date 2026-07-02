from django.urls import path
from . import views

urlpatterns = [
    path("login/", views.admin_login, name="admin_login"),
    path("dashboard/", views.admin_dashboard, name="admin_dashboard"),
    path("logout/", views.admin_logout, name="admin_logout"),
    path("students/", views.students, name="students"),
    path("students/add/", views.add_student, name="add_student"),
    path("students/edit/<int:id>/", views.edit_student, name="edit_student"),
    path("students/delete/<int:id>/", views.delete_student, name="delete_student"),
    path("announcements/", views.announcements, name="announcements"),
    path("announcements/add/", views.add_announcement, name="add_announcement"),

    path("announcements/edit/<int:id>/", views.edit_announcement, name="edit_announcement"),

    path("announcements/delete/<int:id>/", views.delete_announcement, name="delete_announcement"),
    path("candidates/",views.candidates, name="candidates"),

    path("candidates/add/",views.add_candidate,name="add_candidate"),

    path("candidates/edit/<int:id>/",views.edit_candidate,name="edit_candidate"),

    path("candidates/delete/<int:id>/", views.delete_candidate, name="delete_candidate"),
    path("elections/", views.elections, name="elections"),
    path("elections/add/", views.add_election, name="add_election"),
    path("elections/edit/<int:id>/", views.edit_election, name="edit_election"),
    path("elections/delete/<int:id>/", views.delete_election, name="delete_election"),
    path("fees/", views.fees, name="fees"),
    path("fees/add/", views.add_fee, name="add_fee"),
    path("fees/edit/<int:id>/", views.edit_fee, name="edit_fee"),
    path("fees/delete/<int:id>/", views.delete_fee, name="delete_fee"),
    path("lecturer-evaluations/", views.lecturer_evaluations, name="lecturer_evaluations"),
    path("lecturer-evaluations/delete/<int:id>/", views.delete_evaluation, name="delete_evaluation"),
    path("results/", views.results, name="results"),

    path("results/add/", views.add_result,name="add_result"),

    path("results/edit/<int:id>/", views.edit_result, name="edit_result"),

    path("results/delete/<int:id>/", views.delete_result, name="delete_result"),
    path("units/", views.units, name="units"),
    path("units/add/", views.add_unit, name="add_unit"),
    path("units/edit/<int:id>/", views.edit_unit, name="edit_unit"),
    path("units/delete/<int:id>/", views.delete_unit, name="delete_unit"),
    path("timetable/", views.timetable, name="timetable"),
    path("timetable/add/", views.add_timetable, name="add_timetable"),
    path("timetable/edit/<int:id>/", views.edit_timetable, name="edit_timetable"),
    path("timetable/delete/<int:id>/", views.delete_timetable, name="delete_timetable"),
    path("venues/", views.venues, name="venues"),
    path("venues/add/", views.add_venue, name="add_venue"),
    path("venues/edit/<int:id>/", views.edit_venue, name="edit_venue"),
    path("venues/delete/<int:id>/", views.delete_venue, name="delete_venue"),
    path("venues/", views.venues, name="venues"),
    path("venues/add/", views.add_venue, name="add_venue"),
    path("venues/edit/<int:id>/", views.edit_venue, name="edit_venue"),
    path("venues/delete/<int:id>/", views.delete_venue, name="delete_venue"),
    path("lecturers/", views.lecturers, name="lecturers"),
    path("lecturers/add/", views.add_lecturer, name="add_lecturer"),
    path("lecturers/edit/<int:id>/", views.edit_lecturer, name="edit_lecturer"),
    path("lecturers/delete/<int:id>/", views.delete_lecturer, name="delete_lecturer"),
    path("lecturer_evaluation/", views.lecturer_evaluation, name="lecturer_evaluation"),
path("lecturer-evaluation/add/", views.add_evaluation, name="add_evaluation"),
path("lecturer-evaluation/edit/<int:id>/", views.edit_evaluation, name="edit_evaluation"),
path("lecturer-evaluation/delete/<int:id>/", views.delete_evaluation, name="delete_evaluation"),
path("evaluations/", views.evaluations, name="evaluations"),
path("evaluations/add/", views.add_evaluation, name="add_evaluation"),
path("evaluations/edit/<int:id>/", views.edit_evaluation, name="edit_evaluation"),
path("evaluations/delete/<int:id>/", views.delete_evaluation, name="delete_evaluation"),
]

