from django.forms import ModelForm

from .models import WeightLog


class WeightLogForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super(WeightLogForm, self).__init__(*args, **kwargs)
        self.fields["date"].disabled = True
        self.fields["trend"].disabled = True

    class Meta:
        model = WeightLog
        fields = [
            "date",
            "weight",
            "trend",
        ]
