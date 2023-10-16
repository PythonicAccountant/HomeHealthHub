from django.urls import path

from . import views

app_name = "weighttracker"

urlpatterns = [
    path("<int:year>/<int:month>", view=views.month_dash, name="monthdashym"),
    path("", view=views.month_dash, name="monthdash"),
]
