from django.urls import path

from . import views

app_name = "wiki"
urlpatterns = [
    path("", views.index, name="index"),
    path("random/", views.random_entry, name="random_entry"),
    path("wiki/<str:name>", views.entry, name="entry"),
    path("new/", views.new_entry, name="new_entry"),
    path("edit/<str:name>", views.edit_page, name="edit_page")
]
