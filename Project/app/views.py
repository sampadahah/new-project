from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, logout
from .forms import SignUpForm, LoginForm, ProfileForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth import update_session_auth_hash
from .models import Student, Attendance
from django.db.models import Count, Q
from django.utils import timezone
import calendar
from datetime import datetime, timedelta
# Create your views here.
def signup_view(request):
    if request.method == "POST":
        form = SignUpForm(request.POST)#creates form object with submitted data
        if form.is_valid():#every fields are checked against validation rules
            user = form.save()      #  password hashed automatically
            login(request, user)    #  auto login after signup
            return redirect("home")
    else:
        form = SignUpForm()
    return render(request, "signup.html", {"form": form})


from django.shortcuts import redirect, render
from django.contrib.auth import login
from .forms import LoginForm

def login_view(request):
    # If already logged in, redirect immediately
    if request.user.is_authenticated:
        if request.user.is_superuser:
            return redirect("admin_dashboard")
        return redirect("home")

    if request.method == "POST":
        form = LoginForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)

            if user.is_superuser:
                return redirect("admin_dashboard")
<<<<<<< HEAD
            return redirect("home")
=======

            # Normal users go to student dashboard
            return redirect("student_dashboard")
>>>>>>> 72b4a8bf9b7009b6ff0e664b8861022efd2d9bc5
    else:
        form = LoginForm()

    return render(request, "login.html", {"form": form})

def logout_view(request):
    logout(request)  # clears session properly
    return redirect("login")

def home_view(request):
    return render(request, "home.html")

def about_view(request):
    return render(request, "about.html")

@login_required
def profile_view(request):
    user = request.user

    if request.method == "POST":
        form = ProfileForm(request.POST, instance=user)
        if form.is_valid():
            user = form.save(commit=False)

            new_password = form.cleaned_data.get("new_password1")
            if new_password:
                user.set_password(new_password)
                update_session_auth_hash(request, user)

            user.save()
            return redirect("profile")
    else:
        form = ProfileForm(instance=user)

    return render(request, "profile.html", {"form": form})

<<<<<<< HEAD
=======

# ================= STUDENT VIEWS (Person 3) =================

@login_required
def student_dashboard(request):
    """Student dashboard with attendance overview"""
    try:
        # Get the student record linked to this user
        student = Student.objects.get(user=request.user)
    except Student.DoesNotExist:
        # If no student record exists, show a message
        return render(request, "student_dashboard.html", {
            "no_student_record": True,
            "message": "No student record found. Please contact admin."
        })
    
    # Get attendance statistics
    total_attendance = Attendance.objects.filter(student=student).count()
    present_days = Attendance.objects.filter(student=student, is_present=True).count()
    absent_days = total_attendance - present_days
    
    # Calculate attendance percentage
    attendance_percentage = round((present_days / total_attendance) * 100, 2) if total_attendance > 0 else 0
    
    # Get recent attendance (last 7 records)
    recent_attendance = Attendance.objects.filter(student=student).order_by('-date')[:7]
    
    # This month's attendance
    today = timezone.localdate()
    start_of_month = today.replace(day=1)
    this_month_total = Attendance.objects.filter(
        student=student, 
        date__gte=start_of_month,
        date__lte=today
    ).count()
    this_month_present = Attendance.objects.filter(
        student=student, 
        date__gte=start_of_month,
        date__lte=today,
        is_present=True
    ).count()
    this_month_percentage = round((this_month_present / this_month_total) * 100, 2) if this_month_total > 0 else 0
    
    # Last 7 days attendance
    week_ago = today - timedelta(days=7)
    week_total = Attendance.objects.filter(
        student=student,
        date__gte=week_ago,
        date__lte=today
    ).count()
    week_present = Attendance.objects.filter(
        student=student,
        date__gte=week_ago,
        date__lte=today,
        is_present=True
    ).count()
    week_percentage = round((week_present / week_total) * 100, 2) if week_total > 0 else 0
    
    context = {
        'student': student,
        'total_attendance': total_attendance,
        'present_days': present_days,
        'absent_days': absent_days,
        'attendance_percentage': attendance_percentage,
        'recent_attendance': recent_attendance,
        'this_month_percentage': this_month_percentage,
        'week_percentage': week_percentage,
    }
    
    return render(request, "student_dashboard.html", context)


@login_required
def attendance_history(request):
    """View personal attendance history with filtering options"""
    try:
        student = Student.objects.get(user=request.user)
    except Student.DoesNotExist:
        return render(request, "attendence_history.html", {
            "no_student_record": True,
            "message": "No student record found. Please contact admin."
        })
    
    # Get filter parameters
    month = request.GET.get('month')
    year = request.GET.get('year')
    status = request.GET.get('status')  # 'present', 'absent', or 'all'
    
    # Base queryset
    attendance_records = Attendance.objects.filter(student=student).order_by('-date')
    
    # Apply filters
    if month and year:
        attendance_records = attendance_records.filter(
            date__month=int(month),
            date__year=int(year)
        )
    elif year:
        attendance_records = attendance_records.filter(date__year=int(year))
    
    if status == 'present':
        attendance_records = attendance_records.filter(is_present=True)
    elif status == 'absent':
        attendance_records = attendance_records.filter(is_present=False)
    
    # Pagination could be added here if needed
    attendance_records = attendance_records[:100]  # Limit to 100 records for performance
    
    # Generate year and month choices for filters
    current_year = timezone.localdate().year
    years = list(range(current_year - 2, current_year + 1))
    months = [(i, calendar.month_name[i]) for i in range(1, 13)]
    
    context = {
        'student': student,
        'attendance_records': attendance_records,
        'years': years,
        'months': months,
        'selected_month': int(month) if month else None,
        'selected_year': int(year) if year else None,
        'selected_status': status,
    }
    
    return render(request, "attendence_history.html", context)


@login_required
def monthly_summary(request):
    """View monthly attendance summary"""
    try:
        student = Student.objects.get(user=request.user)
    except Student.DoesNotExist:
        return render(request, "monthly_summary.html", {
            "no_student_record": True,
            "message": "No student record found. Please contact admin."
        })
    
    # Get selected month and year, default to current month
    today = timezone.localdate()
    selected_month = int(request.GET.get('month', today.month))
    selected_year = int(request.GET.get('year', today.year))
    
    # Calculate date range for the selected month
    last_day = calendar.monthrange(selected_year, selected_month)[1]
    start_date = datetime(selected_year, selected_month, 1).date()
    end_date = datetime(selected_year, selected_month, last_day).date()
    
    # Get attendance records for the month
    monthly_records = Attendance.objects.filter(
        student=student,
        date__range=(start_date, end_date)
    ).order_by('date')
    
    # Calculate statistics
    total_days = monthly_records.count()
    present_days = monthly_records.filter(is_present=True).count()
    absent_days = total_days - present_days
    attendance_percentage = round((present_days / total_days) * 100, 2) if total_days > 0 else 0
    
    # Generate calendar data for visualization
    cal = calendar.monthcalendar(selected_year, selected_month)
    attendance_map = {record.date.day: record.is_present for record in monthly_records}
    
    # Generate year and month choices
    current_year = timezone.localdate().year
    years = list(range(current_year - 2, current_year + 1))
    months = [(i, calendar.month_name[i]) for i in range(1, 13)]
    
    context = {
        'student': student,
        'selected_month': selected_month,
        'selected_year': selected_year,
        'month_name': calendar.month_name[selected_month],
        'total_days': total_days,
        'present_days': present_days,
        'absent_days': absent_days,
        'attendance_percentage': attendance_percentage,
        'monthly_records': monthly_records,
        'calendar_weeks': cal,
        'attendance_map': attendance_map,
        'years': years,
        'months': months,
    }
    
    return render(request, "monthly_summary.html", context)
>>>>>>> 72b4a8bf9b7009b6ff0e664b8861022efd2d9bc5
# @login_required
# def profile_view(request):
#     return render(request, "profile.html")


# @login_required
# def edit_profile_view(request):
#     user = request.user

#     if request.method == "POST":
#         form = EditProfileForm(request.POST, instance=user)
#         if form.is_valid():
#             form.save()
#             return redirect("profile")
#     else:
#         form = EditProfileForm(instance=user)

#     return render(request, "edit_profile.html", {"form": form})
# @login_required
# def profile_view(request):
#     user = request.user

#     profile_form = EditProfileForm(instance=user)
#     password_form = PasswordChangeForm(user=user)

#     if request.method == "POST":

#         # Update profile
#         if "save_profile" in request.POST:
#             profile_form = EditProfileForm(request.POST, instance=user)
#             if profile_form.is_valid():
#                 profile_form.save()
#                 return redirect("profile")

#         # Change password
#         if "change_password" in request.POST:
#             password_form = PasswordChangeForm(user=user, data=request.POST)
#             if password_form.is_valid():
#                 user = password_form.save()
#                 update_session_auth_hash(request, user)
#                 return redirect("profile")

#     return render(request, "profile.html", {
#         "profile_form": profile_form,
#         "password_form": password_form
#     })