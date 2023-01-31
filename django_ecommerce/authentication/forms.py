from django import forms
from django.core.exceptions import ValidationError
from authentication.models import User

class SignupForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ('name', 'email', 'phone_number')
    def clean(self):
        cleaned_data = super(SignupForm, self).clean()
        return cleaned_data


class OtpForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ('otp',)

    def clean(self):
        cleaned_data = super(OtpForm, self).clean()
        return cleaned_data
