from django import forms
from django.conf import settings
from django.contrib.auth.forms import ReadOnlyPasswordHashField, AuthenticationForm
from django.core.exceptions import ValidationError
from django.core.mail import send_mail

from .models import CustomUser


class RegistrationForm(forms.ModelForm):
    password1 = forms.CharField(
        label="Password", widget=forms.PasswordInput(attrs={"placeholder": "min. 8 characters"})
    )
    password2 = forms.CharField(label="Confirm Password", widget=forms.PasswordInput)

    class Meta:
        model = CustomUser
        fields = ("email", "name", "password1", "password2")

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["name"].widget.attrs["placeholder"] = "min. 3 characters"

    def clean_name(self):
        name = self.cleaned_data.get("name")
        if name and len(name) < 3:
            raise ValidationError("Name too short.")
        return name

    def clean_password2(self):
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise ValidationError("Password missmatch.")
        if password1 == password2 and len(password2) < 8:
            raise ValidationError("Password too short.")
        return password2

    def clean_email(self):
        email = self.cleaned_data.get("email")
        if CustomUser.objects.filter(email=email).first():
            raise ValidationError("This email is registered already.")
        return email

    def save(self, commit=True):
        # Save the provided password in hashed format
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password2"])
        if commit:
            user.save()
        return user


class UserCreationForm(RegistrationForm):
    class Meta:
        model = CustomUser
        fields = ("email", "name", "is_staff", "is_superuser")


class UserChangeForm(forms.ModelForm):
    password = ReadOnlyPasswordHashField()

    class Meta:
        model = CustomUser
        fields = ("email", "name", "password", "is_active", "is_superuser")

    def clean_password(self):
        # Regardless of what the user provides, return the initial value.
        # This is done here, rather than on the field, because the
        # field does not have access to the initial value
        return self.initial["password"]


class SendRegistrationLink(forms.Form):
    email = forms.EmailField()

    def send_mail(self, to, subject, message, fail_silently):
        return send_mail(subject, message, settings.EMAIL_HOST_USER, to, fail_silently=fail_silently)


class LoginForm(AuthenticationForm):
    username = forms.EmailField(
        label="Email", required=False, widget=forms.TextInput(attrs={"name": "username", "placeholder": "Email"})
    )
    password = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        fields = ("username", "password")

    error_messages = {"invalid_login": "Wrong login data."}
