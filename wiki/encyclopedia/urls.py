from django.urls import path

from . import views

app_name = "encyclopedia"
urlpatterns = [
    path("wiki/", views.index, name="index"),
    path("wiki/new/", views.new, name="new"),
    path("wiki/<str:entry>", views.entry, name="entry"),
    path("wiki/search/", views.search, name="search")
]
