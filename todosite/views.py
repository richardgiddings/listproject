from django.shortcuts import render_to_response
from django.shortcuts import get_object_or_404
from django.http import HttpResponseRedirect
from django.template import RequestContext
from django.core.urlresolvers import reverse
from django.contrib import auth
from django.template.context_processors import csrf
from .models import Task, UserProfile
from .forms import TaskForm, UserRegistrationForm
from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.views.generic.edit import DeleteView
from django.views.generic import CreateView
from django.core.urlresolvers import reverse_lazy
from django.contrib.messages.views import SuccessMessageMixin

def login(request):
    """
    The login page
    """
    c = {}
    c.update(csrf(request))

    return render_to_response('todosite/login.html', c)


def auth_view(request):
    """
    Deal with a login request
    """
    username = request.POST.get('username', '')
    password = request.POST.get('password', '')
    user = auth.authenticate(email=username, password=password)

    if user is not None:
        auth.login(request, user)
        return HttpResponseRedirect(reverse('todosite:loggedin'))
    else:
   	    return HttpResponseRedirect(reverse('todosite:invalid'))


def logout(request):
    """
    Deal with a logout request
    """
    auth.logout(request)
    return render_to_response('todosite/logout.html')


@login_required
def loggedin(request):
    """
    The main page seen when logged in
    """
    request.session['django_timezone'] = request.user.timezone

    task_list = Task.objects.order_by('task_due')
    task_list = task_list.filter(belongs_to=request.user)

    return render_to_response('todosite/index.html',
    	                      {'full_name': request.user.known_as,
                               'task_list': task_list})


def invalid_login(request): 
    """
    An invalid login attempt
    """
    return render_to_response('todosite/invalid_login.html')


@login_required
def edit_task(request, task_id=None, template_name='todosite/task.html'):
    """
    Screen for adding/editing a task
    """
    if "cancel" in request.POST:
        return loggedin(request)
    if task_id:
        task = get_object_or_404(Task, pk=task_id)
        if task.belongs_to != request.user:
            return loggedin(request)
    else:
        task = Task(belongs_to=request.user)

    form = TaskForm(request.POST or None, instance=task)
    if request.POST:
        if form.is_valid():
            form.save()
            return loggedin(request)

    return render_to_response(template_name, {
        'form': form,
    }, context_instance=RequestContext(request))


class TaskDelete(DeleteView):
    """
    Delete a task
    """
    model = Task
    success_url = reverse_lazy('todosite:loggedin')
    template_name = 'todosite/delete_task.html'

    @method_decorator(login_required)
    def post(self, request, *args, **kwargs):

        if "cancel" in request.POST:
            return loggedin(request)
        else:
            # check we are deleting for the correct user
            self.object = self.get_object()
            if self.object.belongs_to != request.user:
                return loggedin(request)
            return super(TaskDelete, self).post(request, *args, **kwargs)


class RegistrationView(SuccessMessageMixin, CreateView):
    """
    User registration
    """
    form_class = UserRegistrationForm
    template_name = 'todosite/registration.html'
    success_url = reverse_lazy('todosite:register')
    success_message = 'User created.'

