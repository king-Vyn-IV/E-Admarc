# accounts/forms.py
from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

class UserRegisterForm(UserCreationForm):
    email = forms.EmailField(
        required=True,
        widget=forms.EmailInput(attrs={
            'class': 'form-control rounded-pill',
            'placeholder': 'Enter your email'
        })
    )

    is_staff = forms.BooleanField(
        required=False,
        label="Staff User",
        widget=forms.CheckboxInput(attrs={'class': 'form-check-input'})
    )

    is_superuser = forms.BooleanField(
        required=False,
        label="Superuser",
        widget=forms.CheckboxInput(attrs={'class': 'form-check-input'})
    )

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2', 'is_staff', 'is_superuser']
        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-control rounded-pill', 'placeholder': 'Enter username'}),
            'password1': forms.PasswordInput(attrs={'class': 'form-control rounded-pill', 'placeholder': 'Enter password'}),
            'password2': forms.PasswordInput(attrs={'class': 'form-control rounded-pill', 'placeholder': 'Confirm password'}),
        }

    def __init__(self, *args, **kwargs):
        current_user = kwargs.pop('current_user', None)
        super().__init__(*args, **kwargs)

        # Hide admin fields if current user isn't a superuser
        if not current_user or not current_user.is_superuser:
            self.fields.pop('is_staff')
            self.fields.pop('is_superuser')

    def save(self, commit=True):
        user = super().save(commit=False)
        password = self.cleaned_data.get('password1')
        if password:
            user.set_password(password)
        if commit:
            user.save()
        return user
