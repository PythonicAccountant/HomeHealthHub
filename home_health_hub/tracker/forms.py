from django import forms
from django.forms import DateInput, HiddenInput, ModelForm
from django.utils import timezone

from .models import AccessoryLift, Cycle, Workout


class DateInput(DateInput):
    input_type = "date"


class WorkoutForm(ModelForm):
    date_completed = forms.DateField(
        widget=DateInput(), initial=lambda: timezone.now().date()
    )

    class Meta:
        model = Workout
        fields = ["amrap_reps", "date_completed", "id"]
        widgets = {"id": HiddenInput()}


class StartNextForm(forms.Form):
    cycle_end = forms.DateField(
        widget=DateInput(), initial=lambda: timezone.now().date()
    )
    new_cycle_name = forms.CharField(max_length=200)


class CycleForm(ModelForm):
    cycle_start = forms.DateField(
        widget=DateInput(), initial=lambda: timezone.now().date()
    )

    class Meta:
        model = Cycle
        fields = "__all__"
        widgets = {
            "cycle_end": DateInput(),
        }


class AccessoryLiftForm(ModelForm):
    class Meta:
        model = AccessoryLift
        fields = "__all__"
