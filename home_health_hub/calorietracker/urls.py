from django.urls import path

from .views import (
    add_to_todoist_project_view,
    bulk_todoist_view,
    calorie_profile_create_view,
    calorie_profile_update_view,
    daily_dash_view,
    food_create_view,
    food_delete_view,
    food_filter_view,
    food_list_view,
    food_log_item_create_view,
    food_log_item_delete_view,
    food_log_item_update_view,
    food_update_view,
    get_uom_view,
)

app_name = "calorietracker"

urlpatterns = [
    path("", view=daily_dash_view, name="dailydash"),
    path("foodlogitem/add/", view=food_log_item_create_view, name="FoodLogItem-create"),
    path(
        "foodlogitem/delete/<int:id>/",
        view=food_log_item_delete_view,
        name="FoodLogItem-delete",
    ),
    path(
        "foodlogitem/update/<int:id>/",
        view=food_log_item_update_view,
        name="FoodLogItem-update",
    ),
    path("foodlogitem/getuom/", view=get_uom_view, name="getuom"),
    path("food/", view=food_list_view, name="Food-list"),
    path("food/filter", view=food_filter_view, name="Food-filter"),
    path("food/add", view=food_create_view, name="Food-create"),
    path("food/delete/<int:id>/", view=food_delete_view, name="Food-delete"),
    path("food/update/<int:id>/", view=food_update_view, name="Food-update"),
    path(
        "food/todoist/add/<int:id>/",
        view=add_to_todoist_project_view,
        name="todoist_add",
    ),
    path(
        "food/todoist/add/bulk/",
        view=bulk_todoist_view,
        name="todoist_add_bulk",
    ),
    path(
        "calorieprofile/add",
        view=calorie_profile_create_view,
        name="calorie_profile_create_view",
    ),
    path(
        "calorieprofile/update/<int:id>/",
        view=calorie_profile_update_view,
        name="calorie_profile_update_view",
    ),
]
