from django.urls import path
from . import views


app_name = 'analyzer'

urlpatterns = [
    path("answer-query", views.AnalyzerView().as_view())
]