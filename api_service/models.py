from django.db import models
from django.contrib.auth.models import AbstractBaseUser
from django.contrib.auth.base_user import BaseUserManager
from django.utils.translation import gettext_lazy as _
from django.utils import timezone

class CustomUserManager(BaseUserManager):
    """
    Defines how the User(or the model to which attached)
    will create users and superusers.
    """
    def create_user(
        self,
        email, 
        password,
        **extra_fields
        ):
        """
        Create and save a user with the given email, password,
        and date_of_birth.
        """
        if not email:
            raise ValueError(_("The Email must be set"))
        email = self.normalize_email(email) # lowercase the domain
        user = self.model(
            email=email,
            **extra_fields
        )
        user.set_password(password) # hash raw password and set
        user.save()
        return user
    def create_superuser(
        self,
        email, 
        password,
        **extra_fields
        ):
        """
        Create and save a superuser with the given email, 
        password, and date_of_birth. Extra fields are added
        to indicate that the user is staff, active, and indeed
        a superuser.
        """
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        extra_fields.setdefault("is_active", True)
        extra_fields.setdefault("department", "AD")
        extra_fields.setdefault("user_type", "ADMIN")
        if extra_fields.get("is_staff") is not True:
            raise ValueError(
                _("Superuser must have is_staff=True.")
            )
        if extra_fields.get("is_superuser") is not True:
            raise ValueError(
                _("Superuser must have is_superuser=True.")
            )
        return self.create_user(
            email, 
            password, 
            **extra_fields
        )

# Create your models here.
class CustomUser(AbstractBaseUser):
    DEPARTMENT_LIST = {
        "HR":"Human Resources",
        "IT":"Information Technology",
        "AD":"Admin",
        "MS":"Marketing/Sales"
    }
    USER_TYPE_LIST={
        "ADMIN": "Admin user",
        "USER": "User"
    }
    user_name = models.CharField(max_length=255,null=True)
    email = models.EmailField(_('email address'),unique=True)
    department = models.CharField(max_length=5,choices=DEPARTMENT_LIST, null=False)
    salary = models.DecimalField(max_digits=10,decimal_places=2,default=0)
    country = models.CharField(max_length=255,null=True)
    user_type = models.CharField(max_length=10,default='USER')
    is_active = models.BooleanField(default=True)
    is_superuser = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=True)
    created_at = models.DateTimeField(default=timezone.now)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = CustomUserManager()
    def __str__(self):
        return self.email