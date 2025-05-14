from django.contrib.auth.forms import UserChangeForm, UserCreationForm

from apps.users.models import UserAccount


class UserAccountCreationForm(UserCreationForm):
    class Meta:
        model = UserAccount
        fields = ("email",)


class UserAccountChangeForm(UserChangeForm):
    class Meta:
        model = UserAccount
        fields = ("email",)
