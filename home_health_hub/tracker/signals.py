import decimal

from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver

from home_health_hub.tracker.models import Cycle, Set, Workout


def myround(x, base=5):
    return int(base * round(float(x) / base))


@receiver(post_save, sender=Cycle)
def create_workouts(sender, instance, created, **kwargs):
    # {Week : {Set: {Percent of Max: Reps at this weight}}
    workout = {
        1: {
            1: {0.4: 5},
            2: {0.5: 5},
            3: {0.6: 3},
            4: {0.65: 5},
            5: {0.75: 5},
            6: {0.85: None},
        },
        2: {
            1: {0.4: 5},
            2: {0.5: 5},
            3: {0.6: 3},
            4: {0.7: 3},
            5: {0.8: 3},
            6: {0.9: None},
        },
        3: {
            1: {0.4: 5},
            2: {0.5: 5},
            3: {0.6: 5},
            4: {0.75: 5},
            5: {0.85: 3},
            6: {0.95: None},
        },
        4: {1: {0.4: 5}, 2: {0.5: 5}, 3: {0.6: 5}},
    }
    lifts = {
        "S": instance.squat_max,
        "B": instance.bench_max,
        "D": instance.deadlift_max,
        "O": instance.ohp_max,
    }
    if created:
        for lift, maxx in lifts.items():
            for week, weeks in workout.items():
                Workout.objects.create(cycle=instance, week=week, lift=lift)


@receiver(post_save, sender=Workout)
def create_sets(sender, instance, created, **kwargs):
    workout = {
        1: {
            1: {0.4: 5},
            2: {0.5: 5},
            3: {0.6: 3},
            4: {0.65: 5},
            5: {0.75: 5},
            6: {0.85: None},
        },
        2: {
            1: {0.4: 5},
            2: {0.5: 5},
            3: {0.6: 3},
            4: {0.7: 3},
            5: {0.8: 3},
            6: {0.9: None},
        },
        3: {
            1: {0.4: 5},
            2: {0.5: 5},
            3: {0.6: 5},
            4: {0.75: 5},
            5: {0.85: 3},
            6: {0.95: None},
        },
        4: {1: {0.4: 5}, 2: {0.5: 5}, 3: {0.6: 5}},
    }
    cycle = instance.cycle
    maxes = {
        "S": cycle.squat_max,
        "B": cycle.bench_max,
        "D": cycle.deadlift_max,
        "O": cycle.ohp_max,
    }
    # if instance.amrap_reps:
    try:
        sixth_set = Set.objects.get(workout=instance, set_number=6)
        sixth_set.reps = instance.amrap_reps
        sixth_set.save()

    except Set.DoesNotExist:
        pass

    if created:
        set_info = workout[instance.week]
        weight_info = maxes[instance.lift]
        for sets, value in set_info.items():
            for percent, reps in value.items():
                weight = myround(weight_info * percent)
                if weight <= 45:
                    weight = 45
                Set.objects.create(
                    workout=instance, set_number=sets, weight=weight, reps=reps
                )


@receiver(pre_save, sender=Workout)
def update_1rm(sender, instance, **kwargs):
    if instance.amrap_reps is None and instance.estimated_1rm:
        instance.estimated_1rm = None

    if instance.amrap_reps:
        sixth_set = Set.objects.get(workout=instance, set_number=6)
        instance.estimated_1rm = myround(
            sixth_set.weight * instance.amrap_reps * decimal.Decimal(0.0333)
            + sixth_set.weight
        )
