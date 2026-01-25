from django.contrib.auth.decorators import user_passes_test
from django.shortcuts import render, redirect, get_object_or_404
from .models import Student
from .forms import StudentForm

#  Admin check: only allow superuser
def is_admin(user):
    return user.is_authenticated and user.is_superuser


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


#  Add student
@user_passes_test(is_admin)
def student_add(request):
    if request.method == "POST":
        form = StudentForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("student_list")
    else:
        form = StudentForm()

    return render(request, "admin/student_form.html", {
        "form": form,
        "title": "Add Student"
    })


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

    return render(request, "admin/student_form.html", {
        "form": form,
        "title": "Edit Student"
    })


#  Delete student (confirmation page)
@user_passes_test(is_admin)
def student_delete(request, pk):
    student = get_object_or_404(Student, pk=pk)

    if request.method == "POST":
        student.delete()
        return redirect("student_list")

    return render(request, "admin/student_confirm_delete.html", {
        "student": student
    })
