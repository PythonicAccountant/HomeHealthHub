from datetime import timedelta

import django_filters
from django.utils import timezone

from home_health_hub.users.models import User

from .models import FoodLogItem


class FoodLogItemFilter(django_filters.FilterSet):
    user__username = django_filters.ModelChoiceFilter(queryset=User.objects.all())
    weeks = django_filters.NumberFilter(
        field_name="date_eaten", method="get_past_n_weeks", label="Past n weeks"
    )

    def get_past_n_weeks(self, queryset, field_name, value):
        time_threshold = timezone.now() - timedelta(weeks=int(value))
        return queryset.filter(date_eaten__gte=time_threshold)

    class Meta:
        model = FoodLogItem
        fields = [
            "user__username",
        ]
