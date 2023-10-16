from datetime import datetime

from django.contrib.auth.decorators import login_required
from django.template.response import TemplateResponse

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
