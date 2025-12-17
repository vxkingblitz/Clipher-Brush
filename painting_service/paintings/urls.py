from django.urls import path
from .views import (
    PaintingCreateView,
    PublicPaintingFeedView,
    PublicPaintingDetailView,
    PublishPaintingView,
    SavePaintingView,
    MyPaintgsListView,
    PaintingDetailView,
)

urlpatterns = [
    path("", PaintingCreateView.as_view()),
    path("feed/", PublicPaintingFeedView.as_view()),
    path("<int:painting_id>/", PublicPaintingDetailView.as_view()),
    path("<int:painting_id>/publish/", PublishPaintingView.as_view()),
    path("<int:painting_id>/save/", SavePaintingView.as_view()),
    path("my/", MyPaintgsListView.as_view()),
    path('<int:painting_id>/detail/', PaintingDetailView.as_view()),
]
