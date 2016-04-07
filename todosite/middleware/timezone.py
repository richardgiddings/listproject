import pytz

from django.utils import timezone

class TimezoneMiddleware(object):
    """
    Set the correct timezone based on the user profile
    """
    def process_request(self, request):
        tzname = request.session.get('django_timezone')
        if tzname:
            timezone.activate(pytz.timezone(request.user.timezone))
        else:
            timezone.deactivate()