from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path
from django.views import defaults as default_views

from apps.pingdom.urls import urlpatterns as pingdom_urlpatterns

urlpatterns = []

if settings.DEBUG:
    # This allows the error pages to be debugged during development, just visit
    # these url in browser to see how these error pages look like.
    urlpatterns += [
        path(
            "400/",
            default_views.bad_request,
            kwargs={"exception": Exception("Bad Request!")},
        ),
        path(
            "403/",
            default_views.permission_denied,
            kwargs={"exception": Exception("Permission Denied")},
        ),
        path(
            "404/",
            default_views.page_not_found,
            kwargs={"exception": Exception("Page not Found")},
        ),
        path("500/", default_views.server_error),
    ]

    if settings.DJANGO_ENV == "local":
        urlpatterns += [
            path("admin/", admin.site.urls),
        ]

    # If debug toolbar is installed
    if "debug_toolbar" in settings.INSTALLED_APPS:
        import debug_toolbar

        urlpatterns = [path("__debug__/", include(debug_toolbar.urls))] + urlpatterns

    # Expose static
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

urlpatterns += [
    path("", include("apps.barriers.urls", namespace="barriers")),
    path("", include("apps.core.urls", namespace="core")),
    path("", include("apps.feedback.urls", namespace="feedback")),
    path("", include("apps.healthcheck.urls", namespace="healthcheck")),
] + pingdom_urlpatterns
