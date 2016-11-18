from django import forms


class LoginForm(forms.Form):

    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput)

class SignUpForm(forms.Form):

    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput)
    password_repeat = forms.CharField(widget=forms.PasswordInput)
    email = forms.EmailField(required=False)


class VideoResponseForm(forms.Form):
    docfile = forms.FileField(
        label='Select you video response file',
        help_text='but don\'t post nuttin stupid'
    )