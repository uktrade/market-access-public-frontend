class BreadCrumbsMixin:
    """
    Helper mixin to help adding breadcrumbs to a Django view.
    Breadcrumbs should be a list of tuples (title, url)
    Example:
        breadcrumbs = (
            ("Cookies", reverse_lazy("core:cookies")),
        )
    """
    breadcrumbs = ()

    def get_breadcrumbs(self):
        return self.breadcrumbs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["breadcrumbs"] = self.get_breadcrumbs()
        return context
