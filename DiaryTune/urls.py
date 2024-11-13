from django.urls import path
from . import views


urlpatterns = [
    path('', views.main, name='main'),
    path('main/<int:year>/<int:month>/<int:day>/', views.main, name='main_with_params'),
    path('recommendation/', views.recommendation, name='recommendation'),
    path('diary/', views.diary, name='diary'),
    path('diary/<int:year>/<int:month>/<int:day>/<int:dayofweek>/', views.diary, name='diary_with_params'),
    path('tutorial/', views.tutorial, name='tutorial'),
    path('tutorial_2/', views.tutorial_2, name='tutorial_2'),
    path('tutorial_3/', views.tutorial_3, name='tutorial_3'),
    path('tutorial_4/', views.tutorial_4, name='tutorial_4'),
    path('tutorial_5/', views.tutorial_5, name='tutorial_5'),
    path('tutorial_6/', views.tutorial_6, name='tutorial_6'),
    path('tutorial_7/', views.tutorial_7, name='tutorial_7'),
]