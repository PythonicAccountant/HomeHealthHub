from django.conf import settings
from django.db import models
from django.db.models import F, Sum


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
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    food = models.ForeignKey(
        Food, on_delete=models.CASCADE, related_name="food_log_items"
    )
    units_eaten = models.DecimalField(decimal_places=1, max_digits=10)
    date_eaten = models.DateField(auto_now_add=True)
    category = models.CharField(max_length=1, choices=choices, default=SNACK)

    objects = FoodLogQuerySet.as_manager()

    def __str__(self):
        return f"{self.user} - {self.food} - {self.date_eaten}"

    @property
    def calories_consumed(self):
        return self.units_eaten * self.food.calorie_per_serving_unit
