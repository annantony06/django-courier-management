from django.urls import path
from .views import (
   staff_login_view,
    signin_view,
    signup_view,
    logout_view, 
    forgot_view,
    reset_view,
    dashboard_view,
    branches_view,
    branch_detail_view,
    manage_packages,  # Updated to manage packages instead of creating
    update_package_status,  # Keep this for updating package status
    feedback_list_view,
    feedback_detail_view,
    request_refund,
    user_list_view,
    about_view,
    CustomPasswordResetView
)
urlpatterns = [

    path('', staff_login_view, name='staff'),  # Home page (login page)
    path('dashboard/', dashboard_view, name='staffdashboard'),
    path('staffsignin/', signin_view, name='staffsignin'),  # Sign in page
       path('signup/', signup_view, name='staffsignup'),
    path('logout/', logout_view, name='stafflogout'), 
    path('forgot/', forgot_view, name='staffforgot'),  # Forgot password page
      # Dashboard URL
    path('reset/', reset_view, name='reset'),  # Reset password page
    # Dashboard page
    path('branches/', branches_view, name='branches'),  # Branches list
    path('branch/<int:branch_id>/', branch_detail_view, name='branch_detail'),  # Branch detail page
    path('manage-packages/', manage_packages, name='manage_packages'),#xisting packages
    path('package/update/<str:tracking_number>/', update_package_status, name='update_package_status'),  # Update package status page
      path('feedback/', feedback_list_view, name='feedback_list'),
    path('feedback/<int:feedback_id>/', feedback_detail_view, name='feedback_detail'),  # View feedback details
    path('feedback/refund/request/<int:feedback_id>/', request_refund, name='request_refund'),  # Request refund
    path('users/', user_list_view, name='user_list'),  # List all users (if needed)
    path('about/', about_view, name='about'),  # About page
]