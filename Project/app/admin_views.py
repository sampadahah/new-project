from django.contrib.auth.decorators import user_passes_test, login_required
from django.shortcuts import render, redirect, get_object_or_404
from .models import Student, Attendance
from .forms import StudentForm, AttendanceMarkForm, DailyReportForm, MonthlyReportForm
import calendar
from datetime import date as dt_date
from django.db.models import Count, Q

#  Admin check: only allow superuser
def is_admin(user):
    return user.is_authenticated and user.is_superuser

@login_required
#  Admin dashboard (basic stats + entry points)
@user_passes_test(is_admin)
def admin_dashboard(request):
    return render(request, "admin/admin_dashboard.html", {
        "total_students": Student.objects.count()
    })


#  View student list
@user_passes_test(is_admin)
def student_list(request):
    students = Student.objects.all().order_by("student_id")
    return render(request, "admin/student_list.html", {
        "students": students
    })

@login_required
#  Add student
def student_add(request):
    if request.method == "POST":
        form = StudentForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("student_list")
    else:
        form = StudentForm()

    return render(request, "admin/student_add.html", {"form": form})
# @user_passes_test(is_admin)
# def student_add(request):
#     if request.method == "POST":
#         form = StudentForm(request.POST)
#         if form.is_valid():
#             form.save()
#             return redirect("student_list")
#     else:
#         form = StudentForm()

#     return render(request, "admin/student_form.html", {
#         "form": form
#     })

@login_required
#  Edit student
@user_passes_test(is_admin)
def student_edit(request, pk):
    student = get_object_or_404(Student, pk=pk)

    if request.method == "POST":
        form = StudentForm(request.POST, instance=student)
        if form.is_valid():
            form.save()
            return redirect("student_list")
    else:
        form = StudentForm(instance=student)

    return render(request, "admin/student_edit.html", {
        "form": form,
        "title": "Edit Student"
    })

@login_required
#  Delete student (confirmation page)
@login_required
@user_passes_test(is_admin)
def student_delete(request, pk):
    student = get_object_or_404(Student, pk=pk)

    if request.method == "POST":
        # Store user reference before deleting student
        user_account = student.user
        
        # Delete the student record
        student.delete()
        
        # Also delete the associated user account if it exists
        if user_account:
            user_account.delete()
        
        return redirect("student_list")

    return render(request, "admin/student_confirm_delete.html", {
        "student": student
    })

# mark daily attendance
@login_required
@user_passes_test(is_admin)
def mark_attendance(request):
    form = AttendanceMarkForm(request.GET or None)
    if not form.is_valid():
        return render(request, "admin/mark.html", {"form": form, "rows": None})

    att_date = form.cleaned_data["date"]
    program = form.cleaned_data["program"]
    batch = form.cleaned_data["batch"]

    students = Student.objects.filter(program=program, batch=batch).order_by("full_name")

    # existing attendance for selected date
    existing = Attendance.objects.filter(student__in=students, date=att_date)
    existing_map = {a.student_id: a for a in existing}

    if request.method == "POST":
        present_ids = set(map(int, request.POST.getlist("present")))

        for s in students:
            a = existing_map.get(s.id)
            if a is None:
                a = Attendance(student=s, date=att_date)
            a.is_present = (s.id in present_ids)
            a.marked_by = request.user
            a.save()

        return redirect("attendance_mark")  

    rows = []
    for s in students:
        a = existing_map.get(s.id)
        rows.append({
            "student": s,
            "is_present": True if a is None else a.is_present
        })

    return render(
        request,
        "admin/mark.html",
        {"form": form, "rows": rows, "att_date": att_date, "program": program, "batch": batch}
    )


@login_required
@user_passes_test(is_admin)
def attendance_report(request):
    report_type = request.GET.get("type", "daily")  # "daily" or "monthly"

    daily_form = DailyReportForm(request.GET or None)
    monthly_form = MonthlyReportForm(request.GET or None)

    daily_ctx = {"rows": None, "summary": None}
    monthly_ctx = {"table": None, "meta": None}

    # DAILY
    if report_type == "daily" and daily_form.is_valid():
        att_date = daily_form.cleaned_data["date"]
        program = daily_form.cleaned_data["program"]
        batch = daily_form.cleaned_data["batch"]

        students = Student.objects.filter(program=program, batch=batch).order_by("full_name")
        qs = Attendance.objects.filter(student__in=students, date=att_date).select_related("student")
        att_map = {a.student_id: a for a in qs}

        present_count = 0
        rows = []
        for s in students:
            a = att_map.get(s.id)
            is_present = a.is_present if a else False
            if is_present:
                present_count += 1
            rows.append({"student": s, "is_present": is_present})

        total = students.count()
        daily_ctx["rows"] = rows
        daily_ctx["summary"] = {
            "date": att_date,
            "program": program,
            "batch": batch,
            "total": total,
            "present": present_count,
            "absent": total - present_count,
            "percent": round((present_count / total) * 100, 2) if total else 0,
        }

    # MONTHLY
    if report_type == "monthly" and monthly_form.is_valid():
        program = monthly_form.cleaned_data["program"]
        batch = monthly_form.cleaned_data["batch"]
        month = int(monthly_form.cleaned_data["month"])
        year = int(monthly_form.cleaned_data["year"])

        last_day = calendar.monthrange(year, month)[1]
        start = dt_date( year, month, 1)
        end = dt_date(year, month, last_day)

        students = Student.objects.filter(program=program, batch=batch).order_by("full_name")
        qs = Attendance.objects.filter(student__in=students, date__range=(start, end))

        agg = (
            qs.values("student_id")
            .annotate(
                present=Count("id", filter=Q(is_present=True)),
                absent=Count("id", filter=Q(is_present=False)),
                total=Count("id"),
            )
        )
        agg_map = {a["student_id"]: a for a in agg}

        table = []
        for s in students:
            a = agg_map.get(s.id, {"present": 0, "absent": 0, "total": 0})
            total = a["total"]
            present = a["present"]
            percent = round((present / total) * 100, 2) if total else 0
            table.append({"student": s, "total": total, "present": present, "absent": a["absent"], "percent": percent})

        monthly_ctx["table"] = table
        monthly_ctx["meta"] = {"program": program, "batch": batch, "year":year, "month": month,  "start": start, "end": end}

    return render(
        request,
        "admin/report.html",
        {
            "report_type": report_type,
            "daily_form": daily_form,
            "monthly_form": monthly_form,
            **daily_ctx,
            **monthly_ctx,
        },
    )