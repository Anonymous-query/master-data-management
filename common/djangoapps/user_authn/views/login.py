import json
import logging

from django.conf import settings
from django.contrib.auth import authenticate, get_user_model
from django.contrib.auth import login as django_login
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect
from django.urls import reverse
from django.utils.decorators import method_decorator
from django.utils.translation import gettext as _
from django.views.decorators.csrf import csrf_exempt, csrf_protect, ensure_csrf_cookie
from common.djangoapps.user_authn.exceptions import AuthFailedError, VulnerablePasswordError
from django_ratelimit.decorators import ratelimit
from django.views.decorators.http import require_http_methods
from rest_framework.views import APIView
from django.http import JsonResponse
from common.djangoapps.user_authn.cookies import set_logged_in_cookies


log = logging.getLogger(__name__)
AUDIT_LOG = logging.getLogger("audit")
USER_MODEL = get_user_model()

def _get_user_by_email(email):
    """
    Finds a user object in the database based on the given email, ignores all fields except for email.
    """
    try:
        return USER_MODEL.objects.get(email=email)
    except USER_MODEL.DoesNotExist:
        return None
    
def _get_user_by_username(username):
    """
    Finds a user object in the database based on the given username.
    """
    try:
        return USER_MODEL.objects.get(username=username)
    except USER_MODEL.DoesNotExist:
        return None
    
def _log_and_raise_inactive_user_auth_error(unauthenticated_user):
    AUDIT_LOG.warning(
        f"Login failed - Account not active for user.id: {unauthenticated_user.id}, resending activation"
    )

    raise AuthFailedError(
        error_code='inactive-user',
        context={
            'platformName': settings.PLATFORM_NAME
        }
    )

def _authenticate_user(request, unauthenticated_user):
    """
    Use Django authentication on the given request, using rate limiting if configured
    """
    should_be_rate_limited = getattr(request, 'limited', False)
    if should_be_rate_limited:
        raise AuthFailedError(_('Too many failed login attempts. Try again later.'))  # lint-amnesty, pylint: disable=raise-missing-from

    username = unauthenticated_user.username if unauthenticated_user else ""

    password = request.POST['password']
    return authenticate(
        username=username,
        password=password,
        request=request
    )

def _handle_failed_authentication(user, authenticated_user):
    """
    Handles updating the failed login count, inactive user notifications, and logging failed authentications.
    """
    failure_count = 0
    if user:
        if authenticated_user and not user.is_active:
             _log_and_raise_inactive_user_auth_error(user)

        loggable_id = user.id if user else "<unknown>"
        AUDIT_LOG.warning(f"Login failed - password for user.id: {loggable_id} is invalid")

    raise AuthFailedError(
        _('Username or password is incorrect.'),
        error_code='Login failed',
        context={'failure_count': failure_count},
    )

def _handle_successful_authentication_and_login(user, request):
    try:
        django_login(request, user)
        request.session.set_expiry(604800 * 4)
        log.debug("Setting user session expiry to 4 weeks")
    except Exception as exc:
        AUDIT_LOG.critical("Login failed - Could not create session")
        log.critical("Login failed - Could not create session")
        log.exception(exc)
        raise

@ensure_csrf_cookie
@require_http_methods(['POST'])
@ratelimit(
    key='common.djangoapps.util.ratelimit.request_post_username',
    rate=settings.LOGISTRATION_PER_USERNAME_RATELIMIT_RATE,
    method='POST',
    block=False,
)
def login_user(request):
    possibly_authenticated_user = None
    try:
        username = request.POST.get('username', None)
        user = _get_user_by_username(username)
        possibly_authenticated_user = user
        possibly_authenticated_user = _authenticate_user(request, user)
        if possibly_authenticated_user is None or not possibly_authenticated_user.is_active:
            _handle_failed_authentication(user, possibly_authenticated_user)

        _handle_successful_authentication_and_login(possibly_authenticated_user, request)

        redirect_url = '/dashboard'
        response = JsonResponse({
            'success': True,
            'redirect_url': redirect_url,
        })

        response = set_logged_in_cookies(request, response, possibly_authenticated_user)
        return response
    except AuthFailedError as error:
        response_content = error.get_response()
        log.exception(response_content)

        username = request.POST.get('username', None)
        username = possibly_authenticated_user.email if possibly_authenticated_user else username
        response_content['username'] = username
    except VulnerablePasswordError as error:
        response_content = error.get_response()
        log.exception(response_content)

    response = JsonResponse(response_content, status=400)
    return response

class LoginSessionView(APIView):
    """HTTP end-points for logging in users. """

    # This end-point is available to anonymous users,
    # so do not require authentication.
    authentication_classes = []

    @method_decorator(csrf_protect)
    def post(self, request):
        return login_user(request)
    
def dashboard(request):
    return JsonResponse({})