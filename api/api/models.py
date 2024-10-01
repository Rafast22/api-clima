from django.db import models
from rest_framework.authtoken.models import Token
from django.contrib.auth.models import AbstractUser
from pygments.lexers import get_all_lexers
from pygments.styles import get_all_styles
from django.contrib.auth.models import User, Group, Permission
from  django.utils import timezone
from django.contrib.auth.validators import UnicodeUsernameValidator
from django.utils.translation import gettext_lazy as _

LEXERS = [item for item in get_all_lexers() if item[1]]
LANGUAGE_CHOICES = sorted([(item[1][0], item[0]) for item in LEXERS])
STYLE_CHOICES = sorted([(item, item) for item in get_all_styles()])


class User(AbstractUser):
    username_validator = UnicodeUsernameValidator()

    ROLE_CHOICES = (
        ('administrator', 'Administrator'),
        ('staff', 'Staff'),
        ('user', 'User'),
    )
     
    username = models.CharField(
        _("username"),
        max_length=150,
        unique=True,
        help_text=_(
            "Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only."
        ),
        validators=[username_validator],
        error_messages={
            "unique": _("A user with that username already exists."),
        },
    )
    first_name = models.CharField(_("first name"), max_length=150, blank=True)
    last_name = models.CharField(_("last name"), max_length=150, blank=True)
    email = models.EmailField(_("email address"), blank=True)
    is_staff = models.BooleanField(
        _("staff status"),
        default=False,
        help_text=_("Designates whether the user can log into this admin site."),
    )
    is_active = models.BooleanField(
        _("active"),
        default=True,
        help_text=_(
            "Designates whether this user should be treated as active. "
            "Unselect this instead of deleting accounts."
        ),
    )
    date_joined = models.DateTimeField(_("date joined"), default=timezone.now)

    role = models.CharField(max_length=15, choices=ROLE_CHOICES, null=False, default="user")
    # date_joined =  models.DateTimeField(auto_now_add=True)
    last_login =  models.DateTimeField( auto_now=True)
    
    # groups = models.ManyToManyField( Group, related_name='custom_user_set' )

    # user_permissions = models.ManyToManyField(Permission, related_name='custom_user_set')
    class Meta(AbstractUser.Meta):
        swappable = "AUTH_USER_MODEL"
        ordering = ['date_joined']
    
        

