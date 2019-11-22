from django.urls import path, include

import klogin.views
from klogin import ajax

urlpatterns = [
    path('<str:stock_code>', klogin.views.main_view2),
]
