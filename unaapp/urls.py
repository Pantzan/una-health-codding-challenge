from django.urls import path

from unaapp import views

urlpatterns = [
    path('create_report/', views.CreateUserMetrics.as_view(), name='create-report'),
    path('GetGlucoseLevelsByUser/', views.CreateUserMetrics.as_view(), name='create-report'),
]
