from django.forms import ModelForm

from .models import CalorieProfile, Food, FoodLogItem


class FoodLogForm(ModelForm):
    class Meta:
        model = FoodLogItem
        exclude = ("user",)


class FoodForm(ModelForm):
    class Meta:
        model = Food
        fields = "__all__"


class CalorieProfileForm(ModelForm):
    class Meta:
        model = CalorieProfile
        exclude = ("user",)
