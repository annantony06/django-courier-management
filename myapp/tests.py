from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User
from .models import Package, Courier, Feedback
from .forms import PackageForm, CourierForm, FeedbackForm

class UserRegistrationTestCase(TestCase):
    def setUp(self):
        self.valid_data = {
            'username': 'testuser',
            'email': 'testuser@example.com',
            'password': 'password123',
            'password_confirm': 'password123',
        }

    def test_user_registration(self):
        response = self.client.post(reverse('signup'), self.valid_data)
        self.assertEqual(response.status_code, 302)  # Redirect after successful registration
        self.assertTrue(User.objects.filter(username='testuser').exists())

class PackageTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='password123')
        self.courier = Courier.objects.create(user=self.user, name='Courier 1', email='courier1@example.com', phone_number='1234567890', current_location='City, State', latitude=0.0, longitude=0.0)

    def test_package_creation(self):
        package_data = {
            'courier': self.courier,
            'sender': self.user,
            'recipient': self.user,
            'description': 'Test Package',
            'weight': 1.5,
            'status': 'Pending',
        }
        response = self.client.post(reverse('package_create'), package_data)
        self.assertEqual(response.status_code, 302)  # Redirect after successful creation
        self.assertTrue(Package.objects.filter(description='Test Package').exists())

class CourierTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='password123')

    def test_courier_creation(self):
        courier_data = {
            'user': self.user,
            'name': 'Courier 1',
            'email': 'courier1@example.com',
            'phone_number': '1234567890',
            'current_location': 'City, State',
            'latitude': 0.0,
            'longitude': 0.0,
            'status': 'Pending',
            'source': 'Source Address',
            'destination': 'Destination Address',
            'time_slot': '10:00 AM - 12:00 PM',
        }
        response = self.client.post(reverse('courier_create'), courier_data)
        self.assertEqual(response.status_code, 302)  # Redirect after successful creation
        self.assertTrue(Courier.objects.filter(name='Courier 1').exists())

class FeedbackTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='password123')
        self.package = Package.objects.create(courier=Courier.objects.create(user=self.user, name='Courier 1', email='courier1@example.com', phone_number='1234567890', current_location='City, State', latitude=0.0, longitude=0.0), sender=self.user, recipient=self.user, description='Test Package', weight=1.5)

    def test_feedback_submission(self):
        feedback_data = {
            'package': self.package,
            'user': self.user,
            'rating': 5,
            'comments': 'Great service!',
        }
        response = self.client.post(reverse('feedback_create'), feedback_data)
        self.assertEqual(response.status_code, 302)  # Redirect after successful submission
        self.assertTrue(Feedback.objects.filter(comments='Great service!').exists())

class PackageFormTestCase(TestCase):
    def test_package_form_valid(self):
        form_data = {
            'courier': 1,  # Assuming a courier with ID 1 exists
            'sender': 1,   # Assuming a user with ID 1 exists
            'recipient': 1,  # Assuming a user with ID 1 exists
            'description': 'Test Package',
            'weight': 1.5,
            'status': 'Pending',
        }
        form = PackageForm(data=form_data)
        self.assertTrue(form.is_valid())

class FeedbackFormTestCase(TestCase):
    def test_feedback_form_valid(self):
        form_data = {
            'package': 1,  # Assuming a package with ID 1 exists
            'user': 1,     # Assuming a user with ID 1 exists
            'rating': 5,
            'comments': 'Great service!',
        }
        form = FeedbackForm(data=form_data)
        self.assertTrue(form.is_valid())