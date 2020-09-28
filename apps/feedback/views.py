from django.urls import reverse_lazy
from django.views.generic import FormView, TemplateView

from .forms import FeedbackSplashForm, FeedbackTypes, FeedbackUsabilityForm, FeedbackIssueForm


class FeedbackSplashView(FormView):
    template_name = "feedback/splash.html"
    form_class = FeedbackSplashForm
    extra_context = {"title": "Help us improve our service"}
    success_url = reverse_lazy("feedback:splash")
    success_url_mapping = {
        str(FeedbackTypes.USABILITY): reverse_lazy("feedback:usability"),
        str(FeedbackTypes.ISSUE): reverse_lazy("feedback:issue"),
        str(FeedbackTypes.BARRIER): reverse_lazy("feedback:barrier"),
    }

    def form_valid(self, form):
        feedback_type = form.cleaned_data["feedback_type"]
        self.success_url = self.success_url_mapping.get(feedback_type)
        return super().form_valid(form)


class FeedbackBarrierView(TemplateView):
    template_name = "feedback/barrier.html"
    extra_context = {
        "title": "Report a trade barrier or an issue with an existing trade barrier"
    }


class FeedbackIssueView(FormView):
    template_name = "feedback/issue.html"
    form_class = FeedbackIssueForm
    extra_context = {"title": "A technical issue with this service"}
    success_url = reverse_lazy("feedback:thank-you")

    def form_valid(self, form):
        # TODO: call the Forms API
        return super().form_valid(form)


class FeedbackUsabilityView(FormView):
    template_name = "feedback/usability.html"
    form_class = FeedbackUsabilityForm
    extra_context = {"title": "Feedback on the use of this service"}
    success_url = reverse_lazy("feedback:thank-you")

    def form_valid(self, form):
        # TODO: call the Forms API
        return super().form_valid(form)


class FeedbackThankYouView(TemplateView):
    template_name = "feedback/thank-you.html"
    extra_context = {"title": "Thank you for your feedback"}
