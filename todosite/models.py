from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from django.forms import ModelForm
from django import forms

class Task(models.Model):
    """
    A class representing a task to do.
    """
 
    task_title = models.CharField(max_length=20,
                                  help_text="Maximum of 20 characters.")

    task_description = models.TextField(max_length=300,
                       help_text="Maximum of 300 characters.")

    task_due = models.DateTimeField('Date due', 
                                    default=timezone.now)

    belongs_to = models.ForeignKey(User)

    def __str__(self):
        return self.task_title

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