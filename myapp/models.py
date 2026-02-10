from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from staff.models import Staff


# Avoid circular imports by referencing the model as a string
# Define choices for statuses
STATUS_CHOICES = [
    ('picked_up', 'Picked Up'),
    ('in_transit', 'In Transit'),
    ('delivered', 'Delivered'),
    ('on_hold', 'On Hold'),
]

class Courier(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    current_location = models.CharField(max_length=255)
    status = models.CharField(max_length=50, choices=STATUS_CHOICES)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.name} - {self.status}"
class Staff(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    username = models.CharField(max_length=100)

    def __str__(self):
        return self.user.username 
class Package(models.Model):
    # Define status choices at the class level
    PENDING = 'PENDING'
    IN_TRANSIT = 'IN_TRANSIT'
    DELIVERED = 'DELIVERED'

    STATUS_CHOICES = [
        (PENDING, 'Pending'),
        (IN_TRANSIT, 'In Transit'),
        (DELIVERED, 'Delivered'),
    ]
    
    tracking_number = models.CharField(max_length=100)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default=PENDING)
    description = models.TextField()
    pickup_location = models.CharField(max_length=255)
    delivery_address = models.CharField(max_length=255)
    weight = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    height = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    source_email = models.EmailField(null=True, blank=True)
    source_phone = models.CharField(max_length=15, null=True, blank=True)
    source_address = models.CharField(max_length=255, null=True, blank=True)
    destination_email = models.EmailField(null=True, blank=True)
    destination_phone = models.CharField(max_length=15, null=True, blank=True)
    destination_address = models.CharField(max_length=255, null=True, blank=True)
    pickup_time = models.DateTimeField(null=True, blank=True)
    delivery_time = models.DateTimeField(null=True, blank=True)
    
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user_packages')
    staff = models.ForeignKey('Staff', on_delete=models.CASCADE, null=True, blank=True, related_name='staff_packages')

    # Automatically set these fields when the package is created or updated
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.tracking_number

class Delivery(models.Model):
    package = models.ForeignKey(Package, on_delete=models.CASCADE)
    courier = models.ForeignKey(Courier, on_delete=models.CASCADE, default=1)
    scheduled_time = models.DateTimeField()
    delivered = models.BooleanField(default=False)
    delivered_at = models.DateTimeField(null=True, blank=True)

class Tracking(models.Model):
    courier = models.ForeignKey(Courier, on_delete=models.CASCADE)
    tracking_id = models.CharField(max_length=100, unique=True)
    status = models.CharField(max_length=50)
    location = models.CharField(max_length=255)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Tracking ID: {self.tracking_id} - {self.status}"

class Feedback(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='myapp_feedback')
    feedback_text = models.TextField()
    refund_requested = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Feedback from {self.user.username} on {self.created_at}"

class PaymentHistory(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    payment_date = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=50, choices=[  
        ('pending', 'Pending'),
        ('completed', 'Completed'),
        ('failed', 'Failed'),
    ])
    courier = models.ForeignKey(Courier, on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self):
        return f"Payment of {self.amount} by {self.user.username} on {self.payment_date} - Status: {self.status}"
