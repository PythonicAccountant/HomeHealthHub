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
    path("getchart/<int:year>/<int:month>", view=views.get_chart, name="getchart"),
    path(
        "profile/create",
        view=views.weight_profile_create_view,
        name="weight-profile-create-view",
    ),
    path(
        "profile/update/<int:id>",
        view=views.weight_profile_update_view,
        name="weight-profile-update-view",
    ),
]
