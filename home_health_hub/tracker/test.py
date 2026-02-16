week1 = {1: {0.4: 5}, 2: {0.5: 5}}

# for sets, value in week1.items():
#     for percent, reps in value.items():
#         print(sets, percent, reps)


class instance:
    def __init__(self):
        self.squat_max = 100
        self.bench_max = 150
        self.deadlift_max = 150
        self.ohp_max = 200


instance = instance()

lifts = {
    "S": instance.squat_max,
    "B": instance.bench_max,
    "D": instance.deadlift_max,
    "O": instance.ohp_max,
}

for lift, maxx in lifts.items():
    print(lift, maxx)
