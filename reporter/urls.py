from django.urls import path
from . import views

app_name = 'reporter'
urlpatterns = [
    # Home page
    path('', views.index, name='index'),
    path("reports/", views.reports, name="reports"),
    path('new_report/', views.new_report, name='new_report'),
    path('map_view/', views.map_view, name='map_view')
]

