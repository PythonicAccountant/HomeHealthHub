from django.urls import path

from . import views

app_name = "weighttracker"

urlpatterns = [
    path("<int:year>/<int:month>", view=views.month_dash, name="monthdashym"),
    path("", view=views.month_dash, name="monthdash"),
    path(
        "weightlog/update/<int:id>",
        view=views.weightlog_update_row,
        name="weightlog-update",
    ),
    path("weightlog/<int:id>", view=views.weightlog_get_row, name="weightlog-get"),
]
