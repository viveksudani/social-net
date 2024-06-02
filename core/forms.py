from django.contrib.auth.forms import UserChangeForm, UserCreationForm
from core.models import User


class UserCreationForm(UserCreationForm):

    class Meta:
        model = User
        fields = "__all__"


class UserChangeForm(UserChangeForm):

    class Meta:
        model = User
        fields = "__all__"
