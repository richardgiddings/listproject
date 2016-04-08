from django.forms import ModelForm
from django import forms
from django.contrib.auth.forms import ReadOnlyPasswordHashField, UserCreationForm
from .models import Task, UserProfile
import pytz
from bootstrap3_datetime.widgets import DateTimePicker

class TaskForm(forms.ModelForm):
    """
    A form for a Task
    """
    class Meta:
        model = Task
        fields = ['task_title', 'task_description', 'task_due']
        widgets={
        'task_title':
        forms.TextInput(attrs = {'placeholder': 'Give the task a name here.'}),
        'task_description':
        forms.Textarea(attrs={'placeholder': 'Describe the task here.'}),
        'task_due':
        DateTimePicker(options={"format": "YYYY-MM-DD HH:mm"})
        }

    def __init__(self, *args, **kwargs):
        super(TaskForm, self).__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'

class UserRegistrationForm(UserCreationForm):
    """
    A form for creating a user
    """
    password1 = forms.CharField(label= 'Please enter a password', 
        widget = forms.PasswordInput(
                attrs = {'placeholder': 'Choose a password.'}))
    password2 = forms.CharField(label= 'Please confirm your password', 
        widget = forms.PasswordInput(
                attrs = {'placeholder': 'Enter your password again.'}))
    timezone = forms.ChoiceField(
        label='Time zone',
        choices=[(t, t) for t in pytz.common_timezones]
    )

    class Meta:
        model = UserProfile
        fields = ['email', 'known_as', 'timezone',]
        widgets={
        'email':
        forms.EmailInput(attrs = {'placeholder': 'Your email address.'}),
        'known_as':
        forms.TextInput(attrs = {'placeholder': 'How you want to be greeted.'}),
        }

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

    def __init__(self, *args, **kwargs):
        super(UserRegistrationForm, self).__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'

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
        fields = ['email', 'known_as', 'timezone',]

    def clean_password(self):
        self.initial['password']

    def __init__(self, *args, **kwargs):
        super(UserChangeForm, self).__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'