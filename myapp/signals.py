from django.db.models.signals import post_save
from django.dispatch import receiver
from django.core.mail import send_mail
from .models import Package

@receiver(post_save, sender=Package)
def notify_package_update(sender, instance, created, **kwargs):
    if created:
        subject = 'New Package Created'
        message = f'Your package from {instance.sender} to {instance.recipient} has been created. Status: {instance.status}'
        recipient_list = [instance.sender.email, instance.recipient.email]
        send_mail(subject, message, 'from@example.com', recipient_list)
    else:
        subject = 'Package Status Updated'
        message = f'Your package status has been updated to: {instance.status}'
        recipient_list = [instance.sender.email, instance.recipient.email]
        send_mail(subject, message, 'from@example.com', recipient_list)