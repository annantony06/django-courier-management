from django import forms  # Import forms module
from django.db import models
from django.contrib.auth.models import User
from .models import Feedback, Courier, Package  
from .models import Staff# Import the Feedback model


class FeedbackForm(forms.ModelForm):  # Define the FeedbackForm class
    class Meta:
        model = Feedback
        fields = ['feedback_text', 'refund_requested']
        widgets = {
            'feedback_text': forms.Textarea(attrs={'rows': 4, 'placeholder': 'Enter your feedback here...'}),
            'refund_requested': forms.CheckboxInput(),
        }


class CourierForm(models.Model):  # Define the Courier model (this is a model, not a form)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    current_location = models.CharField(max_length=255)
    status = models.CharField(max_length=50)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

class PackageForm(forms.ModelForm):
    class Meta:
        model = Package
        fields = ['tracking_number', 'status', 'description', 'pickup_location', 'delivery_address',
                  'weight', 'height', 'source_email', 'source_phone', 'source_address', 'destination_email',
                  'destination_phone', 'destination_address', 'pickup_time', 'delivery_time']
        widgets = {
            'status': forms.Select(choices=Package.STATUS_CHOICES),
            'description': forms.Textarea(attrs={'rows': 3}),
            'pickup_location': forms.TextInput(attrs={'placeholder': 'Optional'}),
            'delivery_address': forms.TextInput(attrs={'placeholder': 'Optional'}),
            'pickup_time': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
            'delivery_time': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
        }
class StaffForm(forms.ModelForm):
    class Meta:
        model = Staff  # Specify your model
        exclude = ['password'] 