from django.http import HttpResponse


PINGDOM_TEMPLATE = """<?xml version="1.0" encoding="UTF-8"?>
<pingdom_http_custom_check>
    <status>{status}</status>
</pingdom_http_custom_check>\n"""

COMMENT_TEMPLATE = "<!--{comment}-->\n"


def pingdom(request):
    checked = {}

    if all(item[0] for item in checked.values()):
        return HttpResponse(
            PINGDOM_TEMPLATE.format(status="OK"), content_type="text/xml"
        )
    else:
        body = PINGDOM_TEMPLATE.format(status="FALSE")
        for service_result in filter(lambda x: x[0] is False, checked.values()):
            body += COMMENT_TEMPLATE.format(comment=service_result[1])
        return HttpResponse(body, status=500, content_type="text/xml")
