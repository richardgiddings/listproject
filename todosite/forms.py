from django.forms import ModelForm
from django import forms
from django.contrib.auth.forms import ReadOnlyPasswordHashField, UserCreationForm
from .models import Task, UserProfile
import pytz

class TaskForm(forms.ModelForm):
    """
    A form for a Task
    """
    class Meta:
        model = Task
        fields = ['task_title', 'task_description', 'task_due']
        widgets={
        'task_description': forms.Textarea(attrs={'cols': 30, 'rows': 10}),
        }

class UserRegistrationForm(UserCreationForm):
    """
    A form for creating a user
    """
    password1 = forms.CharField(label= 'Please enter a password', widget = forms.PasswordInput)
    password2 = forms.CharField(label= 'Please confirm password', widget = forms.PasswordInput)
    timezone = forms.ChoiceField(
        label='Time Zone',
        choices=[(t, t) for t in pytz.common_timezones]
    )

    class Meta:
        model = UserProfile
        fields = ['email', 'timezone', 'known_as',]

        def clean_password(self):
            password1 = self.cleaned_data['password1']
            password2 = self.cleaned_data['password2']
            if password1 and password2 and password1 != password2:
                raise forms.ValidationError('Passwords do no not match.')
            return password2

        def save(self, commit = True):
            user = super(UserRegistrationForm, self).save(commit = False)
            user.set_password(self.cleaned_data['password1'])
            user.save()
            return user

class UserChangeForm(forms.ModelForm):
    """
    A form for changing a user
    """
    password =  ReadOnlyPasswordHashField()
    timezone = forms.ChoiceField(
        label='Time Zone',
        choices=[(t, t) for t in pytz.common_timezones]
    )

    class Meta:
        model = UserProfile
        fields = ['email', 'timezone', 'known_as',]

    def clean_password(self):
        self.initial['password']