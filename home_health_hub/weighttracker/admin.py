from django.contrib import admin

from .models import WeightLog, WeightProfile

admin.site.register(WeightProfile)


@admin.register(WeightLog)
class WeightAdmin(admin.ModelAdmin):
    model = WeightLog
    fields = (
        "user",
        "date",
        "weight",
        "trend",
        "var",
    )
    readonly_fields = (
        "var",
        "trend",
    )
