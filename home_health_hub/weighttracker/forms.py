from django.forms import ModelForm

from .models import WeightLog, WeightProfile


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


class WeightLogNonTableForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super(WeightLogNonTableForm, self).__init__(*args, **kwargs)
        self.fields["date"].disabled = True

    class Meta:
        model = WeightLog
        fields = [
            "date",
            "weight",
        ]


class WeightProfileForm(ModelForm):
    class Meta:
        model = WeightProfile
        exclude = ("user",)
