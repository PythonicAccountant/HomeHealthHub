from django.urls import path

from . import views

app_name = "calorietracker"

urlpatterns = [
    path("", view=views.daily_dash_view, name="dailydash"),
    path(
        "foodlogitem/add/",
        view=views.food_log_item_create_view,
        name="FoodLogItem-create",
    ),
    path(
        "foodlogitem/delete/<int:id>/",
        view=views.food_log_item_delete_view,
        name="FoodLogItem-delete",
    ),
    path(
        "foodlogitem/update/<int:id>/",
        view=views.food_log_item_update_view,
        name="FoodLogItem-update",
    ),
    path("foodlogitem/getuom/", view=views.get_uom_view, name="getuom"),
    path("food/", view=views.food_list_view, name="Food-list"),
    path("food/filter", view=views.food_filter_view, name="Food-filter"),
    path("food/add", view=views.food_create_view, name="Food-create"),
    path("food/delete/<int:id>/", view=views.food_delete_view, name="Food-delete"),
    path("food/update/<int:id>/", view=views.food_update_view, name="Food-update"),
    path("foodlog/", view=views.food_log_list_view, name="FoodLog-list"),
    path("foodlog/<int:id>/", view=views.food_log_detail_view, name="FoodLog-detail"),
    path(
        "food/todoist/add/<int:id>/",
        view=views.add_to_todoist_project_view,
        name="todoist_add",
    ),
    path(
        "food/todoist/add/bulk/",
        view=views.bulk_todoist_view,
        name="todoist_add_bulk",
    ),
    path(
        "calorieprofile/add",
        view=views.calorie_profile_create_view,
        name="calorie_profile_create_view",
    ),
    path(
        "calorieprofile/update/<int:id>/",
        view=views.calorie_profile_update_view,
        name="calorie_profile_update_view",
    ),
]
