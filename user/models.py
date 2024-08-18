from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.translation import gettext_lazy as _
from phonenumber_field.modelfields import PhoneNumberField


class User(AbstractUser):
    email = models.EmailField(verbose_name=_("Email Address"), unique=True)
    username = models.CharField(
        verbose_name=_("Username"),
        max_length=150,
        help_text=_("Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only."),
    )
    full_name = models.CharField(
        verbose_name=_("Full Name"), max_length=512, null=True, blank=True, help_text=_("Full name is auto generated.")
    )

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["username"]

    def get_full_name(self):
        return " ".join([name for name in [self.first_name, self.last_name] if name]) or self.email

    def save(self, *args, **kwargs):
        self.full_name = self.get_full_name()
        return super().save(*args, **kwargs)


class Profile(models.Model):
    class UserType(models.IntegerChoices):
        ADMIN = 1000, _("Admin")
        CUSTOMER = 100, _("Customer")

    user = models.OneToOneField(
        User, on_delete=models.CASCADE, verbose_name=_("User"), help_text=_("User whom profile belongs")
    )
    user_type = models.IntegerField(verbose_name=_("User Type"), choices=UserType.choices, help_text=_("User user type"))
    phone_number = PhoneNumberField(region="NP")

    def __str__(self):
        return f"{self.user.username} - {self.get_user_type_display()}"
