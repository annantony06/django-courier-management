from django.urls import path
from .views import (
    index,
    signup,  # Ensure this is your signup view
    signin,
    logout_view,
    forgot,
    resetpassword,
    dashboard,
    add_package,
    payment,
    schedule_delivery,
    handle_time_slot_selection,
    track_page,
    track_courier,
    feedback_view,
    list_couriers,
    about,
    feedbacksuccess_view,
    paymentsuccess,
    courier_success,
)

urlpatterns = [
    path('', index, name='index'),
    path('signup/', signup, name='signup'),  # This should be defined
    path('signin/', signin, name='signin'),
    path('forgot/', forgot, name='forgot'),
    path('resetpassword/<str:token>/', resetpassword, name='resetpassword'),
       path('dashboard/', dashboard, name='dashboard'),
    path('addpackage/', add_package, name='add_package'),
    path('payment/', payment, name='payment'),
   path('paymentsuccess/', paymentsuccess, name='paymentsuccess'),  # Add this line
    path('schedule-delivery/', schedule_delivery, name='schedule_delivery'),
    path('handle-time-slot-selection/', handle_time_slot_selection, name='handle_time_slot_selection'),
    path('track/', track_page, name='track_page'),
    path('track-courier/', track_courier, name='track_courier'),
    path('feedback/', feedback_view, name='feedback'),
    path('feedbacksuccess/', feedbacksuccess_view, name='feedbacksuccess'),  # Feedback success 
    path('couriers/', list_couriers, name='list_couriers'),
    path('about/', about, name='about'),
    path('logout/', logout_view, name='logout'),  # Custom logout view
    path('courier-success/', courier_success, name='courier_success'),
]