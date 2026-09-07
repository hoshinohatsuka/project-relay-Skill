SESSION_COOKIE_NAME = "fixture_session"


def authenticate(request):
    """Fixture: authentication uses a server-side session, not JWT."""
    return request.cookies.get(SESSION_COOKIE_NAME)
