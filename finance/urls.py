from django.urls import path
from . import views

urlpatterns = [
    path("", views.dashboard_view, name="dashboard"),

    path("profile/", views.profile_view, name="profile"),

    path(
        "purchase/add/",
        views.purchase_add_view,
        name="purchase_add"
    ),

    path(
        "feedback/",
        views.feedback_list_view,
        name="feedback_list"
    ),

    path(
        "feedback/add/",
        views.feedback_add_view,
        name="feedback_add"
    ),

    path(
        "feedback/<int:pk>/edit/",
        views.feedback_update_view,
        name="feedback_update"
    ),

    path(
        "feedback/<int:pk>/delete/",
        views.feedback_delete_view,
        name="feedback_delete"
    ),
    path("purchase/<int:pk>/", views.purchase_detail_view, name="purchase_detail"),
path("purchase/<int:pk>/edit/", views.purchase_update_view, name="purchase_update"),
path("purchase/<int:pk>/delete/", views.purchase_delete_view, name="purchase_delete"),
path("purchases/", views.purchase_list_view, name="purchase_list"),
]