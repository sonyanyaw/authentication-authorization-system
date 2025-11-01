from django.urls import path

from accounts import views

urlpatterns = [
    path('register/', views.register_view, name='register'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('profile/', views.profile_view, name='profile'),
    path('access-rules/', views.access_rules_view, name='access-rules'),
    path('access-rules/<int:rule_id>/', views.access_rule_detail_view, name='access-rule-detail'),
]
