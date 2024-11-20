from django import forms
from .models import User42
from django.contrib.auth.forms import UserCreationForm, PasswordChangeForm


# class changePasswordForm(PasswordChangeForm):
#     pass
#     # fields = [
#     #     'old_password',
#     #     'new_password1',
#     #     'new_password1',
#     # ]

class ChangePasswordForm(forms.Form):
    old_password = forms.CharField(widget=forms.PasswordInput())
    new_password = forms.CharField(widget=forms.PasswordInput())
    confirm_password = forms.CharField(widget=forms.PasswordInput())


class UserUpdateForm(forms.ModelForm):
    description = forms.CharField(required=False)
    image = forms.ImageField(required=True)

    class Meta:
        model = User42
        fields = [
            'username',
            'description',
            'image',
            'language',
        ]


class UserForm(UserCreationForm):

    class Meta:
        model = User42
        fields = [
            'username',
            'email',
            'password1',
            'password2',
            'language',
        ]
