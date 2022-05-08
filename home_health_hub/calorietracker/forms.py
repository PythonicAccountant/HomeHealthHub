import datetime
from datetime import time

from django.forms import ModelForm

from .models import CalorieProfile, Food, FoodLogItem


class FoodLogForm(ModelForm):
    class Meta:
        model = FoodLogItem
        exclude = ("food_log",)

    @staticmethod
    def get_initial_for_category():
        breakfast_begin = time(hour=6)
        breakfast_end = time(hour=11)
        lunch_begin = time(hour=11, minute=1)
        lunch_end = time(hour=14)
        time_now = datetime.datetime.now().time()

        if breakfast_begin <= time_now <= breakfast_end:
            return {"category": FoodLogItem.BREAKFAST}
        elif lunch_begin <= time_now <= lunch_end:
            return {"category": FoodLogItem.LUNCH}
        else:
            return {"category": FoodLogItem.SNACK}


class FoodForm(ModelForm):
    class Meta:
        model = Food
        fields = "__all__"


class CalorieProfileForm(ModelForm):
    class Meta:
        model = CalorieProfile
        exclude = ("user",)
