from django.urls import path
from .views import _render_agent_view
urlpatterns = [
    path('dashboard', _render_agent_view, name="agent_dash_board")
]
