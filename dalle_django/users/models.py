from django.contrib.auth.models import AbstractUser
from django.db.models import CharField
from django.db.models import IntegerField
from django.db.models import Model
from django.urls import reverse
from django.utils.translation import gettext_lazy as _


class User(AbstractUser):
    """
    Default custom user model for dalle-django.
    If adding fields that need to be filled at user signup,
    check forms.SignupForm and forms.SocialSignupForms accordingly.
    """

    # First and last name do not cover name patterns around the globe
    name = CharField(_("Name of User"), blank=True, max_length=255)
    first_name = None  # type: ignore[assignment]
    last_name = None  # type: ignore[assignment]

    def get_absolute_url(self) -> str:
        """Get URL for user's detail view.

        Returns:
            str: URL for user detail.

        """
        return reverse("users:detail", kwargs={"username": self.username})


class DalleParams(Model):
    name = None
    trees_amount = IntegerField(_("Tree amount"), blank=True, default=1)
    hangar_size = IntegerField(_("Hangar size"), blank=True, default=1)

    class Meta:
        verbose_name = _("DalleParams")
        verbose_name_plural = _("DalleParamss")

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse("DalleParams_detail", kwargs={"pk": self.pk})
