from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import redirect, render
from django.urls import reverse
from django.views.generic.edit import FormView

from users.forms import LoginForm, SendRegistrationLink, RegistrationForm
from users.models import Registration, CustomUser


class SendRegistrationLinkView(FormView):
    template_name = "users/send_registration_link.html"
    form_class = SendRegistrationLink
    success_url = "/user/link-sent/"

    def form_valid(self, form):
        if not (user := Registration.objects.filter(email=self.request.POST.get("email")).first()):
            user = Registration.objects.create(email=self.request.POST.get("email"))

        url = self.request.get_host() + self.request.get_full_path() + str(user.uuid)
        if CustomUser.objects.filter(email=user.email).first():
            msg = "Hello,\nYou are registered already."
            user.delete()
        else:
            msg = f"Hello,\nTo complete the registration use the link bellow.\n{url}"

        n = form.send_mail(to=(user.email,), subject="Registration link", message=msg, fail_silently=True)
        if n == 0:
            user.delete()
            self.request.session["email"] = "invalid"
            return self.form_invalid(form)

        self.request.session["email"] = user.email
        return super().form_valid(form)


class RegisterUserView(FormView):
    template_name = "users/register_user.html"
    form_class = RegistrationForm
    success_url = "/user/login/"

    def get_initial(self):
        """
        Returns the initial data to use for forms on this view.
        """
        user = Registration.objects.get(uuid=self.kwargs["uuid"])
        initial = super().get_initial()
        initial["email"] = user.email
        return initial

    def get_form_class(self):
        form = super().get_form_class()
        form.base_fields["email"].disabled = True
        return form

    def form_valid(self, form):
        form.save(uuid=self.kwargs["uuid"])
        return super().form_valid(form)


def login_view(request):
    if request.method == "POST":
        form = LoginForm(request, request.POST)

        if form.is_valid():
            username = form.cleaned_data.get("username")
            password = form.cleaned_data.get("password")

            if user := authenticate(email=username, password=password) is not None:
                if user.is_active:
                    login(request, user)
                    messages.add_message(request, messages.SUCCESS, f"You are logged in. Hello {username}")
                    return redirect(reverse("home:home"))
    else:
        form = LoginForm()
    return render(request, "users/login.html", {"form": form})


def logout_view(request):
    logout(request)
    return redirect(reverse("home:home"))
