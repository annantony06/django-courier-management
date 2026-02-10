from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm # <-- This comma is causing the error
from django.core.mail import send_mail
from django.utils.crypto import get_random_string
from .models import Delivery, Courier  # Assuming you have a Delivery and Courier model
from django.http import HttpResponse
from .forms import FeedbackForm
from datetime import datetime
from django.contrib.auth import logout
from django.shortcuts import redirect
from django.contrib.auth.views import LoginView
from django.contrib.auth.decorators import login_required
from .models import Package, Courier 
from .models import PaymentHistory 
import logging
from django.db.models import Q
from .models import Feedback 

logger = logging.getLogger(__name__)

def logout_view(request):
    logout(request)  # Log the user out
    return redirect('myapp:index')
def index(request):
    return render(request, 'myapp/index.html')
def index(request):
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)  # Log the user in
                messages.success(request, 'Login successful!')
                return redirect('myapp:dashboard')  # Redirect to the dashboard or home page
            else:
                messages.error(request, 'Invalid username or password.')
    else:
        form = AuthenticationForm()  # Create an empty form

    return render(request, 'myapp/index.html', {'form': form})
class CustomLoginView(LoginView):
    template_name = 'myapp/index.html'  # Specify your login template

    def get_success_url(self):
        return '/' 
def home_view(request):
    return render(request, 'myapp/index.html')  
def signup(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Signup successful! You can now log in.')
            return redirect('myapp:signin')  # Redirect to the sign-in page
    else:
        form = UserCreationForm()
    return render(request, 'myapp/signup.html', {'form': form})
def signin(request):
    """Render the welcome user page."""
    return render(request, 'myapp/signin.html') 
def forgot(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        new_password = request.POST.get('new_password')

        try:
            # Find the user by email
            user = User.objects.get(email=email)
            # Update the user's password
            user.set_password(new_password)
            user.save()
            messages.success(request, "Your password has been reset successfully.")
            return redirect('myapp:signin')  # Redirect to the sign-in page after resetting the password
        except User.DoesNotExist:
            messages.error(request, "No user found with this email address.")
        except Exception as e:
            messages.error(request, "An error occurred while resetting the password. Please try again.")

    return render(request, 'myapp/forget.html')  # Render the passw
# Reset password page
def resetpassword(request, token):
    if request.method == 'POST':
        # Handle password reset logic here (e.g., update password in database)
        messages.success(request, 'Your password has been reset!')
        return redirect('signin')
    return render(request, 'myapp/resetpassword.html', {'token': token})
def dashboard(request):
    """Render the welcome user page."""
    return render(request, 'myapp/dashboard.html') #ass the username to the templateo the template 
# Add Package page
# views.py
from django.shortcuts import render, redirect
from .models import Courier, Package
from django.contrib.auth.models import User

# Add Package View
# myapp/views.py
from django.shortcuts import render, redirect
from .models import Package
from .forms import PackageForm  # Assuming you're using a form class

def add_package(request):
    if request.method == 'POST':
        form = PackageForm(request.POST)
        if form.is_valid():
            package = form.save(commit=False)
            package.user = request.user  # If user is logged in
            package.save()
            return render(request, 'myapp/couriersucess.html') # or any success URL
    else:
        form = PackageForm()

    return render(request, 'myapp/addpackage.html', {'form': form})


def courier_success(request):
    return render(request, 'myapp/couriersucess.html')  #
    #
def payment(request):
    # Retrieve package details from the session
    package_details = request.session.get('package_details', {})
    amount = 100.00  # Set a default amount or calculate based on package details

    if request.method == 'POST':
        card_number = request.POST.get('card_number')
        expiry_date = request.POST.get('expiry_date')
        cvv = request.POST.get('cvv')

        # Here you would typically handle the payment processing logic
        # For example, you could integrate with a payment gateway API

        # Simulate payment processing
        payment_successful = True  # Change this based on actual payment processing logic

        if payment_successful:
            # Save package and courier information
            try:
                # Create and save package and courier instances
                # (Your existing logic here)

                # Send delivery link to the destination user
                send_delivery_link(package_details.get('destination_email'), package_details)

                messages.success(request, 'Payment successful! Your package has been added.')
                
                # Clear the package details from the session after payment
                if 'package_details' in request.session:
                    del request.session['package_details']

                logger.info("Payment processed successfully, redirecting to success page.")
                return redirect('myapp:paymentsuccess')  # Redirect to the paymentsuccess page
            except Exception as e:
                messages.error(request, f'An error occurred while processing your payment: {e}')
                logger.error(f"Error during payment processing: {e}")
                return redirect('myapp:payment')  # Redirect back to the payment page
        else:
            messages.error(request, 'Payment failed. Please try again.')
            logger.warning("Payment failed.")
            return redirect('myapp:payment')  # Redirect back to the payment page

    # If it's a GET request, render the payment page with the amount and package details
    return render(request, 'myapp/payment.html', {'amount': amount, 'package_details': package_details})

def paymentsuccess(request):
    """View to display the payment success message."""
    return render(request, 'myapp/paymentsuccess.html')

# Function to send delivery link
def send_delivery_link(destination_email, package_details):
    token = get_random_string(32)  # Generate a secure token
    link = f"http://yourdomain.com/schedule-delivery/?email={destination_email}&token={token}"  # Replace with your domain

    subject = "Select Your Delivery Time Slot"
    message = f"Please click the following link to select your delivery time slot: {link}"
    from_email = "from@example.com"  # Replace with your email
    recipient_list = [destination_email]

    try:
        send_mail(subject, message, from_email, recipient_list)
    except Exception as e:
        # Log the error or handle it as needed
        print(f"Error sending email: {str(e)}")

# Schedule Delivery page
def schedule_delivery(request):
    email = request.GET.get('email')
    token = request.GET.get('token')

    # Validate the token and email (you may want to implement token expiration)
    if email and token:
        return render(request, 'myapp/scheduledelivery.html', {'email': email})
    else:
        messages.error(request, 'Invalid link or token.')
        return redirect('myapp:dashboard')

# Handle the time slot selection
def handle_time_slot_selection(request):
    if request.method == 'POST':
        email = request.POST['email']
        time_slot = request.POST['time_slot']

        # Here you would typically save the selected time slot to the Delivery model
        # Assuming you have a Delivery model with a field for scheduled_time
        delivery = get_object_or_404(Delivery, destination_user__email=email)  # Adjust as needed
        delivery.scheduled_time = time_slot
        delivery.save()

        messages.success(request, 'Delivery time scheduled successfully!')
        return redirect('myapp:dashboard')

    return render(request, 'myapp/scheduledelivery.html')

def track_page(request):
    courier_id = request.GET.get('courier_id')
    courier_name = request.GET.get('courier_name')

    # Fetch the courier data from the database
    if courier_id and courier_name:
        try:
            courier = Courier.objects.get(id=courier_id, name=courier_name)
            # Prepare the context dictionary to pass data to the template
            context = {
                'courier': courier,  # Pass the fetched courier data to the template
            }
            return render(request, 'myapp/track.html', context)
        except Courier.DoesNotExist:
            # Handle case where courier is not found
            context = {'error': 'Courier not found'}
            return render(request, 'myapp/track.html', context)
    else:
        # Handle missing courier_id or courier_name
        context = {'error': 'Invalid courier details'}
        return render(request, 'myapp/track.html', context)
# Track Courier logic
def track_courier(request):
    courier_id = request.GET.get('courier_id')
    courier_name = request.GET.get('courier_name')
    
    # Check if the courier_id or courier_name is empty
    if not courier_id or not courier_name:
        return render(request, 'myapp/track.html', {'error': 'Courier ID or name is missing.'})
    
    # Ensure courier_id is a number
    try:
        courier_id = int(courier_id)
    except ValueError:
        return render(request, 'myapp/track.html', {'error': 'Invalid Courier ID.'})
    
    # Now filter the Courier model with the extracted parameters
    courier = Courier.objects.filter(id=courier_id, name__iexact=courier_name).first()
    
    if courier:
        # Pass the courier object to the template
        return render(request, 'myapp/leaflet.html', {'courier': courier})
    else:
        return render(request, 'myapp/track.html', {'error': 'No courier matches the given query.'})
@login_required
def feedback_view(request):
    if request.method == 'POST':
        form = FeedbackForm(request.POST)
        if form.is_valid():
            # Create the user's feedback
            Feedback.objects.create(
                user=request.user,
                feedback_text=form.cleaned_data['feedback_text'],
                refund_requested=form.cleaned_data['refund_requested'],
            )
            
            # Create default feedback for a specific user (e.g., a staff user)
            default_user = User.objects.filter(is_staff=True).first()  # Get the first staff user
            if default_user:
                Feedback.objects.create(
                    user=default_user,
                    feedback_text='Default feedback for staff',  # Customize this message
                    refund_requested=False,  # Set default value for refund_requested
                )
            
            messages.success(request, 'Thank you for your feedback!')
            return redirect('myapp:feedbacksuccess')
        else:
            # If the form is not valid, you can add error messages
            messages.error(request, 'There was an error with your feedback. Please try again.')
    else:
        form = FeedbackForm()
    return render(request, 'myapp/feedback.html', {'form': form})

@login_required
def feedback_list_view(request):
    feedbacks = Feedback.objects.all()
    return render(request, 'staff/feedback.html', {'feedbacks': feedbacks})
@login_required
def feedbacksuccess_view(request): #Added feedback_success view
    return render(request, 'myapp/feedbacksuccess.html')
def list_couriers(request):
    user = User.objects.get(id=1)  # Temporarily hardcoded for testing
    couriers = Courier.objects.filter(user=user)
    return render(request, 'myapp/listcouriers.html', {'couriers': couriers})

def about(request):
    current_year = datetime.now().year
    return render(request, 'myapp/about.html', {'current_year': current_year})