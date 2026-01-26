from django.shortcuts import render, redirect
from django.contrib.auth import login, logout
from .forms import SignUpForm, LoginForm, ProfileForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth import update_session_auth_hash
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


# def login_view(request):
#     if request.method == "POST":
#         form = LoginForm(request, data=request.POST)
#         if form.is_valid():
#             login(request, form.get_user())
#             return redirect("home")
#     else:
#         form = LoginForm()
#     return render(request, "login.html", {"form": form})
def login_view(request):
    if request.method == "POST":
        form = LoginForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)

            if user.is_superuser:
                return redirect("admin_dashboard")

            # Normal users
            return redirect("home")
    else:
        form = LoginForm()

    return render(request, "login.html", {"form": form})
def logout_view(request):
    logout(request)
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