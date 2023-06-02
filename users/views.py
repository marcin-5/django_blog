from django.db import IntegrityError
from django.http import HttpResponseRedirect
from django.views.generic.edit import FormView

from users.forms import SendRegistrationLink, RegistrationForm
from users.models import Registration


class SendRegistrationLinkView(FormView):
    template_name = "users/send_registration_link.html"
    form_class = SendRegistrationLink
    success_url = "/user/send-registration-link/done/"

    def form_valid(self, form):
        try:
            user = Registration.objects.create(email=self.request.POST.get("email"))
        except IntegrityError:
            user = Registration.objects.get(email=self.request.POST.get("email"))
        url = self.request.get_host() + self.request.get_full_path() + str(user.uuid)
        msg = f"Hello,\nTo complete the registration use the link bellow.\n{url}"
        form.send_mail(to=(user.email,),
                       subject="Registration link",
                       message=msg)
        self.request.session["email"] = user.email
        return super().form_valid(form)


class RegisterUserView(FormView):
    template_name = "users/register_user.html"
    form_class = RegistrationForm
    success_url = ""

    def form_valid(self, form):
        return super().form_valid(form)
