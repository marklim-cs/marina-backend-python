from django.urls import path
from .internal.transport.webview.handlers import MeViewHtml

urlpatterns = [
     path('me/<int:id>', MeViewHtml.as_view()),
]