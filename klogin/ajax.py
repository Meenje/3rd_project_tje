from django.urls import path, include

import klogin.views

urlpatterns = [
    path('ajax', klogin.views.like),
]