from django.urls import path
from . import views

app_name = 'authentication'

urlpatterns = [
    # Index page (redirects based on authentication status)
    path('', views.index_view, name='index'),
    
    # Authentication URLs
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('dashboard/', views.dashboard_view, name='dashboard'),
]
