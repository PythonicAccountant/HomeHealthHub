from django.contrib import admin

from .models import CalorieProfile, Food, FoodLogItem

admin.site.register(Food)
admin.site.register(CalorieProfile)
admin.site.register(FoodLogItem)
