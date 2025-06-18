
from django.urls import path
from . import views

app_name = 'main'

urlpatterns = [
    path('', views.home, name='home'),
    path('toggle-vote/<int:discussion_id>/', views.toggle_vote, name='toggle_vote'),
    path('discussion/<int:discussion_id>/', views.discussion_detail, name='discussion_detail'),
    path('category/<slug:slug>/', views.category_filter, name='category_filter'),
]