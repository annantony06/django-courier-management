from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.core.mail import send_mail
from django.utils import timezone
from .models import Branch, Package, Feedback, Refund, Staff
from datetime import datetime
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm
from .models import Package
from django.core.mail import send_mail
from django.urls import reverse_lazy
from django.contrib.auth.views import PasswordResetView
from .forms import StaffLoginForm
from django.http import HttpResponseForbidden
from django.contrib.auth.decorators import login_required, user_passes_test
def is_staff(user):
    return user.groups.filter(name='Staff').exists()
def staff_login_view(request):
    if request.method == 'POST':
        form = StaffLoginForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('staff/staffsignin')  # Redirect to the dashboard after login
            else:
                messages.error(request, "Invalid username or password.")
    else:
        form = StaffLoginForm()
    
    return render(request, 'staff/staffindex.html', {'form': form})
def logout_view(request):
    logout(request)  # Log the user out
    return redirect('staff/staff')



def signin_view(request):
    """Render the welcome user page."""
    return render(request, 'staff/staffsignin.html') 

# Sign up view
def signup_view(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            try:
                send_mail(
                    'Welcome to Our Service',
                    'Thank you for signing up!',
                    'annaantony0306.com',  # Replace with your email
                    [user.email],
                    fail_silently=False,
                )
            except Exception as e:
                messages.error(request, f'An error occurred while sending the email: {str(e)}')
            messages.success(request, 'Registration successful! Please log in.')
            return redirect('signin')
    else:
        form = UserCreationForm()
    return render(request, 'staff/staffsignup.html', {'form': form})



def forgot_view(request):
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
            return redirect('staff')  # Redirect to the login page
        except User.DoesNotExist:
            messages.error(request, "No user found with this email address.")
        except Exception as e:
            messages.error(request, "An error occurred while resetting the password. Please try again.")

    return render(request, 'staff/staffforget.html')  # Ren


class CustomPasswordResetView(PasswordResetView):
    template_name = 'users/password_reset.html'
    email_template_name = 'users/password_reset_email.html'
    subject_template_name = 'users/password_reset_subject.txt'
    success_url = reverse_lazy('password_reset_done')

# Reset password view
def reset_view(request):
    return render(request, 'staff/staffreset.html')
@login_required
def dashboard_view(request):
    """Render the welcome user page."""
    return render(request, 'staff/staffdashboard.html')
# Branch management view
@login_required
def branches_view(request):
    branches = Branch.objects.all()
    current_year = datetime.now().year
    return render(request, 'staff/branches.html', {'branches': branches, 'current_year': current_year})

# Branch detail view
@login_required
def branch_detail_view(request, branch_id):
    branch = get_object_or_404(Branch, id=branch_id)
    current_year = datetime.now().year
    return render(request, 'staff/branch.html', {'branch': branch, 'current_year': current_year})
def manage_packages(request):
    if request.user.is_staff:
        # Retrieve all packages, no filtering on staff
        packages = Package.objects.all()

        # Debugging - optional: print info to console (can be removed in production)
        print(f"Logged-in staff: {request.user.username}")
        print(f"All packages count: {packages.count()}")

        return render(request, 'staff/managepackage.html', {'packages': packages})

    else:
        return HttpResponseForbidden("You don't have permission to view this page.")
    
@login_required
def update_package_status(request, tracking_number):
    package = get_object_or_404(Package, tracking_number=tracking_number)
    if request.method == 'POST':
        new_status = request.POST['status']
        package.status = new_status
        package.save()

        # Send notification email to the user
        try:
            send_mail(
                'Package Status Update',
                f'Your package {tracking_number} status has been updated to {new_status}.',
                'from@example.com',  # Replace with your email
                [package.user.email],
                fail_silently=False,
            )
        except Exception as e:
            messages.error(request, f'An error occurred while sending the email: {str(e)}')

        messages.success(request, 'Package status updated successfully!')
        return redirect('manage_packages')  # Redirect to manage packages view
    return render(request, 'staff/updatestatus.html', {'package': package})

# Feedback list view
@login_required
def feedback_list_view(request):
    # Add default feedback
    default_user = User.objects.first()  # Get the first user
    if default_user:
        Feedback.objects.get_or_create(
            user=default_user,
            content="good.",  # Set default feedback
            defaults={},
        )
    feedbacks = Feedback.objects.all()
    print(f"Number of feedback entries: {feedbacks.count()}")
    print(f"Current user: {request.user}, is_staff: {request.user.is_staff}")
    return render(request, 'staff/feedback.html', {'feedbacks': feedbacks})


# Feedback detail view
@login_required
def feedback_detail_view(request, feedback_id):
    feedback = get_object_or_404(Feedback, id=feedback_id)
    return render(request, 'staff/feedbackdetails.html', {'feedback': feedback})

# Request refund view
@login_required
def request_refund(request, feedback_id):
    feedback = get_object_or_404(Feedback, id=feedback_id)
    if request.method == 'POST':
        amount = request.POST['amount']
        reason = request.POST['reason']
        refund = Refund(feedback=feedback, amount=amount, reason=reason)
        refund.save()
        messages.success(request, 'Refund request submitted successfully.')
        return redirect('feedback_list')  # Redirect to feedback list after submitting the refund request
    return render(request, 'staff/feedbackrefund.html', {'feedback': feedback})

# User list view for staff
@login_required
def user_list_view(request):
    users = User.objects.all()  # Get all users
    return render(request, 'staff/userlist.html', {'users': users})

# About view
@login_required
def about_view(request):
    return render(request, 'staff/about.html')