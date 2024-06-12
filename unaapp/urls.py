from django.urls import path

from unaapp import views

urlpatterns = [
    path('create_report/', views.CreateUserMetrics.as_view(), name='create-report'),
    path('get_levels_by_id/', views.GetGlucoseLevelsByUser.as_view(), name='get-glucose-levels'),
]
