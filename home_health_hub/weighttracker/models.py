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


class WeightLogManager(models.Manager):
    def get_queryset(self):
        return WeightLogQuerySet(self.model, using=self._db)

    def get_or_create_days(self, user, year, month):
        no_days_in_month = calendar.monthrange(year, month)[1]
        logs = self.filter(user=user, date__year=year, date__month=month)
        if len(logs) == no_days_in_month:
            return logs
        else:
            date = datetime.date(year=year, month=month, day=1)
            days_in_month = [
                date.replace(day=day) for day in range(1, no_days_in_month + 1)
            ]
            self.bulk_create(
                [WeightLog(user=user, date=day) for day in days_in_month],
                ignore_conflicts=True,
            )
            logs = self.filter(user=user, date__year=year, date__month=month)
            return logs

    def for_user(self, user):
        return self.filter(user=user)

    def actual_entries(self):
        return self.filter(weight__isnull=False)

    # def weekly_loss(self, user):
    #     queryset = self.for_user(user).actual_entries().
    #     annotate(seven_days_ago=Subquery(self.filter(date=OuterRef("date") -
    #     datetime.timedelta(days=7)).values("weight")[:1])).annotate(weight_loss=F("weight") -
    #     F("seven_days_ago")).values("date", "weight_loss")
    #     return queryset

    def weekly_loss2(self, user):
        latest = self.for_user(user).actual_entries().latest()
        seven_days_ago = latest.date - datetime.timedelta(days=7)
        seven_days_ago_trend = (
            self.for_user(user)
            .actual_entries()
            .filter(date__lte=seven_days_ago)
            .latest()
            .trend
        )
        weight_loss = latest.trend - seven_days_ago_trend
        return weight_loss


class WeightLogQuerySet(models.QuerySet):
    def actual_entries(self):
        return self.filter(weight__isnull=False)


class WeightLog(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    date = models.DateField()
    weight = models.DecimalField(max_digits=10, decimal_places=1, blank=True, null=True)
    trend = models.DecimalField(max_digits=10, decimal_places=1, blank=True, null=True)

    objects = WeightLogManager()

    class Meta:
        get_latest_by = "date"
        ordering = ["date"]
        constraints = [
            models.UniqueConstraint(
                fields=["user", "date"], name="unique WeightLog per user"
            )
        ]

    def __str__(self):
        return f"{self.user} - {self.date}"

    def save(self, *args, **kwargs):
        latest_trend = WeightLog.objects.filter(
            user=self.user, date__lt=self.date, trend__isnull=False
        ).last()
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
