from django.shortcuts import render, redirect
from django.urls import reverse
from django import views
from main.users.forms import SignUpForm


# def register(request):

#     form = SignUpForm()
#     if request.POST:
#         form = SignUpForm(request.POST)
#         if form.is_valid():
#             # username = request.POST.get("username")
#             # first_name = request.POST.get("first_name")
#             # last_name = request.POST.get("last_name")
#             # email = request.POST.get("email")
#             # password = request.POST.get("password")
#             # password2 = request.POST.get("password2")
#             # next_page = request.POST.get("next") or "/"

#             form.save()

class RegisterView(views.View):
    def get(self, request):
        return render(request, "registration/register.html", {"form": SignUpForm()})

    def post(self, request):
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()

            return redirect(reverse("users:login"))

        return render(request, "register.html", {"form": form})