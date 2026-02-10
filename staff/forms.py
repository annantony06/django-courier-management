# staff/forms.py
from django import forms
from django.contrib.auth.forms import AuthenticationForm

class StaffLoginForm(AuthenticationForm):
    class Meta:
        model = AuthenticationForm
        fields = ['username', 'password']