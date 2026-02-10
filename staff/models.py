from django.db import models
from django.contrib.auth.models import User
from django.contrib.auth import get_user_model  # This is necessary for compatibility with custom User models

class Staff(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='staff_staff')  # Unique related_name
    # Other fields...

    def __str__(self):
        return self.user.username
# Package Model
class Package(models.Model):
    sender = models.ForeignKey(User, related_name='sent_packages', on_delete=models.CASCADE)
    receiver = models.ForeignKey(User, related_name='received_packages', on_delete=models.CASCADE)
    tracking_number = models.CharField(max_length=100, unique=True)
    status = models.CharField(max_length=50, choices=[
        ('pending', 'Pending'),
        ('in_transit', 'In Transit'),
        ('delivered', 'Delivered'),
        ('cancelled', 'Cancelled')
    ])
    pickup_location = models.CharField(max_length=255)
    delivery_address = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    # Removed redundant user field (sender and receiver are sufficient)
    assigned_staff = models.ForeignKey('Staff', null=True, blank=True, on_delete=models.SET_NULL)

    def __str__(self):
        return f"Package {self.tracking_number} - {self.status}"

# Feedback Model
class Feedback(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='feedbacks')
    content = models.TextField()  # Feedback content
    created_at = models.DateTimeField(auto_now_add=True)
    rating = models.PositiveIntegerField(default=1)  # Rating field

    def __str__(self):
        return f"Feedback from {self.user.username} at {self.created_at}"

# Refund Model
class Refund(models.Model):
    feedback = models.ForeignKey(Feedback, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    reason = models.TextField()
    processed = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'Refund for Feedback ID {self.feedback.id} - Amount: {self.amount} - Processed: {self.processed}'

# Courier Model
class Courier(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='couriers')
    name = models.CharField(max_length=100)
    current_location = models.CharField(max_length=255)
    status = models.CharField(max_length=50, choices=[
        ('picked_up', 'Picked Up'),
        ('in_transit', 'In Transit'),
        ('delivered', 'Delivered'),
        ('on_hold', 'On Hold')
    ])
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.name} - {self.status}"

# Branch Model
class Branch(models.Model):
    name = models.CharField(max_length=100)
    location = models.CharField(max_length=255)
    address = models.CharField(max_length=255, blank=True, null=True)
    contact_email = models.EmailField(blank=True, null=True)
    phone_number = models.CharField(max_length=20, blank=True, null=True)
    operating_hours = models.CharField(max_length=100, blank=True, null=True)

    def __str__(self):
        return self.name

# Franchise Model
class Franchise(models.Model):
    name = models.CharField(max_length=100)
    location = models.CharField(max_length=255)
    contact_email = models.EmailField(blank=True, null=True)
    phone_number = models.CharField(max_length=20, blank=True, null=True)

    def __str__(self):
        return self.name

# Tracking Model
class Tracking(models.Model):
    tracking_id = models.CharField(max_length=100)
    courier = models.ForeignKey(Courier, on_delete=models.CASCADE)  # Link to Courier, not User
    package = models.ForeignKey(Package, on_delete=models.CASCADE)
    status = models.CharField(max_length=50)
    updated_at = models.DateTimeField(auto_now=True)

# Delivery Model
class Delivery(models.Model):
    package = models.ForeignKey(Package, on_delete=models.CASCADE)
    courier = models.ForeignKey(Courier, on_delete=models.CASCADE)
    delivery_time = models.DateTimeField(auto_now_add=True)
    scheduled_date = models.DateTimeField(null=True, blank=True)
    delivered_at = models.DateTimeField(null=True, blank=True)
    status = models.CharField(max_length=50, choices=[
        ('pending', 'Pending'),
        ('in_progress', 'In Progress'),
        ('completed', 'Completed'),
        ('failed', 'Failed')
    ], default='pending')

    def __str__(self):
        return f"Delivery of {self.package.tracking_number} by {self.courier.name} - Status: {self.status}"
