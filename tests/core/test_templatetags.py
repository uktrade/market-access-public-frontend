from django.template import Context, RequestContext, Template
from django.test import RequestFactory, SimpleTestCase

from apps.barriers.middleware import FiltersMiddleware


class QueryParamsTestCase(SimpleTestCase):
    def test_rendered_remove_filter(self):
        context = Context({"query_string": "resolved=0&location=dk"})
        expected_link = '<a href="https://wibble.com/?resolved=0">wobble</a>'
        template_to_render = Template(
            "{% load query_params %}"
            '<a href="https://wibble.com/{% remove_filter "location" %}">wobble</a>'
        )
        rendered_template = template_to_render.render(context)
        self.assertInHTML(expected_link, rendered_template)

    def test_rendered_remove_filter__nothing_to_remove(self):
        context = Context({"query_string": "resolved=0&location=dk"})
        expected_link = (
            '<a href="https://wibble.com/?resolved=0&location=dk">wobble</a>'
        )
        template_to_render = Template(
            "{% load query_params %}"
            '<a href="https://wibble.com/{% remove_filter "heyho" %}">wobble</a>'
        )
        rendered_template = template_to_render.render(context)
        self.assertInHTML(expected_link, rendered_template)

    def test_rendered_replace_filter(self):
        context = Context({"query_string": "resolved=0&location=dk"})
        expected_link = (
            '<a href="https://wibble.com/?location=dk&resolved=1">wobble</a>'
        )
        template_to_render = Template(
            "{% load query_params %}"
            '<a href="https://wibble.com/{% replace_filter "resolved" 1 %}">wobble</a>'
        )
        rendered_template = template_to_render.render(context)
        self.assertInHTML(expected_link, rendered_template)

    def test_rendered_replace_filter__nothing_to_replace(self):
        context = Context({"query_string": "resolved=0&location=dk"})
        expected_link = (
            '<a href="https://wibble.com/?resolved=0&location=dk">wobble</a>'
        )
        template_to_render = Template(
            "{% load query_params %}"
            '<a href="https://wibble.com/{% replace_filter "heyho" 0 %}">wobble</a>'
        )
        rendered_template = template_to_render.render(context)
        self.assertInHTML(expected_link, rendered_template)

    def test_rendered_current_path(self):
        rf = RequestFactory()
        get_request = rf.get("/hello/")
        middleware = FiltersMiddleware()
        middleware.process_request(get_request)
        context = RequestContext(get_request)
        expected_link = '<a href="/hello/">wobble</a>'
        template_to_render = Template(
            "{% load query_params %}" '<a href="{% current_path %}">wobble</a>'
        )

        rendered_template = template_to_render.render(context)
        self.assertInHTML(expected_link, rendered_template)

    def test_rendered_current_path_carriers_query_params(self):
        rf = RequestFactory()
        get_request = rf.get("/hello/?resolved=0&location=dk")
        middleware = FiltersMiddleware()
        middleware.process_request(get_request)
        context = RequestContext(get_request)
        expected_link = '<a href="/hello/?resolved=0&location=dk">wobble</a>'
        template_to_render = Template(
            "{% load query_params %}" '<a href="{% current_path %}">wobble</a>'
        )

        rendered_template = template_to_render.render(context)
        self.assertInHTML(expected_link, rendered_template)
