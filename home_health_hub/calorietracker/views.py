from datetime import datetime

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404
from django.template.response import TemplateResponse
from django.urls import reverse

from .filters import FoodLogItemFilter
from .forms import CalorieProfileForm, FoodForm, FoodLogForm
from .models import CalorieProfile, Food, FoodLog, FoodLogItem, IntegrationProfile
from .todoist import add_to_todoist, bulk_add_to_todoist


@login_required
def daily_dash_view(request):
    food_log, created = FoodLog.objects.get_or_create(
        user=request.user, date=datetime.today()
    )

    try:
        calorie_goal = CalorieProfile.objects.get(user=request.user)
    except CalorieProfile.DoesNotExist:
        return HttpResponseRedirect(reverse("calorietracker:add_calorie_profile"))

    total = food_log.calorie_total
    calories_remaining = calorie_goal.daily_calorie_goal - total
    perc = (total / calorie_goal.daily_calorie_goal) * 100
    context = {
        "object": food_log,
        "total": total,
        "calorie_goal": calorie_goal,
        "rem": calories_remaining,
        "perc": perc,
    }

    if not request.META.get("HTTP_HX_REQUEST"):
        return TemplateResponse(request, "calorietracker/dailydash.html", context)
    return TemplateResponse(
        request, "calorietracker/fragments/dailydash_fragment.html", context
    )


@login_required
def food_log_item_create_view(request):
    # if this is a POST request we need to process the form data
    food_log, created = FoodLog.objects.get_or_create(
        user=request.user, date=datetime.today()
    )
    if request.method == "POST":
        # create a form instance and populate it with data from the request:
        form = FoodLogForm(request.POST)
        # check whether it's valid:
        if form.is_valid():
            entry = form.save(commit=False)
            entry.food_log = food_log
            entry.save()
            return HttpResponseRedirect(reverse("calorietracker:dailydash"))

    # if a GET (or any other method) we'll create a blank form
    else:
        initial_dict = FoodLogForm.get_initial_for_category()
        form = FoodLogForm(initial=initial_dict)

    if not request.META.get("HTTP_HX_REQUEST"):
        return TemplateResponse(
            request, "calorietracker/food_log_item_form.html", {"form": form}
        )
    else:
        return TemplateResponse(
            request,
            "calorietracker/fragments/food_log_item_form_fragment.html",
            {"form": form},
        )


@login_required
def food_log_item_update_view(request, id):
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
            "calorietracker/fragments/food_log_item_update_form_fragment.html",
            {"form": form},
        )


@login_required
def food_log_item_delete_view(request, id):
    obj = get_object_or_404(FoodLogItem, id=id)
    obj.delete()
    return HttpResponseRedirect(reverse("calorietracker:dailydash"))


@login_required
def get_uom_view(request):
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
                "calorietracker/fragments/food_log_item_est_cal_fragment.html",
                context,
            )


@login_required
def food_list_view(request):
    context = get_food_context()
    if not request.META.get("HTTP_HX_REQUEST"):
        return TemplateResponse(request, "calorietracker/food_list.html", context)
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
        return TemplateResponse(request, "calorietracker/food_list.html", context)
    else:
        return TemplateResponse(
            request, "calorietracker/fragments/food_list_fragment.html", context
        )


def get_food_context():
    foods = Food.objects.all()
    context = {"object": foods}
    return context


@login_required
def food_create_view(request):
    # if this is a POST request we need to process the form data
    if request.method == "POST":
        # create a form instance and populate it with data from the request:
        form = FoodForm(request.POST)
        # check whether it's valid:
        if form.is_valid():
            entry = form.save(commit=False)
            entry.save()
            return HttpResponseRedirect(reverse("calorietracker:Food-list"))

    # if a GET (or any other method) we'll create a blank form
    else:
        form = FoodForm()

    if not request.META.get("HTTP_HX_REQUEST"):
        return TemplateResponse(
            request, "calorietracker/food_form.html", {"form": form}
        )
    else:
        return TemplateResponse(
            request, "calorietracker/fragments/food_form_fragment.html", {"form": form}
        )


@login_required
def calorie_profile_create_view(request):
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
            return HttpResponseRedirect(reverse("calorietracker:Food-list"))
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
def calorie_profile_update_view(request, id):
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
    return TemplateResponse(
        request,
        "calorietracker/fragments/message_fragment.html",
    )


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


@login_required
def bulk_todoist_view(request):
    if request.method == "POST":
        bulk_list = request.POST.getlist("names")
        integration_profile = IntegrationProfile.objects.get(user=request.user)
        success = bulk_add_to_todoist(bulk_list, integration_profile)
        if success:
            messages.success(
                request,
                message=f"{len(bulk_list)} items added to Todoist successfully!",
            )
        else:
            messages.error(request, message="Error adding to Todoist")
        return TemplateResponse(
            request,
            "calorietracker/fragments/message_fragment.html",
        )


def food_log_list_view(request):
    context = {}
    context["object"] = (
        FoodLog.objects.filter(user=request.user).calorie_total_day().all()
    )

    if not request.META.get("HTTP_HX_REQUEST"):
        return TemplateResponse(request, "calorietracker/food_log_list.html", context)
    return TemplateResponse(
        request, "calorietracker/fragments/food_log_list_fragment.html", context
    )


def food_log_detail_view(request, id):
    food_log = get_object_or_404(FoodLog, id=id)

    try:
        calorie_goal = CalorieProfile.objects.get(user=request.user)
    except CalorieProfile.DoesNotExist:
        return HttpResponseRedirect(reverse("calorietracker:add_calorie_profile"))

    total = food_log.calorie_total
    calories_remaining = calorie_goal.daily_calorie_goal - total
    perc = (total / calorie_goal.daily_calorie_goal) * 100
    context = {
        "object": food_log,
        "total": total,
        "calorie_goal": calorie_goal,
        "rem": calories_remaining,
        "perc": perc,
    }

    if not request.META.get("HTTP_HX_REQUEST"):
        return TemplateResponse(request, "calorietracker/dailydash.html", context)
    return TemplateResponse(
        request, "calorietracker/fragments/dailydash_fragment.html", context
    )
