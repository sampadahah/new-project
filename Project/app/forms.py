from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from .models import CustomUser, Student
from django.contrib.auth.password_validation import validate_password


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