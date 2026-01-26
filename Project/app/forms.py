from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from .models import CustomUser, Student
from django.contrib.auth.password_validation import validate_password
from django.utils import timezone
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


# ModelForm used for Add & Update operations
class StudentForm(forms.ModelForm):
    class Meta:
        model = Student
        fields = ["student_id", "full_name", "email", "program", "batch"]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Apply Bootstrap class to each input
        for f in self.fields.values():
            f.widget.attrs["class"] = "form-control"
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
    date = forms.DateField(initial=timezone.localdate, widget=forms.DateInput(attrs={"type": "date"}))
    program = forms.ChoiceField(choices=[], required=True)
    batch = forms.ChoiceField(choices=[], required=True)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        programs = Student.objects.values_list("program", flat=True).distinct().order_by("program")
        batches = Student.objects.values_list("batch", flat=True).distinct().order_by("batch")

        self.fields["program"].choices = [(p, p) for p in programs]
        self.fields["batch"].choices = [(b, b) for b in batches]

class AttendanceMonthForm(forms.Form):
    program = forms.ChoiceField(choices=[], required=True)
    batch = forms.ChoiceField(choices=[], required=True)
    month = forms.ChoiceField(choices=[], required=True)
    year = forms.IntegerField(min_value=2000, max_value=2100, initial=timezone.localdate().year)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        programs = Student.objects.values_list("program", flat=True).distinct().order_by("program")
        batches = Student.objects.values_list("batch", flat=True).distinct().order_by("batch")

        self.fields["program"].choices = [(p, p) for p in programs]
        self.fields["batch"].choices = [(b, b) for b in batches]
        self.fields["month"].choices = [
            (i, calendar.month_name[i]) for i in range(1, 13)
        ]
