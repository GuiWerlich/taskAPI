from django.urls import path
from .views import TaskView


urlpatterns = [
    path('tasks/', TaskView.as_view()),
    path('tasks/<int:task_id>/', TaskView.as_view()),
]