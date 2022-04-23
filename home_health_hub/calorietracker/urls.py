from django.urls import path

from .views import (
    add_calorie_profile,
    delete_food_list_view,
    food_list_view,
    food_log_delete_view,
    food_log_list_view,
    food_log_update_view,
    get_uom,
    new_entry_view,
    new_food_view,
)

app_name = "calorietracker"

urlpatterns = [
    path("", view=food_log_list_view, name="dailydash"),
    path("foodlog/add/", view=new_entry_view, name="newentry"),
    path("foodlog/delete/<int:id>/", view=food_log_delete_view, name="deleteentry"),
    path("foodlog/update/<int:id>/", view=food_log_update_view, name="updateentry"),
    path("getuom/", view=get_uom, name="getuom"),
    path("foods/", view=food_list_view, name="food_list"),
    path("foods/add", view=new_food_view, name="food_add"),
    path("foods/delete/<int:id>/", view=delete_food_list_view, name="deletefood"),
    path("calorieprofile/", view=add_calorie_profile, name="add_calorie_profile"),
]
