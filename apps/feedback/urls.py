from django.urls import path

from .views import (FeedbackBarrierView, FeedbackIssueView, FeedbackSplashView,
                    FeedbackThankYouView, FeedbackUsabilityView)

app_name = "feedback"

urlpatterns = [
    path("feedback/", FeedbackSplashView.as_view(), name="splash"),
    path("feedback/barrier/", FeedbackBarrierView.as_view(), name="barrier"),
    path("feedback/issue/", FeedbackIssueView.as_view(), name="issue"),
    path("feedback/usability/", FeedbackUsabilityView.as_view(), name="usability"),
    path("feedback/thank-you/", FeedbackThankYouView.as_view(), name="thank-you"),
]
