from django.urls import path

from . import views

app_name = "tracker"
urlpatterns = [
    path("", views.tracker, name="tracker"),
    path("accessories/log", views.accessory_tracker, name="accessory_tracker"),
    path("cycles/", views.cycles, name="cycles"),
    path("charts/", views.chartview, name="charts"),
    path("accessories/", views.AccessoryView.as_view(), name="accessory_list"),
    path(
        "accessories/<int:pk>/delete",
        views.AccessoryDeleteView.as_view(),
        name="accessory_delete",
    ),
    path(
        "accessories/<int:pk>/update",
        views.AccessoryUpdateView.as_view(),
        name="accessory_update",
    ),
    path(
        "accessories/log/<int:pk>/delete",
        views.AccessoryLogDeleteView.as_view(),
        name="accessorylog_delete",
    ),
    path(
        "accessories/log/<int:pk>/update",
        views.AccessoryLogUpdateView.as_view(),
        name="accessorylog_update",
    ),
    path(
        "cycles/<int:pk>/delete", views.CycleDeleteView.as_view(), name="cycle_delete"
    ),
    path(
        "cycles/<int:pk>/update", views.CycleUpdateView.as_view(), name="cycle_update"
    ),
    path(
        "<int:id>/accessory/create",
        views.AccessoryCreateView.as_view(),
        name="add_accessory",
    ),
    path("cycles/create", views.CycleCreateView.as_view(), name="cycle_create"),
    path("archive/<int:pk>", views.view_archive, name="view_archive"),
    path("update/<int:pk>", views.workout_update, name="workout_update"),
    path("startnext/", views.start_next, name="start_next"),
]
