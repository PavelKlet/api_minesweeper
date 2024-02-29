from django.urls import path
from .views import MineSweeperNewAPIView, MineSweeperTurnAPIView

appname = "appminesweeper"

urlpatterns = [
    path("new", MineSweeperNewAPIView.as_view(), name="new"),
    path("turn", MineSweeperTurnAPIView.as_view(), name="turn"),
]
