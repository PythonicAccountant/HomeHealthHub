from datetime import datetime

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404
from django.template.response import TemplateResponse
from django.urls import reverse

from .filters import FoodLogItemFilter
from .forms import CalorieProfileForm, FoodForm, FoodLogForm
from .models import CalorieProfile, Food, FoodLogItem, IntegrationProfile
from .todoist import add_to_todoist


@login_required
def food_log_list_view(request):
    try:
        food_items = FoodLogItem.objects.filter(
            user=request.user, date_eaten=datetime.today()
        ).order_by("category")
    except FoodLogItem.DoesNotExist:
        food_items = {}

    # food_items = FoodLogItem.objects.all()
    total = FoodLogItem.objects.calorie_total_day(
        date=datetime.today(), user=request.user
    )
    if total["total"] is None:
        total = {"total": 0}
    try:
        calorie_goal = CalorieProfile.objects.get(user=request.user)
    except CalorieProfile.DoesNotExist:
        return HttpResponseRedirect(reverse("calorietracker:add_calorie_profile"))

    calories_remaining = calorie_goal.daily_calorie_goal - total["total"]
    perc = (total["total"] / calorie_goal.daily_calorie_goal) * 100
    context = {
        "object": food_items,
        "total": total,
        "calorie_goal": calorie_goal,
        "rem": calories_remaining,
        "perc": perc,
    }

    if not request.META.get("HTTP_HX_REQUEST"):
        return TemplateResponse(request, "calorietracker/dailydash.html", context)
    return TemplateResponse(request, "calorietracker/fragments/foodlog.html", context)


@login_required
def new_entry_view(request):
    # if this is a POST request we need to process the form data
    if request.method == "POST":
        # create a form instance and populate it with data from the request:
        form = FoodLogForm(request.POST)
        # check whether it's valid:
        if form.is_valid():
            entry = form.save(commit=False)
            entry.user = request.user
            entry.save()
            return HttpResponseRedirect(reverse("calorietracker:dailydash"))

    # if a GET (or any other method) we'll create a blank form
    else:
        initial_dict = FoodLogForm.get_initial_for_category()
        form = FoodLogForm(initial=initial_dict)

    if not request.META.get("HTTP_HX_REQUEST"):
        return TemplateResponse(request, "calorietracker/newentry.html", {"form": form})
    else:
        return TemplateResponse(
            request, "calorietracker/fragments/new_entry_fragment.html", {"form": form}
        )


@login_required
def food_log_update_view(request, id):
    food_log = get_object_or_404(FoodLogItem, id=id)
    if request.method == "POST":
        form = FoodLogForm(request.POST, instance=food_log)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse("calorietracker:dailydash"))
    else:
        form = FoodLogForm(instance=food_log)

    if not request.META.get("HTTP_HX_REQUEST"):
        return TemplateResponse(
            request, "calorietracker/food_log_update.html", {"form": form}
        )
    else:
        return TemplateResponse(
            request,
            "calorietracker/fragments/food_log_update_fragment.html",
            {"form": form},
        )


@login_required
def food_log_delete_view(request, id):
    obj = get_object_or_404(FoodLogItem, id=id)
    obj.delete()
    if not request.META.get("HTTP_HX_REQUEST"):
        return HttpResponseRedirect(reverse("calorietracker:dailydash"))
    else:
        try:
            food_items = FoodLogItem.objects.filter(
                user=request.user, date_eaten=datetime.today()
            )
        except FoodLogItem.DoesNotExist:
            food_items = {}

        # food_items = FoodLogItem.objects.all()
        total = FoodLogItem.objects.calorie_total_day(
            date=datetime.today(), user=request.user
        )
        if total["total"] is None:
            total = {"total": 0}
        calorie_goal = CalorieProfile.objects.get(user=request.user)
        calories_remaining = calorie_goal.daily_calorie_goal - total["total"]
        context = {
            "object": food_items,
            "total": total,
            "calorie_goal": calorie_goal,
            "rem": calories_remaining,
        }
        return TemplateResponse(
            request, "calorietracker/fragments/foodlog.html", context
        )


@login_required
def get_uom(request):
    if request.method == "POST":
        if request.META.get("HTTP_HX_REQUEST"):
            context = {}
            food_post = request.POST.get("food")
            units_eaten = request.POST.get("units_eaten")
            if units_eaten == "":
                units_eaten = "0.0"

            food = Food.objects.get(id=food_post)

            context["form"] = FoodLogForm(request.POST)
            context["food"] = food
            context["estimated_calories"] = float(
                food.calorie_per_serving_unit
            ) * float(units_eaten)
            return TemplateResponse(
                request,
                "calorietracker/fragments/new_entry_est_cal_fragments.html",
                context,
            )

        # else:
        #     form = FoodLogForm(request.POST)
        #     # check whether it's valid:
        #     if form.is_valid():
        #         entry = form.save(commit=False)
        #         entry.user = request.user
        #         entry.save()
        #         return HttpResponseRedirect(reverse("calorietracker:dailydash"))
        #
        # food_post = request.POST.get("food")
        # food = Food.objects.get(id=food_post)
        # uom = food.get_uom_display()
        # uom = uom.capitalize() + " Eaten"
        # return HttpResponse(uom)


@login_required
def food_list_view(request):
    context = get_food_context()
    if not request.META.get("HTTP_HX_REQUEST"):
        return TemplateResponse(request, "calorietracker/food_log_list.html", context)
    else:
        return TemplateResponse(
            request, "calorietracker/fragments/food_list_fragment.html", context
        )


@login_required
def food_delete_view(request, id):
    obj = get_object_or_404(Food, id=id)
    obj.delete()

    context = get_food_context()
    if not request.META.get("HTTP_HX_REQUEST"):
        return TemplateResponse(request, "calorietracker/food_log_list.html", context)
    else:
        return TemplateResponse(
            request, "calorietracker/fragments/food_list_fragment.html", context
        )


def get_food_context():
    foods = Food.objects.all()
    context = {"object": foods}
    return context


@login_required
def new_food_view(request):
    # if this is a POST request we need to process the form data
    if request.method == "POST":
        # create a form instance and populate it with data from the request:
        form = FoodForm(request.POST)
        # check whether it's valid:
        if form.is_valid():
            entry = form.save(commit=False)
            entry.save()
            return HttpResponseRedirect(reverse("calorietracker:food_list"))

    # if a GET (or any other method) we'll create a blank form
    else:
        form = FoodForm()

    if not request.META.get("HTTP_HX_REQUEST"):
        return TemplateResponse(request, "calorietracker/new_food.html", {"form": form})
    else:
        return TemplateResponse(
            request, "calorietracker/fragments/new_food_fragment.html", {"form": form}
        )


@login_required
def add_calorie_profile(request):
    # if this is a POST request we need to process the form data
    if request.method == "POST":
        # create a form instance and populate it with data from the request:
        form = CalorieProfileForm(request.POST)
        # check whether it's valid:
        if form.is_valid():
            entry = form.save(commit=False)
            entry.user = request.user
            entry.save()
            return HttpResponseRedirect(reverse("calorietracker:dailydash"))

    # if a GET (or any other method) we'll create a blank form
    else:
        form = CalorieProfileForm()

    if not request.META.get("HTTP_HX_REQUEST"):
        return TemplateResponse(
            request, "calorietracker/calorie_profile_form.html", {"form": form}
        )
    else:
        return TemplateResponse(
            request,
            "calorietracker/fragments/calorie_profile_form_fragment.html",
            {"form": form},
        )


@login_required
def food_update_view(request, id):
    food = get_object_or_404(Food, id=id)
    if request.method == "POST":
        form = FoodForm(request.POST, instance=food)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse("calorietracker:food_list"))
    else:
        form = FoodForm(instance=food)

    if not request.META.get("HTTP_HX_REQUEST"):
        return TemplateResponse(
            request, "calorietracker/food_update.html", {"form": form}
        )
    else:
        return TemplateResponse(
            request,
            "calorietracker/fragments/food_update_fragment.html",
            {"form": form},
        )


@login_required
def update_calorie_profile(request, id):
    calorie_profile = get_object_or_404(CalorieProfile, id=id)
    if request.method == "POST":
        form = CalorieProfileForm(request.POST, instance=calorie_profile)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse("home"))
    else:
        form = CalorieProfileForm(instance=calorie_profile)
    return TemplateResponse(
        request,
        "calorietracker/calorie_profile_update.html",
        {"form": form},
    )


@login_required
def add_to_todoist_project_view(request, id):
    food = Food.objects.get(id=id)
    integration_profile = IntegrationProfile.objects.get(user=request.user)
    success = add_to_todoist(item=food.name, integration_profile=integration_profile)
    if success:
        messages.success(request, message=f"{food.name} added to Todoist successfully!")
    else:
        messages.error(request, message="Error adding to Todoist")
    return HttpResponseRedirect(reverse("calorietracker:food_filter"))


def food_filter_view(request):
    f = FoodLogItemFilter(request.GET, queryset=FoodLogItem.objects.distinct_qty())

    if not request.META.get("HTTP_HX_REQUEST"):
        return TemplateResponse(
            request, "calorietracker/food_filter.html", {"filter": f}
        )

    else:
        return TemplateResponse(
            request,
            "calorietracker/fragments/food_filter_fragment.html",
            {"filter": f},
        )
