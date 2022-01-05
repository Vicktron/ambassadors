from django.contrib import admin
from django.contrib.auth import admin as auth_admin
from django.contrib.auth.forms import UserCreationForm, UserChangeForm

from .models import User, Account, Profile
from django.utils.translation import gettext_lazy as _

from .forms import RegistrationForm, UserForm


@admin.register(User)
class UserAdmin(auth_admin.UserAdmin):
    # form = UserChangeForm
    # add_form = RegistrationForm

    fieldsets = (
        (None, {"fields": ("email", "password")}),
        # (_("Personal info"), {"fields": ('email',)}),
        (
            _("Permissions"),
            {
                "fields": (
                    "is_active",
                ),
            },
        ),
        (_("Important dates"), {"fields": ("last_login", "date_joined")}),
    )
    list_display = ['email', ]
    list_display_links = ('email', )
    readonly_fields = ('last_login', 'date_joined')
    search_fields = ["email"]
    ordering = ['email']

    filter_horizontal = ()
    list_filter = ()


@admin.register(Account)
class ReferAdmin(admin.ModelAdmin):
    list_display = ("f_name", "l_name", "tel", "amt_wallet")
