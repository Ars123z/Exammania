from django.urls import path
from . import views

urlpatterns= [
    path("", views.main, name="videos_main"),
    path("chemistry/<str:topic>/<int:no>", views.chemistry, name="videos_chemistry"),
    path("physics/<str:topic>/<int:no>", views.physics, name="videos_physics"),
    path("math/<str:topic>/<int:no>", views.maths, name="videos_maths"),
]