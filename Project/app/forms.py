from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from .models import CustomUser, Student
from django.contrib.auth.password_validation import validate_password
from django.utils import timezone
from django.contrib.auth import get_user_model
import calendar

class SignUpForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = CustomUser
        fields = ("username", "email", "password1", "password2")#Which inputs appear on signup form

    def __init__(self, *args, **kwargs):#This is the constructor
        super().__init__(*args, **kwargs)#Calls Django’s original form setup
        for f in self.fields.values():
            f.widget.attrs["class"] = "form-control"


class LoginForm(AuthenticationForm):
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for f in self.fields.values():
            f.widget.attrs["class"] = "form-control"


User = get_user_model()

# ModelForm used for Add & Update operations
# ModelForm used for Add & Update operations
class StudentForm(forms.ModelForm):
    username = forms.CharField(
        max_length=150,
        required=True,
        widget=forms.TextInput(attrs={"class": "form-control", "placeholder": "Enter username"})
    )
    password = forms.CharField(
        required=True,
        widget=forms.PasswordInput(attrs={"class": "form-control", "placeholder": "Enter temporary password"})
    )
    
    class Meta:
        model = Student
        fields = ["student_id", "full_name", "email", "program", "batch", "year"]
        widgets = {
            "student_id": forms.TextInput(attrs={"class": "form-control", "placeholder": "e.g., STU001"}),
            "full_name": forms.TextInput(attrs={"class": "form-control", "placeholder": "Enter full name"}),
            "email": forms.EmailInput(attrs={"class": "form-control", "placeholder": "student@example.com"}),
            "program": forms.TextInput(attrs={"class": "form-control", "placeholder": "e.g., Computer Science"}),
            "batch": forms.TextInput(attrs={"class": "form-control", "placeholder": "e.g., 2024"}),
            "year": forms.TextInput(attrs={"class": "form-control", "placeholder": "e.g., 2023"}),
        }

    def save(self, commit=True):
        # 1️⃣ Create login user
        user = User.objects.create_user(
            username=self.cleaned_data["username"],
            password=self.cleaned_data["password"],
            email=self.cleaned_data["email"],
        )

        # 2️⃣ Create student record
        student = super().save(commit=False)
        student.user = user

        if commit:
            user.save()
            student.save()

        return student
# class EditProfileForm(forms.ModelForm):
#     class Meta:
#         model = CustomUser
#         fields = ("username", "email")

#     def __init__(self, *args, **kwargs):
#         super().__init__(*args, **kwargs)
#         for field in self.fields.values():
#             field.widget.attrs["class"] = "form-control"

class ProfileForm(forms.ModelForm):
    new_password1 = forms.CharField(
        label="New Password",
        widget=forms.PasswordInput(attrs={"class": "form-control"}),
        required=False
    )
    new_password2 = forms.CharField(
        label="Confirm New Password",
        widget=forms.PasswordInput(attrs={"class": "form-control"}),
        required=False
    )

    class Meta:
        model = CustomUser
        fields = ("username", "email")

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for f in self.fields.values():
            f.widget.attrs.setdefault("class", "form-control")

    def clean(self):
        cleaned_data = super().clean()
        p1 = cleaned_data.get("new_password1")
        p2 = cleaned_data.get("new_password2")

        # If either password field is filled, validate both
        if p1 or p2:
            if p1 != p2:
                raise forms.ValidationError("Passwords do not match.")
            validate_password(p1)

        return cleaned_data

class AttendanceMarkForm(forms.Form):
    date = forms.DateField(initial=timezone.localdate, widget=forms.DateInput(attrs={"type": "date", "class": "form-control"}))
    program = forms.ChoiceField(choices=[], required=True, widget=forms.Select(attrs={"class":"form-select"}))
    batch = forms.ChoiceField(choices=[], required=True, widget=forms.Select(attrs={"class":"form-select"}))

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        programs = Student.objects.values_list("program", flat=True).distinct().order_by("program")
        batches = Student.objects.values_list("batch", flat=True).distinct().order_by("batch")

        self.fields["program"].choices = [(p, p) for p in programs]
        self.fields["batch"].choices = [(b, b) for b in batches]



class ReportBaseForm(forms.Form):
    program = forms.ChoiceField(choices=[], required=True, widget=forms.Select(attrs={"class":"form-select"}))
    batch = forms.ChoiceField(choices=[], required=True, widget=forms.Select(attrs={"class":"form-select"}))

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        programs = Student.objects.values_list("program", flat=True).distinct().order_by("program")
        batches = Student.objects.values_list("batch", flat=True).distinct().order_by("batch")

        self.fields["program"].choices = [(p, p) for p in programs]
        self.fields["batch"].choices = [(b, b) for b in batches]


class DailyReportForm(ReportBaseForm):
    date = forms.DateField(
        initial=timezone.localdate,
        widget=forms.DateInput(attrs={"type": "date", "class": "form-control"})
    )


class MonthlyReportForm(ReportBaseForm):
    month = forms.ChoiceField(choices=[], required=True, widget=forms.Select(attrs={"class":"form-select"}))
    year = forms.IntegerField(
        min_value=2000, max_value=2100,
        initial=timezone.localdate().year,
        widget=forms.NumberInput(attrs={"class": "form-control"})
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["month"].choices = [(i, calendar.month_name[i]) for i in range(1, 13)]
