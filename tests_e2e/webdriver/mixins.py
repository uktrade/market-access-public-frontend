from .. import settings


class NavigationMixin:
    """ To be used with WebDrivers """

    def navigate(self, path="/"):
        """ Helper to add basic auth to requests """
        base = settings.BASE_URL.rstrip("/")
        if settings.AUTH_SECRET:
            base = base.replace("://", f"://auth_user:{settings.AUTH_SECRET}@")
        url = f"{base}/{path.lstrip('/')}"
        self.visit(url)
