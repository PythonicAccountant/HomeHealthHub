from django import forms
from django.forms import DateInput, HiddenInput, ModelForm

from .models import AccessoryLift, Cycle, Workout


class DateInput(DateInput):
    input_type = "date"


class WorkoutForm(ModelForm):
    class Meta:
        model = Workout
        fields = ["amrap_reps", "date_completed", "id"]
        widgets = {"date_completed": DateInput(), "id": HiddenInput()}


class StartNextForm(forms.Form):
    cycle_end = forms.DateField(widget=DateInput())
    new_cycle_name = forms.CharField(max_length=200)


class CycleForm(ModelForm):
    class Meta:
        model = Cycle
        fields = "__all__"
        widgets = {
            "cycle_start": DateInput(),
            "cycle_end": DateInput(),
        }


class AccessoryLiftForm(ModelForm):
    class Meta:
        model = AccessoryLift
        fields = "__all__"
