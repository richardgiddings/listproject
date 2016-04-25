from django.test import TestCase, TransactionTestCase
from .models import Task, UserProfile
from django.core.urlresolvers import reverse
from django.utils import timezone
import pytz

class RegistrationViewTests(TestCase):

    """
    Test the Registration of users
    """

    def test_registration_initial(self):
        # Tests RegistrationView
        # Form shown to user
        response = self.client.get(reverse('todosite:register'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'todosite/registration.html')

    def test_registration_invalid(self):
        # Tests RegistrationView
        # Invalid data supplied (could test all form errors)
        response = self.client.post(
                reverse('todosite:register'),
                        data={'email': 'test@test.com', 
                              'password1': 'testpass10', 
                              'password2': 'testpass1', 
                              'timezone': 'UTC', 
                              'known_as': 'Test user'}
        )
        errors = response.context['form'].errors
        self.assertFormError(response, 'form', 'password2', 
                             'The two password fields didn\'t match.')
        #import ipdb; ipdb.set_trace()


    def test_registration_success(self):
        # Tests RegistrationView
        # User registered (try logging in too)
        response = self.client.post(
                reverse('todosite:register'),
                        data={'email': 'test@test.com', 
                              'password1': 'testpass10', 
                              'password2': 'testpass10', 
                              'timezone': 'UTC', 
                              'known_as': 'Test user'},
                        follow=True
        )
        self.assertRedirects(response, reverse('todosite:register'), 
                             status_code=302, target_status_code=200,
                             fetch_redirect_response=True)
        self.assertContains(response, 'User created.')
        self.assertEqual(UserProfile.objects.count(), 1)

        #import ipdb; ipdb.set_trace()

class AuthenticationViewTests(TestCase):

    """
    Test logging in/out of a user
    """    

    def test_login_view(self):
        # Shows login page
        response = self.client.get(reverse('todosite:login'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'todosite/login.html')
        self.assertContains(response, reverse('todosite:register'))

    def test_auth_view_success(self):
        # Directs to loggedin view
        # Create a task to display
        user = UserProfile.objects.create_user('test@test.com', 'testpass10', 
                                        timezone='UTC', known_as='Test user')
        user2 = UserProfile.objects.create_user('test2@test.com', 'test2pass10', 
                                        timezone='UTC', known_as='Test user 2')

        # Create a task to display and one for a user that shouldn't be
        Task.objects.create(task_title="Task title",
                            task_description="Task description",
                            belongs_to=user)
        Task.objects.create(task_title="Task title 2",
                            task_description="Task description 2",
                            belongs_to=user2)

        response = self.client.post(
                reverse('todosite:auth_view'),
                        data={'username': 'test@test.com', 
                              'password': 'testpass10'},
                        follow=True
        )
        self.assertRedirects(response, reverse('todosite:loggedin'), 
                             status_code=302, target_status_code=200,
                             fetch_redirect_response=True)
        self.assertContains(response, 'Task title')
        self.assertNotContains(response, 'Task title 2')

    def test_auth_view_failure(self):
        # Directs to invalid_login view
        user = UserProfile.objects.create_user('test@test.com', 'testpass10', 
                                        timezone='UTC', known_as='Test user')

        response = self.client.post(
                reverse('todosite:auth_view'),
                        data={'username': 'test@test.com', 
                              'password': 'invalid'},
                        follow=True
        )
        self.assertRedirects(response, reverse('todosite:invalid'), 
                             status_code=302, target_status_code=200,
                             fetch_redirect_response=True)
        self.assertTemplateUsed(response, 'todosite/invalid_login.html')

    def test_logout_view(self):
        # Shows logout page
        user = UserProfile.objects.create_user('test@test.com', 'testpass10', 
                                        timezone='UTC', known_as='Test user')

        response = self.client.post(
                reverse('todosite:auth_view'),
                        data={'username': 'test@test.com', 
                              'password': 'testpass10'},
                        follow=True
        )
        self.assertRedirects(response, reverse('todosite:loggedin'), 
                             status_code=302, target_status_code=200,
                             fetch_redirect_response=True)
        response = self.client.get(reverse('todosite:logout'))
        self.assertTemplateUsed(response, 'todosite/logout.html')

class TaskViewTests(TestCase):

    """
    Test the Add/Edit/Delete of tasks
    """

    def setUp(self):
        self.user = UserProfile.objects.create_user('test@test.com', 'testpass10', 
                                   timezone='Europe/London', known_as='Test user')
    
    def _login(self, username, password):
        self.client.logout()
        self.client.login(username=username, password=password)

    def _add_task(self, task_title, task_description, task_due, belongs_to):
        Task.objects.create(task_title=task_title,
                            task_description=task_description,
                            task_due=task_due,
                            belongs_to=belongs_to)

    def _add_second_user(self):
        return UserProfile.objects.create_user('test2@test.com', 'testpass101', 
                                timezone='Europe/London', known_as='Test user2')

    def test_add_a_task_initial(self):
        # Tests edit_view
        # Returns empty form to task page
        self._login('test@test.com', 'testpass10')

        response = self.client.get(reverse('todosite:add_task'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'todosite/task.html')

    def test_add_a_task_success(self):
        # Test edit_view POST
        # Check that we are redirected to loggedin with new task
        self._login('test@test.com', 'testpass10')

        response = self.client.post(
                reverse('todosite:add_task'),
                        data={'task_title': 'success', 
                              'task_description': 'description success',
                              'task_due': '2016-10-10 10:30'},
                        follow=True
        )
        self.assertEqual(Task.objects.count(), 1)
        self.assertQuerysetEqual(response.context['task_list'],['<Task: success>'])
        self.assertContains(response, 'description success')
 
    def test_add_a_task_cancel(self):
        # Tests edit_view POST
        # Check that we are returned to loggedin with NO new task
        self._login('test@test.com', 'testpass10')

        response = self.client.post(
                reverse('todosite:add_task'),
                        data={'cancel': 'Cancel'},
                        follow=True
        )
        self.assertEqual(Task.objects.count(), 0)
        self.assertContains(response, 'There are no tasks to display.')       

    def test_edit_a_task_initial(self):
        # Tests edit_view
        # Check that we are shown task to edit_view
        self._login('test@test.com', 'testpass10')
        now = timezone.now()
        self._add_task('Task title', 'Task description', 
                       now, self.user)
        task = Task.objects.first()

        response = self.client.get(reverse('todosite:edit_task',
                                   args=(task.id,)))       
        self.assertContains(response, 'Task title')
        self.assertContains(response, 'Task description')


    def test_edit_a_task_wrong_user(self):
        # Tests edit_view
        # Not allowed to edit, returned to loggedin
        user2 = self._add_second_user()
        self._add_task('Task title2', 'Task description2', 
                       timezone.now(), user2)
        task = Task.objects.first()

        self._login('test@test.com', 'testpass10')
        response = self.client.get(reverse('todosite:edit_task',
                                   args=(task.id,)))
        self.assertTemplateUsed(response, 'todosite/index.html')
        self.assertEqual(response.status_code, 200)  

    def test_edit_a_task_success(self):
        # Tests edit_view POST
        # Check that we are redirected to loggedin with edited task
        self._login('test@test.com', 'testpass10')
        self._add_task('Task title', 'Task description', 
                       timezone.now(), self.user)
        task = Task.objects.first()
        response = self.client.get(reverse('todosite:edit_task',
                                   args=(task.id,)))
        form = response.context['form']
        data = form.initial
        data['task_title'] = 'New title'
        data['task_due'] = '2016-01-10 10:32'

        response = self.client.post(reverse('todosite:edit_task', 
                                      kwargs={'task_id': task.id}), 
                                    data, follow=True)

        self.assertEqual(response.status_code, 200)
        self.assertQuerysetEqual(response.context['task_list'],['<Task: New title>'])

    def test_edit_a_task_cancel(self):
        # Tests edit_view POST
        # Check that we are returned to loggedin with task NOT edited
        self._login('test@test.com', 'testpass10')
        self._add_task('Task title', 'Task description', 
                       timezone.now(), self.user)
        task = Task.objects.first()
        response = self.client.get(reverse('todosite:edit_task',
                                   args=(task.id,)))
        form = response.context['form']
        data = form.initial
        data['task_title'] = 'New title'
        data['task_due'] = '2016-01-10 10:32'
        data['cancel'] = 'Cancel'

        response = self.client.post(reverse('todosite:edit_task', 
                                      kwargs={'task_id': task.id}), 
                                    data, follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertQuerysetEqual(response.context['task_list'],['<Task: Task title>'])

    def test_delete_a_task_initial(self):
        # Tests confirm delete screen shown
        self._login('test@test.com', 'testpass10')
        self._add_task('Task title', 'Task description', 
                       timezone.now(), self.user)
        task = Task.objects.first()

        response = self.client.get(reverse('todosite:delete_task', kwargs={'pk': task.id}))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'todosite/delete_task.html')

    def test_delete_a_task_cancel(self):
        # Tests TaskDelete
        # Returns to loggedin with task NOT deleted
        self._login('test@test.com', 'testpass10')
        self._add_task('Task title', 'Task description', 
                       timezone.now(), self.user)
        task = Task.objects.first()
        
        response = self.client.post(reverse('todosite:delete_task', 
                                    kwargs={'pk': task.id}), 
                                    data={'cancel': 'Cancel'}, follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertQuerysetEqual(response.context['task_list'],['<Task: Task title>'])

    def test_delete_a_task_wrong_user(self):
        # Tests TaskDelete
        # Returns to loggedin with task NOT deleted        
        user2 = self._add_second_user()
        self._add_task('Task title2', 'Task description2', 
                       timezone.now(), user2)
        task = Task.objects.first()

        self._login('test@test.com', 'testpass10')
        response = self.client.post(reverse('todosite:delete_task', 
                                    kwargs={'pk': task.id}), follow=True)
        self.assertTemplateUsed(response, 'todosite/index.html')
        self.assertEqual(response.status_code, 200)  
        self.assertEqual(Task.objects.count(), 1)

    def test_delete_a_task_success(self):
        # Tests TaskDelete
        # Returns to loggedin with task deleted
        self._login('test@test.com', 'testpass10')
        self._add_task('Task title', 'Task description', 
                       timezone.now(), self.user)
        task = Task.objects.first()

        self.assertEqual(Task.objects.count(), 1)
        response = self.client.post(reverse('todosite:delete_task', 
                                    kwargs={'pk': task.id}), follow=True)
        self.assertTemplateUsed(response, 'todosite/index.html')
        self.assertEqual(response.status_code, 200)  
        self.assertEqual(Task.objects.count(), 0)

