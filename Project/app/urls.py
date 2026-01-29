from django.urls import path
from .views import (
    login_view, logout_view, home_view, about_view, profile_view,
    student_dashboard, attendance_history, monthly_summary
)
from .admin_views import (admin_dashboard,student_list,student_add,student_edit,student_delete,mark_attendance,edit_attendance,attendance_report)


urlpatterns = [
    # Home
    path("", home_view, name="home"),
    path("about/", about_view, name="about"),
    
    # Authentication (REMOVED SIGNUP)
    path("login/", login_view, name="login"),
    path("logout/", logout_view, name="logout"),

    path("profile/", profile_view, name="profile"),

    # Student Views (Person 3)
    path("dashboard/", student_dashboard, name="student_dashboard"),
    path("attendance/history/", attendance_history, name="attendance_history"),
    path("attendance/monthly/", monthly_summary, name="monthly_summary"),

    # Admin dashboard + Student CRUD
    path("admin-dashboard/", admin_dashboard, name="admin_dashboard"),
    path("admin-students/", student_list, name="student_list"),
    path("admin-students-add/", student_add, name="student_add"),
    path("admin-students-edit/<int:pk>/", student_edit, name="student_edit"),
    path("admin-students-delete/<int:pk>/", student_delete, name="student_delete"),

    # Admin Attendance Management
    path("mark/", mark_attendance, name="attendance_mark"),
    path("edit/<int:pk>/", edit_attendance, name="attendance_edit"),
    path("report/", attendance_report, name="attendance_report"),
]