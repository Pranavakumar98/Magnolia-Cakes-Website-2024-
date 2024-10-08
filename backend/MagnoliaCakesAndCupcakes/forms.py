from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.core.validators import validate_email
from django.core.exceptions import ValidationError
import os

from MagnoliaCakesAndCupcakes.models import Quote


class NewUserForm(UserCreationForm):
    first_name = forms.CharField(max_length=30, required=True)
    last_name = forms.CharField(max_length=30, required=True)
    customer_id = forms.IntegerField(required=False, initial=None)

    class Meta:
        model = User
        fields = ("username", "first_name", "last_name", "password1", "password2")

    def clean_username(self):
        # Custom validation to check if the username (email) is already in use.
        username = self.cleaned_data.get("username")
        # Check if the username (email) is already used as an email address.
        if User.objects.filter(email=username).exists():
            raise forms.ValidationError("This email address is already in use.")
            # Django's built-in EmailValidator:
        try:
            validate_email(username)
        # For some reason my
        except forms.ValidationError:
            raise forms.ValidationError("Please enter a valid email address.")

        return username

    def save(self, commit=True):
        user = super(NewUserForm, self).save(commit=False)
        user.email = self.cleaned_data["username"]
        user.first_name = self.cleaned_data["first_name"]
        user.last_name = self.cleaned_data["last_name"]

        if commit:
            user.save()
        return user


class MultipleFileInput(forms.ClearableFileInput):
    allow_multiple_selected = True

'''
#previous implementation of file upload 
class MultipleFileField(forms.FileField):
    def __init__(self, *args, **kwargs):
        kwargs.setdefault("widget", MultipleFileInput())
        super().__init__(*args, **kwargs)

    def clean(self, data, initial=None):
        single_file_clean = super().clean
        if isinstance(data, (list, tuple)):
            result = [single_file_clean(d, initial) for d in data]
        else:
            result = single_file_clean(data, initial)
        return result


class ContactForm(forms.Form):
    email = forms.CharField(required=True)
    subject = forms.CharField(required=True)
    message = forms.CharField(widget=forms.Textarea, required=True)
    file = MultipleFileField(required=False)
'''

class MultipleFileField(forms.FileField):
    def __init__(self, *args, **kwargs):
        kwargs.setdefault("widget", MultipleFileInput())
        super().__init__(*args, **kwargs)

    def clean(self, data, initial=None):
        single_file_clean = super().clean
        if isinstance(data, (list, tuple)):
            result = []
            for d in data:
                cleaned_file = single_file_clean(d, initial)
                self.validate_file(cleaned_file)
                result.append(cleaned_file)
        else:
            result = single_file_clean(data, initial)
            self.validate_file(result)
        return result

    def validate_file(self, file):
        if file:
            # Define allowed file types
            allowed_types = [
                'image/jpeg', 'image/png', 
                'text/plain', 'application/vnd.openxmlformats-officedocument.wordprocessingml.document', 'text/csv',
                'application/pdf'
            ]
            allowed_extensions = ['.jpg', '.jpeg', '.png', '.txt', '.docx', '.csv', '.pdf']

            file_extension = os.path.splitext(file.name)[1].lower()
            if file.content_type not in allowed_types and file_extension not in allowed_extensions:
                raise ValidationError('Invalid file type. Allowed types are: PNG, JPEG, JPG, TXT, DOCX, CSV, and PDF.')

class ContactForm(forms.Form):
    email = forms.EmailField(required=True)
    subject = forms.CharField(required=True)
    message = forms.CharField(widget=forms.Textarea, required=True)
    file = MultipleFileField(required=False)

# ... (keep other classes as they are)
class FlavourServingsForm(forms.Form):
    title = forms.CharField(max_length=100)
    list = forms.Textarea()



