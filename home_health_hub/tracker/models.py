from django.core.exceptions import ValidationError
from django.db import models


class Cycle(models.Model):
    cycle_name = models.CharField(max_length=200)
    cycle_start = models.DateField("Cycle Start Date")
    cycle_end = models.DateField("Cycle End Date", blank=True, null=True)
    squat_max = models.IntegerField()
    bench_max = models.IntegerField()
    deadlift_max = models.IntegerField()
    ohp_max = models.IntegerField()

    def __str__(self):
        return self.cycle_name

    def clean(self, *args, **kwargs):
        if (
            Cycle.objects.filter(cycle_end__isnull=True).count() > 0
            and self.cycle_end is None
            and Cycle.objects.get(cycle_end__isnull=True) != self
        ):
            raise ValidationError("Can only have 1 active cycle")
        super(Cycle, self).clean(*args, **kwargs)

    def save(self, *args, **kwargs):
        self.full_clean()
        super(Cycle, self).save(*args, **kwargs)

    @staticmethod
    def current_active_cycle():
        if Cycle.objects.filter(cycle_end__isnull=True).count() > 0:
            return Cycle.objects.get(cycle_end__isnull=True)
        else:
            return Cycle.objects.latest("cycle_end")


class Workout(models.Model):
    LIFT_CHOICES = [("S", "Squat"), ("B", "Bench"), ("D", "Deadlift"), ("O", "OHP")]
    cycle = models.ForeignKey(Cycle, on_delete=models.CASCADE, related_name="cycles")
    week = models.IntegerField()
    lift = models.CharField(max_length=1, choices=LIFT_CHOICES)
    amrap_reps = models.IntegerField(blank=True, null=True)
    date_completed = models.DateField(blank=True, null=True)
    estimated_1rm = models.IntegerField(blank=True, null=True)

    def __str__(self):
        return f"{self.cycle} - Week {self.week} - {self.get_lift_display()}"


class Set(models.Model):
    class Meta:
        ordering = [
            "set_number",
        ]

    workout = models.ForeignKey(Workout, on_delete=models.CASCADE, related_name="sets")
    set_number = models.IntegerField()
    weight = models.DecimalField(decimal_places=1, max_digits=20)
    reps = models.IntegerField(null=True, blank=True)

    def __str__(self):
        return f"Set {self.set_number} - {self.workout}"

    @property
    def plates_viz(self):
        weight_set = [45, 25, 10, 5, 2.5]
        plate_weight = float(self.weight) - 45

        if plate_weight <= 0:
            return "Bar Only"

        representation = [0 for _ in weight_set]
        weight_needed_on_one_side = plate_weight / 2
        for i, plate in enumerate(weight_set):
            if plate <= weight_needed_on_one_side:
                multiplier = weight_needed_on_one_side // plate
                representation[i] = multiplier
                weight_needed_on_one_side -= multiplier * plate

        if weight_needed_on_one_side > 0:
            return "no good answer found"

        string_print = []

        for plate, count in zip(weight_set, representation):
            for x in range(int(count)):
                string_print.append(plate)

        return string_print


class AccessoryLift(models.Model):
    lift = models.CharField(max_length=200)
    body_part_group = models.CharField(max_length=200)

    def __str__(self):
        return self.lift


class AccessoryLog(models.Model):
    workout = models.ForeignKey(
        Workout, on_delete=models.CASCADE, related_name="accessories"
    )
    accessory_lift = models.ForeignKey(
        AccessoryLift, on_delete=models.CASCADE, related_name="accessory_lift"
    )
    weight = models.DecimalField(decimal_places=1, max_digits=20)
    sets = models.IntegerField()
    reps = models.IntegerField(null=True, blank=True)
