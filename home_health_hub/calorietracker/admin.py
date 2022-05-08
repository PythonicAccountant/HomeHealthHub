from django.contrib import admin

from .models import CalorieProfile, Food, FoodLog, FoodLogItem, IntegrationProfile

admin.site.register(Food)
admin.site.register(CalorieProfile)
admin.site.register(FoodLog)
admin.site.register(FoodLogItem)
admin.site.register(IntegrationProfile)
