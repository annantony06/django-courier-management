from django.contrib import admin
from django.urls import path, include
from myapp.views import index  # Import your index view

urlpatterns = [
    path('admin/', admin.site.urls),  # Admin interface
    path('', index, name='home'),  # Add this line to handle the root URL
    path('myapp/', include(('myapp.urls', 'myapp'), namespace='myapp')),  # Include myapp URLs with namespace
    path('staff/', include(('staff.urls', 'staff'), namespace='staff')),  # Include staff URLs with namespace
]