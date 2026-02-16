from django.contrib import admin

from .models import AccessoryLift, AccessoryLog, Cycle, Set, Workout

# Register your models here.

admin.site.register(Workout)
admin.site.register(Cycle)
admin.site.register(Set)
admin.site.register(AccessoryLift)
admin.site.register(AccessoryLog)
