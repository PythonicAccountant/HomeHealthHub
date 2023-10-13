import calendar
import datetime
import decimal

from django.conf import settings
from django.db import models


class WeightProfile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    goal_weight = models.IntegerField()
    height = models.IntegerField()
    estimated_tdee = models.IntegerField()

    def __str__(self):
        return f"{self.user} Weight Profile"


class WeightLog(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    date = models.DateField()
    weight = models.DecimalField(max_digits=10, decimal_places=1)
    trend = models.DecimalField(max_digits=10, decimal_places=1, blank=True)

    class Meta:
        get_latest_by = "date"
        constraints = [
            models.UniqueConstraint(
                fields=["user", "date"], name="unique WeightLog per user"
            )
        ]

    def __str__(self):
        return f"{self.user} - {self.date}"

    def save(self, *args, **kwargs):
        latest_trend = WeightLog.objects.filter(
            user=self.user, date__lt=self.date
        ).first()
        if latest_trend:
            latest_trend = latest_trend.trend
            self.trend = (self.weight - latest_trend) * decimal.Decimal(
                0.3636
            ) + latest_trend
        else:
            self.trend = self.weight
        super(WeightLog, self).save(*args, **kwargs)

    @property
    def var(self):
        """Returns the difference(variation) between the weight entry and the trend"""
        if self.weight:
            return self.weight - self.trend
        else:
            return 0

    @staticmethod
    def get_days(month, year):
        date = datetime.datetime(year=year, month=month, day=1)
        days = calendar.monthrange(date.year, date.month)[1]
        return [date.replace(day=day) for day in range(1, days + 1)]
