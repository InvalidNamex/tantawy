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
    
    # User Management URLs
    path('users/', views.users_list_view, name='users_list'),
    path('users/create/', views.user_create_view, name='user_create'),
    path('users/<int:user_id>/edit/', views.user_edit_view, name='user_edit'),
    path('users/<int:user_id>/delete/', views.user_delete_view, name='user_delete'),
    path('users/<int:user_id>/detail/', views.user_detail_view, name='user_detail'),
    
    # Agent Management URLs
    path('agents/manage/', views.agents_manage_view, name='agents_manage'),
    path('agents/manage/create/', views.agent_create_view, name='agent_create'),
    path('agents/manage/<int:agent_id>/', views.agent_detail_view, name='agent_detail'),
    path('agents/manage/<int:agent_id>/edit/', views.agent_edit_view, name='agent_edit'),
    path('agents/manage/<int:agent_id>/delete/', views.agent_delete_view, name='agent_delete'),
    
    # API Endpoints
    path('api/agents/login/', views.agent_login_api, name='agent_login_api'),
    path('api/agents/<int:agent_id>/invoices/', views.agent_invoices_api, name='agent_invoices_api'),
    path('api/agents/invoices/', views.agent_invoices_filtered_api, name='agent_invoices_filtered_api'),
    path('api/agents/transactions/', views.agent_transactions_filtered_api, name='agent_transactions_filtered_api'),
    path('api/agents/customer_transactions/', views.customer_transactions_api, name='customer_transactions_api'),
]
