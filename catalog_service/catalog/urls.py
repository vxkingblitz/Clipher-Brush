from django.urls import path
from .views import CategoryListView, MarkersSetListView

urlpatterns = [
    path("categories/", CategoryListView.as_view()),
    path("categories/<int:category_id>/", CategoryListView.as_view()),
    path("markers-sets/", MarkersSetListView.as_view()),
    path("markers-sets/<int:markers_set_id>/", MarkersSetListView.as_view()),
]
