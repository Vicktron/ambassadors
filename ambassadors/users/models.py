from django.contrib.auth.base_user import BaseUserManager, AbstractBaseUser
from django.contrib.auth.models import AbstractUser

from config.settings import base as settings
from .utils import generate_ref_code
from django.db import models


class UserManager(BaseUserManager):
    def create_user(self, email, f_name, l_name, password=None, is_admin=False, is_staff=False,
                    is_active=True):
        if not email:
            raise ValueError("User must have an email")
        if not password:
            raise ValueError("User must have a password")
        if not f_name:
            raise ValueError("User must have a first name")
        if not l_name:
            raise ValueError("User must have a first name")

        user = self.model(
            email=self.normalize_email(email)
        )
        user.f_name = f_name
        user.l_name = l_name
        user.set_password(password)  # change password to hash
        user.admin = is_admin
        user.staff = is_staff
        user.active = is_active
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError("User must have an email")
        if not password:
            raise ValueError("User must have a password")

        user = self.model(
            email=self.normalize_email(email)
        )
        user.set_password(password)
        user.admin = True
        user.staff = True
        user.active = True
        user.save(using=self._db)
        return user


class User(AbstractBaseUser):
    email = models.EmailField(max_length=100, unique=True)
    is_active = models.BooleanField(default=True)
    staff = models.BooleanField(default=False)  # a admin user; non super-user
    admin = models.BooleanField(default=False)  # a superuser
    date_joined = models.DateTimeField(auto_now_add=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    def __str__(self):
        return f"{self.email}"

    def has_perm(self, perm, obj=None):
        "Does the user have a specific permission?"
        # Simplest possible answer: Yes, always
        return True

    def has_module_perms(self, app_label):
        """Does the user have permissions to view the app `app_label`?"""
        # Simplest possible answer: Yes, always
        return True

    @property
    def is_staff(self):
        """Is the user a member of staff?"""
        return self.staff

    @property
    def is_admin(self):
        """Is the user a admin member?"""
        return self.admin

    objects = UserManager()


class Account(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='ambassador')
    f_name = models.CharField(max_length=50)
    l_name = models.CharField(max_length=50)
    amt_wallet = models.CharField(max_length=100)
    amt_staked = models.PositiveIntegerField(default=0)
    usd_staked = models.PositiveIntegerField(default=0)
    is_leader = models.BooleanField(default=False)
    is_regional = models.BooleanField(default=False)
    is_national = models.BooleanField(default=False)
    tel = models.CharField(max_length=50, blank=True)
    bio = models.TextField(blank=True)
    code = models.CharField(max_length=12, blank=True)
    recommended_by = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True, related_name='ref_by')
    updated = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)

    # USERNAME_FIELD = 'email'
    # REQUIRED_FIELDS = ['f_name', 'l_name', 'tel']

    def fullname(self):
        return f"{self.f_name} {self.l_name}"

    def __str__(self):
        return f"{self.f_name} {self.l_name}"

    def get_recommended_profiles(self):
        qs = Account.objects.all()
        # my_recs =[p for p in qs if p.recommended_by == self.user]
        my_recs = []
        for profile in qs:
            if profile.recommended_by == self.user:
                my_recs.append(profile)
        return my_recs

    def save(self, *args, **kwargs):
        if self.code == "":
            code = generate_ref_code()
            self.code = code
        super().save(*args, **kwargs)


class Profile(models.Model):
    user = models.OneToOneField(Account, on_delete=models.CASCADE)
    address = models.CharField(max_length=100, blank=True)
    profile_picture = models.ImageField(null=True, blank=True)
    city = models.CharField(max_length=100, blank=True)
    state = models.CharField(max_length=100, blank=True)
    country = models.CharField(max_length=100, blank=True)

    def __str__(self):
        return self.user.user.get_full_name()

    def fulllocation(self):
        return f"{self.city}, {self.state}, {self.country}"
