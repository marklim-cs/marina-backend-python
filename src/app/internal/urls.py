from django.urls import path
from .transport.rest.handlers import MeView

urlpatterns = [
     path('me/<int:id>', MeView.as_view()),
]