from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, render
from django.urls import reverse, reverse_lazy
from django.views.generic import ListView, View
from django.views.generic.edit import CreateView, DeleteView, UpdateView

from .forms import AccessoryLiftForm, CycleForm, StartNextForm, WorkoutForm
from .models import AccessoryLift, AccessoryLog, Cycle, Workout


@login_required
def tracker(request):
    try:
        max_cycle = Cycle.current_active_cycle()
        workout_list = Workout.objects.filter(cycle=max_cycle).order_by("id")
        context = {"workout_list": workout_list, "form": WorkoutForm}
        return render(request, "tracker/tracker.html", context)
    except Cycle.DoesNotExist:
        return HttpResponseRedirect(reverse("tracker:cycles"))


@login_required
def cycles(request):
    cycles_list = Cycle.objects.all().order_by("-cycle_end")
    context = {"cycle_list": cycles_list, "form": StartNextForm}
    return render(request, "tracker/cycles.html", context)


@login_required
def view_archive(request, pk):
    max_cycle = Cycle.objects.get(id=pk)
    workout_list = Workout.objects.filter(cycle=max_cycle)
    context = {"workout_list": workout_list, "form": WorkoutForm}
    return render(request, "tracker/tracker.html", context)


@login_required
def workout_update(request, pk):
    if request.method == "POST":
        workout = Workout.objects.get(id=pk)
        form = WorkoutForm(request.POST, instance=workout)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse("tracker:tracker"))


@login_required
def start_next(request):
    if request.method == "POST":
        form = StartNextForm(request.POST)
        max_cycle = Cycle.current_active_cycle()
        if form.is_valid():
            cycle_end = form.cleaned_data["cycle_end"]
            cycle_name = form.cleaned_data["new_cycle_name"]
            max_cycle.cycle_end = cycle_end
            max_cycle.save()
            Cycle.objects.create(
                cycle_name=cycle_name,
                cycle_start=cycle_end,
                cycle_end=None,
                squat_max=max_cycle.squat_max + 10,
                bench_max=max_cycle.bench_max + 5,
                deadlift_max=max_cycle.deadlift_max + 10,
                ohp_max=max_cycle.ohp_max + 5,
            )
            return HttpResponseRedirect(reverse("tracker:cycles"))


class CycleDeleteView(LoginRequiredMixin, DeleteView):
    model = Cycle
    template_name = "tracker/cycle_delete.html"
    success_url = reverse_lazy("tracker:cycles")


class CycleCreateView(LoginRequiredMixin, CreateView):
    model = Cycle
    form_class = CycleForm
    template_name = "tracker/cycle_edit.html"
    success_url = reverse_lazy("tracker:cycles")


class CycleUpdateView(LoginRequiredMixin, UpdateView):
    model = Cycle
    form_class = CycleForm
    template_name = "tracker/cycle_edit.html"
    success_url = reverse_lazy("tracker:cycles")


class AccessoryCreateView(LoginRequiredMixin, CreateView):
    model = AccessoryLog
    fields = "__all__"
    template_name = "tracker/accessory_add.html"
    success_url = reverse_lazy("tracker:accessory_list")

    def get_initial(self):
        workout = get_object_or_404(Workout, id=self.kwargs.get("id"))
        return {"workout": workout}


class AccessoryListView(LoginRequiredMixin, ListView):
    model = AccessoryLift
    template_name = "tracker/accessory_list.html"

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(AccessoryListView, self).get_context_data(**kwargs)
        context["form"] = AccessoryLiftForm()
        return context


class AccessoryListFormView(LoginRequiredMixin, CreateView):
    template_name = "tracker/accessory_list.html"
    form_class = AccessoryLiftForm
    model = AccessoryLift
    success_url = reverse_lazy("tracker:accessory_list")


class AccessoryView(View):
    def get(self, request, *args, **kwargs):
        view = AccessoryListView.as_view()
        return view(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        view = AccessoryListFormView.as_view()
        return view(request, *args, **kwargs)


@login_required
def accessory_tracker(request):
    try:
        max_cycle = Cycle.current_active_cycle()
        workout_list = Workout.objects.filter(cycle=max_cycle).order_by("id")
        context = {"workout_list": workout_list, "form": WorkoutForm}
        return render(request, "tracker/accessory_tracker.html", context)
    except Cycle.DoesNotExist:
        return HttpResponseRedirect(reverse("tracker:cycles"))


class AccessoryDeleteView(LoginRequiredMixin, DeleteView):
    model = AccessoryLift
    template_name = "tracker/accessorylift_delete.html"
    success_url = reverse_lazy("tracker:accessory_list")


class AccessoryUpdateView(LoginRequiredMixin, UpdateView):
    model = AccessoryLift
    fields = "__all__"
    template_name = "tracker/accessorylift_edit.html"
    success_url = reverse_lazy("tracker:accessory_list")


class AccessoryLogDeleteView(LoginRequiredMixin, DeleteView):
    model = AccessoryLog
    template_name = "tracker/accessorylift_delete.html"
    success_url = reverse_lazy("tracker:accessory_list")


class AccessoryLogUpdateView(LoginRequiredMixin, UpdateView):
    model = AccessoryLog
    fields = "__all__"
    template_name = "tracker/accessorylift_edit.html"
    success_url = reverse_lazy("tracker:accessory_list")


# class ChartView(LoginRequiredMixin, ListView):
#     model = AccessoryLift
#     template_name = 'tracker/charts.html'


@login_required
def chartview(request):
    squat_data = []
    squat_labels = []
    bench_data = []
    bench_labels = []
    deadlift_data = []
    deadlift_labels = []
    ohp_data = []
    ohp_labels = []

    queryset = Workout.objects.order_by("date_completed")

    for workout in queryset:
        if workout.lift == "S" and workout.date_completed:
            squat_data.append(workout.estimated_1rm)
            squat_labels.append(workout.date_completed.strftime("%b %d, %Y"))
        if workout.lift == "B" and workout.date_completed:
            bench_data.append(workout.estimated_1rm)
            bench_labels.append(workout.date_completed.strftime("%b %d, %Y"))
        if workout.lift == "D" and workout.date_completed:
            deadlift_data.append(workout.estimated_1rm)
            deadlift_labels.append(workout.date_completed.strftime("%b %d, %Y"))
        if workout.lift == "O" and workout.date_completed:
            ohp_data.append(workout.estimated_1rm)
            ohp_labels.append(workout.date_completed.strftime("%b %d, %Y"))

    # queryset = Workout.objects.filter(lift="S").order_by('date_completed')

    return render(
        request,
        "tracker/charts.html",
        {
            "squat_labels": squat_labels,
            "bench_labels": bench_labels,
            "deadlift_labels": deadlift_labels,
            "ohp_labels": ohp_labels,
            "squat_data": squat_data,
            "bench_data": bench_data,
            "deadlift_data": deadlift_data,
            "ohp_data": ohp_data,
        },
    )
