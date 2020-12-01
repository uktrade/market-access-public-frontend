from django.db import models


class HealthCheck(models.Model):
    health_check_field = models.BooleanField(null=False, default=True)

    def __str__(self):
        return "%s" % self.health_check_field

    def __repr__(self):
        return "<%s - %s>" % (self.__class__.__name__, self.health_check_field)
