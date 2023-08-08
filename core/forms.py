from django.contrib.auth.forms import BaseUserCreationForm, UserChangeForm
from .models import User


class CustomUserCreationForm(BaseUserCreationForm):
    class Meta(BaseUserCreationForm):
        model = User
        fields = BaseUserCreationForm.Meta.fields + ("email",)


class CustomUserChangeForm(UserChangeForm):

    class Meta(UserChangeForm):
        model = User
        fields = UserChangeForm.Meta.fields

