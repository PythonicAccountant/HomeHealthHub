from django.conf import settings
from django.db import models
from django.db.models import DecimalField, F, Sum
from django.db.models import Value as V
from django.db.models.functions import Coalesce


class Food(models.Model):
    class Meta:
        ordering = ["name"]

    UOM_GRAMS = "g"
    UOM_OZ = "oz"
    UOM_QTY = "qty"

    uom_choices = [(UOM_GRAMS, "grams"), (UOM_OZ, "ounces"), (UOM_QTY, "quantity")]

    name = models.CharField(max_length=255, unique=True)
    serving_unit = models.DecimalField(max_digits=5, decimal_places=1)
    uom = models.CharField("Unit of Measurement", max_length=10, choices=uom_choices)
    calories = models.DecimalField(max_digits=5, decimal_places=1)
    fat_grams = models.IntegerField(blank=True, null=True)
    protein_grams = models.IntegerField(blank=True, null=True)
    carb_grams = models.IntegerField(blank=True, null=True)

    def __str__(self):
        return self.name

    @property
    def calorie_per_serving_unit(self):
        return self.calories / self.serving_unit


class CalorieProfile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    daily_calorie_goal = models.IntegerField()

    def __str__(self):
        return f"{self.user} Profile"


class FoodLogQuerySet(models.QuerySet):
    def calorie_total_day(self):
        return self.annotate(
            total=Coalesce(
                Sum(
                    F("food_log_items__units_eaten")
                    * F("food_log_items__food__calories")
                    / F("food_log_items__food__serving_unit")
                ),
                V(0),
                output_field=DecimalField(),
            )
        ).order_by("-date")


class FoodLog(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    date = models.DateField()

    objects = FoodLogQuerySet.as_manager()

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["user", "date"], name="unique Foodlog per user"
            )
        ]

    def __str__(self):
        return f"{self.user} - {self.date}"

    @property
    def calorie_total(self):
        return (
            self.food_log_items.aggregate(
                total=Sum(
                    F("units_eaten") * F("food__calories") / F("food__serving_unit")
                )
            )["total"]
            or 0
        )

    def calorie_total_by_category(self):
        return (self.food_log_items.values("category").annotate(total=Sum(F("units_eaten") * F("food__calories") / F("food__serving_unit"))))

    @property
    def calories_remaining(self):
        return (
            self.food_log_items.aggregate(
                rem=Sum(
                    F("units_eaten") * F("food__calories") / F("food__serving_unit")
                )
            )["rem"]
            or 0
        )


class FoodLogItemQuerySet(models.QuerySet):
    def calorie_total_day(self, date, user):
        return (
            self.filter(date_eaten=date)
            .filter(user=user)
            .aggregate(
                total=Sum(
                    F("units_eaten") * F("food__calories") / F("food__serving_unit")
                )
            )
        )

    def distinct_qty(self):
        return (
            self.values("food__name", "food__id", "food__uom")
            .annotate(Sum("units_eaten"))
            .order_by("food__name")
        )


class FoodLogItem(models.Model):
    BREAKFAST = "1"
    LUNCH = "2"
    DINNER = "3"
    SNACK = "4"

    choices = [
        (BREAKFAST, "Breakfast"),
        (LUNCH, "Lunch"),
        (DINNER, "Dinner"),
        (SNACK, "Snack"),
    ]
    food_log = models.ForeignKey(
        FoodLog, on_delete=models.CASCADE, related_name="food_log_items"
    )
    food = models.ForeignKey(
        Food, on_delete=models.CASCADE, related_name="food_log_items"
    )
    units_eaten = models.DecimalField(decimal_places=1, max_digits=10)
    category = models.CharField(max_length=1, choices=choices, default=SNACK)

    objects = FoodLogItemQuerySet.as_manager()

    class Meta:
        ordering = ["category"]

    def __str__(self):
        return f"{self.food_log.user} - {self.food} - {self.food_log.date}"

    @property
    def calories_consumed(self):
        return self.units_eaten * self.food.calorie_per_serving_unit


class IntegrationProfile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    todoist_api_key = models.CharField(max_length=200, blank=True, null=True)
    todoist_target_project = models.CharField(max_length=200, blank=True, null=True)
