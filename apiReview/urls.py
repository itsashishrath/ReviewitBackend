from django.urls import path

from . import views

app_name = "apiReview"

urlpatterns = [
    # path("", views.ReactView.as_view(), name="index"),
    path('', views.search_mobile_phones_view, name='search'),

]
