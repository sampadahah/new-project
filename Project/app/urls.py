from django.urls import path
from .views import signup_view, login_view, logout_view,home_view, about_view, profile_view
from .admin_views import (admin_dashboard,student_list,student_add,student_edit,student_delete,mark_attendance,edit_attendance,daily_report,monthly_report)

urlpatterns = [
    # Home
    path("", home_view, name="home"),
    path("about/", about_view, name="about"),
    # Authentication
    path("login/", login_view, name="login"),
    path("signup/", signup_view, name="signup"),
    path("logout/", logout_view, name="logout"),

    path("profile/", profile_view, name="profile"),

    # Admin dashboard + Student CRUD
    path("admin-panel/dashboard/", admin_dashboard, name="admin_dashboard"),
    path("admin-panel/students/", student_list, name="student_list"),
    path("admin-panel/students/add/", student_add, name="student_add"),
    path("admin-panel/students/<int:pk>/edit/", student_edit, name="student_edit"),
    path("admin-panel/students/<int:pk>/delete/", student_delete, name="student_delete"),

    path("mark/", mark_attendance, name="attendance_mark"),
    path("edit/<int:pk>/", edit_attendance, name="attendance_edit"),

    path("report/daily/", daily_report, name="attendance_daily_report"),
    path("report/monthly/", monthly_report, name="attendance_monthly_report"),

]