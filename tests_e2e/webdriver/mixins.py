import base64

from .. import settings


class NavigationMixin:
    """ To be used with WebDrivers """

    def navigate(self, path="/"):
        """ Helper to add basic auth to requests """
        if settings.AUTH_SECRET:
            creds = f"auth_user:{settings.AUTH_SECRET}"
            encoded_creds = base64.b64encode(creds.encode("utf-8")).decode("utf-8")
            self.driver.header_overrides = {
                "Authorization": f"Basic {encoded_creds}",
            }
        url = f"{settings.BASE_URL.rstrip('/')}/{path.lstrip('/')}"
        self.driver.get(url)
