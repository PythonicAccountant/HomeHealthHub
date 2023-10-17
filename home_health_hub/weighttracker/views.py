from datetime import datetime

from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from django.template.response import TemplateResponse
from django.urls import reverse

from .forms import WeightLogForm
from .models import WeightLog


@login_required
def month_dash(request, year=datetime.today().year, month=datetime.today().month):
    context = {
        "days": WeightLog.get_or_create_days(request.user, year, month),
        "month": month,
        "year": year,
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
        request,
        "weighttracker/fragments/weightlog_readonly_fragment.html",
        {"weightlog": weightlog},
    )
