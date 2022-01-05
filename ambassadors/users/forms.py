from django import forms
from django.contrib.auth.forms import UserCreationForm

from .models import Account, Profile, User


class UserForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput(attrs={
        'placeholder': 'Enter password'
    }))
    confirm_password = forms.CharField(widget=forms.PasswordInput(attrs={
        'placeholder': 'Confirm password'
    }))

    class Meta:
        model = User
        fields = ['email']

    def __init__(self, *args, **kwargs):
        super(UserForm, self).__init__(*args, **kwargs)
        self.fields['email'].widget.attrs['placeholder'] = 'ambassador@agromatic.io'


class RegistrationForm(forms.ModelForm):
    class Meta:
        model = Account
        fields = ['f_name', 'l_name', 'tel', 'amt_staked', 'amt_wallet', 'usd_staked']

    def __init__(self, *args, **kwargs):
        super(RegistrationForm, self).__init__(*args, **kwargs)
        self.fields['f_name'].widget.attrs['placeholder'] = 'Agro'
        self.fields['l_name'].widget.attrs['placeholder'] = 'Matician'
        self.fields['tel'].widget.attrs['placeholder'] = '08012345678'
        self.fields['amt_wallet'].widget.attrs['placeholder'] = '0x000000000000000000000000000'
        self.fields['amt_staked'].widget.attrs['placeholder'] = '$AMT'
        self.fields['usd_staked'].widget.attrs['placeholder'] = '$USD'

        # for field in self.fields:
        #     self.fields[field].widget.attrs['class'] = 'form-control'

    def clean(self):
        cleaned_data = super(RegistrationForm, self).clean()
        password = cleaned_data.get('password')
        confirm_password = cleaned_data.get('confirm_password')

        if password != confirm_password:
            raise forms.ValidationError('Password does not match!')


class LoginForm(forms.Form):
    email = forms.CharField(
        widget=forms.EmailInput(
            attrs={
                "placeholder": "Email",
                "class": "form-control"
            }
        ))
    password = forms.CharField(
        widget=forms.PasswordInput(
            attrs={
                "placeholder": "Password",
                "class": "form-control"
            }
        ))


# class UserForm(forms.ModelForm):
#     class Meta:
#         model = Account
#         fields = ('f_name', 'l_name', 'email', 'tel')
#
#     def __init__(self, *args, **kwargs):
#         super(UserForm, self).__init__(*args, **kwargs)
#         for field in self.fields:
#             self.fields[field].widget.attrs['class'] = 'form-control'


class UserProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ('address', 'city', 'state', 'country')

    def __init__(self, *args, **kwargs):
        super(UserProfileForm, self).__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs['class'] = 'form-control'
