from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.password_validation import validate_password
from django.core import validators


class Register(forms.Form):
    first_name = forms.CharField(label="First Name", widget=forms.TextInput(
        attrs={"id": "fname", "class": "form-control", "placeholder": "First name"}))
    last_name = forms.CharField(label="Last Name", widget=forms.TextInput(
        attrs={"id": "lname", "class": "form-control", "placeholder": "Last name"}))
    username = forms.CharField(label="Username", widget=forms.TextInput(
        attrs={"id": "username", "class": "form-control", "placeholder": "Username"}))
    email = forms.EmailField(label="Email Address", widget=forms.EmailInput(
        attrs={"id": "email", "class": "form-control", "placeholder": "Email Address",
               "aria-describedby": "emailHelp"}))
    password = forms.CharField(label="Password", widget=forms.PasswordInput(
        attrs={"id": "password", "class": "form-control", "placeholder": "Password"}), validators=[validate_password])
    cpassword = forms.CharField(label="Password", widget=forms.PasswordInput(
        attrs={"id": "cpassword", "class": "form-control", "placeholder": "Confirm Password"}))

    def clean(self):
        cd = self.cleaned_data
        if cd.get('password') != cd.get('cpassword'):
            self.add_error('cpassword', 'Both the passwords should match')
        try:
            existingUserName = User.objects.get(username=cd['username'])
        except User.DoesNotExist:
            existingUserName = None

        if existingUserName is not None:
            self.add_error('username', 'This username already exists, please choose another one')

        try:
            existingEmail = User.objects.get(email=cd['email'])
        except User.DoesNotExist:
            existingEmail = None
        if existingEmail is not None:
            self.add_error('email', 'An account with this email address already exists')


class Login(forms.Form):
    username = forms.CharField(label="Username", widget=forms.TextInput(
        attrs={"id": "username", "class": "form-control", "placeholder": "Username"}))
    password = forms.CharField(label="Password", widget=forms.PasswordInput(
        attrs={"id": "password", "class": "form-control", "placeholder": "Password"}))

class newThread(forms.Form):
    title = forms.CharField(label="Title", widget=forms.TextInput(
        attrs={"id": "title", "class": "form-control", "placeholder": "Title"}))
    content = forms.CharField(label="Content", widget=forms.Textarea(
        attrs={"id": "content", "class": "form-control", "placeholder": "Content", "rows": "3"}))


class commentForm(forms.Form):
    commentText = forms.CharField(label="Add a comment", widget=forms.TextInput(
        attrs={"id": "commentText", "class": "form-control", "placeholder": "Add a comment"}))

class forgotPassword(forms.Form):
    email = forms.EmailField(label="Email Address" , widget=forms.EmailInput(
        attrs={"id":"email","class":"form-control","placeholder":"Enter email address"}
    ))