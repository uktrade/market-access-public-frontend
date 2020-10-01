from django import forms


class FeedbackTypes:
    USABILITY = 1
    ISSUE = 2
    BARRIER = 3

    @classmethod
    def choices(cls):
        return (
            (
                cls.USABILITY,
                {
                    "label": "Feedback on the use of this service",
                    "hint": "For example, does it meet your expectations?",
                },
            ),
            (
                cls.ISSUE,
                {
                    "label": "A technical issue with this service",
                    "hint": "For example, functionality that isn’t working.",
                },
            ),
            (
                cls.BARRIER,
                {
                    "label": "Report a trade barrier "
                             "or an issue with an existing trade barrier",
                    "hint": "For example, do you have an issue with "
                            "a published trade barrier or want to report "
                            "a trade barrier that is not in the service.",
                },
            ),
        )


class FeedbackSplashForm(forms.Form):
    feedback_type = forms.ChoiceField(
        choices=FeedbackTypes.choices, label="Feedback or issues"
    )


class FeelingTypes:
    VERY_DISSATISFIED = 1
    DISSATISFIED = 2
    NEITHER = 3
    SATISFIED = 4
    VERY_SATISFIED = 5

    @classmethod
    def choices(cls):
        return (
            (cls.VERY_SATISFIED, {"label": "Very satisfied"}),
            (cls.SATISFIED, {"label": "Satisfied"}),
            (cls.NEITHER, {"label": "Neither satisfied or dissatisfied"}),
            (cls.DISSATISFIED, {"label": "Dissatisfied"}),
            (cls.VERY_DISSATISFIED, {"label": "Very dissatisfied"}),
        )


class FeedbackUsabilityForm(forms.Form):
    feeling_type = forms.ChoiceField(
        choices=FeelingTypes.choices,
        label="How would you rate the quality of the service?",
    )
    suggestions = forms.CharField(
        widget=forms.Textarea,
        label="How can we improve this service?",
        help_text="Do not include personal or financial information, "
                  "like your National Insurance number or credit card details.",
        max_length=1200,
        required=False
    )


class FeedbackIssueForm(forms.Form):
    expectations = forms.CharField(
        widget=forms.Textarea,
        label="What did you expect to happen?",
        help_text="Do not include personal or financial information, "
                  "like your National Insurance number or credit card details.",
        max_length=1200
    )
    outcome = forms.CharField(
        widget=forms.Textarea,
        label="What went wrong?",
        help_text="Do not include personal or financial information, "
                  "like your National Insurance number or credit card details.",
        max_length=1200
    )
