from datetime import datetime

from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404
from django.template.response import TemplateResponse
from django.urls import reverse

from .forms import WeightLogForm, WeightLogNonTableForm, WeightProfileForm
from .models import WeightLog, WeightProfile


def get_current_year():
    return datetime.today().year


def get_current_month():
    return datetime.today().month


@login_required
def month_dash(request, year=get_current_year(), month=get_current_month()):
    try:
        weekly_loss = WeightLog.objects.weekly_loss2(request.user)
        estimated_daily_deficit = (weekly_loss * 3500) / 7
    except WeightLog.DoesNotExist:
        weekly_loss = 0
        estimated_daily_deficit = 0
    try:
        wp = WeightProfile.objects.get(user=request.user)
    except WeightProfile.DoesNotExist:
        return HttpResponseRedirect(reverse("weighttracker:weight-profile-create-view"))
    est_calories = wp.estimated_tdee + estimated_daily_deficit
    days = WeightLog.objects.get_or_create_days(request.user, year, month)
    labels = []
    trend_data = []
    weight_data = []
    for day in days:
        # if day.trend:
        labels.append(day.date.strftime("%b %d, %Y"))
        trend_data.append(day.trend)
        weight_data.append(day.weight)

    context = {
        "days": days,
        "weekly_loss": weekly_loss,
        "est_calories": est_calories,
        "daily_deficit": estimated_daily_deficit,
        "month": month,
        "year": year,
        "labels": labels,
        "trend_data": trend_data,
        "weight_data": weight_data,
    }

    if not request.META.get("HTTP_HX_REQUEST"):
        return TemplateResponse(request, "weighttracker/monthlydash.html", context)
    return TemplateResponse(
        request, "weighttracker/fragments/monthlydash_fragment.html", context
    )


@login_required
def weightlog_update_row(request, id):
    """Edit weightlog entry row(Form)"""
    weightlog = WeightLog.objects.get(id=id)
    # if put request then update, validate form save, redirect to weightlog_getrow
    if request.method == "POST":
        form = WeightLogForm(request.POST, instance=weightlog)
        if form.is_valid():
            entry = form.save(commit=False)
            entry.weight = form.cleaned_data["weight"]
            entry.save()
            return HttpResponseRedirect(
                reverse("weighttracker:weightlog-get", args=(id,))
            )
    # if get request then return "form" as row
    if request.method == "GET":
        form = WeightLogForm(instance=weightlog)

        return TemplateResponse(
            request,
            "weighttracker/fragments/weightlog_update_fragment.html",
            {"form": form, "weightlog": weightlog},
        )


@login_required
def weightlog_get_row(request, id):
    """Read only view of weightlog entry row"""
    # get request return read only row fragment
    weightlog = WeightLog.objects.get(id=id)
    return TemplateResponse(
        request=request,
        template="weighttracker/fragments/weightlog_readonly_fragment.html",
        context={"weightlog": weightlog},
        headers={"HX-Trigger": "weightUpdate"},
    )


@login_required
def get_chart(request, year=get_current_year(), month=get_current_month()):
    days = WeightLog.objects.get_or_create_days(request.user, year, month)
    labels = []
    trend_data = []
    weight_data = []
    for day in days:
        # if day.trend:
        labels.append(day.date.strftime("%b %d, %Y"))
        trend_data.append(day.trend)
        weight_data.append(day.weight)

    context = {
        "days": days,
        "month": month,
        "year": year,
        "labels": labels,
        "trend_data": trend_data,
        "weight_data": weight_data,
    }

    if not request.META.get("HTTP_HX_REQUEST"):
        return TemplateResponse(
            request, "weighttracker/fragments/chart_fragment.html", context
        )
    return TemplateResponse(
        request, "weighttracker/fragments/chart_fragment.html", context
    )


@login_required
def weight_profile_create_view(request):
    # if this is a POST request we need to process the form data
    if request.method == "POST":
        # create a form instance and populate it with data from the request:
        form = WeightProfileForm(request.POST)
        # check whether it's valid:
        if form.is_valid():
            entry = form.save(commit=False)
            entry.user = request.user
            entry.save()
            return HttpResponseRedirect(reverse("weighttracker:monthdash"))

    # if a GET (or any other method) we'll create a blank form
    else:
        form = WeightProfileForm()

    if not request.META.get("HTTP_HX_REQUEST"):
        return TemplateResponse(
            request, "weighttracker/weight_profile_form.html", {"form": form}
        )
    else:
        return TemplateResponse(
            request,
            "weighttracker/fragments/weight_profile_form_fragment.html",
            {"form": form},
        )


@login_required
def weight_profile_update_view(request, id):
    weight_profile = get_object_or_404(WeightProfile, id=id)
    if request.method == "POST":
        form = WeightProfileForm(request.POST, instance=weight_profile)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse("home"))
    else:
        form = WeightProfileForm(instance=weight_profile)
    return TemplateResponse(
        request,
        "weighttracker/weight_profile_update.html",
        {"form": form},
    )


@login_required
def weight_log_non_table_update_view(request):
    # if this is a POST request we need to process the form data
    weightlog = WeightLog.objects.get(user=request.user, date=datetime.today())
    if request.method == "POST":
        # create a form instance and populate it with data from the request:
        form = WeightLogNonTableForm(request.POST, instance=weightlog)
        # check whether it's valid:
        if form.is_valid():
            entry = form.save(commit=False)
            entry.weight = form.cleaned_data["weight"]
            entry.save()
            return HttpResponseRedirect(reverse("weighttracker:monthdash"))

    # if put request then update, validate form save, redirect to weightlog_getrow
    else:
        form = WeightLogNonTableForm(instance=weightlog)

    if not request.META.get("HTTP_HX_REQUEST"):
        return TemplateResponse(
            request, "weighttracker/weightlog_form.html", {"form": form}
        )
    else:
        return TemplateResponse(
            request,
            "weighttracker/fragments/weightlog_form_fragment.html",
            {"form": form},
        )
