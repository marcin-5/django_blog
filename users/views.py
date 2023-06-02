from django.db import IntegrityError
from django.views.generic.edit import FormView

from users.forms import SendRegistrationLink, RegistrationForm
from users.models import Registration, CustomUser


class SendRegistrationLinkView(FormView):
    template_name = "users/send_registration_link.html"
    form_class = SendRegistrationLink
    success_url = "/user/send-registration-link/done/"

    def form_valid(self, form):
        if not (user := Registration.objects.filter(email=self.request.POST.get("email")).first()):
            user = Registration.objects.create(email=self.request.POST.get("email"))

        url = self.request.get_host() + self.request.get_full_path() + str(user.uuid)
        if CustomUser.objects.filter(email=user.email).first():
            msg = "Hello,\nYou are registered already."
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
    success_url = ""

    def form_valid(self, form):
        return super().form_valid(form)
