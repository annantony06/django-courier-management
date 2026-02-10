from django.contrib import admin
from django.contrib.auth.models import User
from .models import Courier, Delivery, Feedback, Tracking, Branch, Refund, Franchise
from .models import Package, Staff

# Inline model for Feedback
class FeedbackInline(admin.TabularInline):
    model = Feedback
    extra = 0
    fields = ('content', 'created_at', 'refund_requested')  # Use the correct field name
    readonly_fields = ('created_at',)  # Make created_at read-only



# Custom User Admin to manage user details (staff)
class UserAdmin(admin.ModelAdmin):
    list_display = ('username', 'email', 'first_name', 'last_name', 'is_staff', 'is_active')
    list_filter = ('is_staff', 'is_active')
    search_fields = ('username', 'email', 'first_name', 'last_name')
    ordering = ('username',)
    inlines = [FeedbackInline]

# Unregister the default User admin
admin.site.unregister(User)
# Register the custom User admin
admin.site.register(User, UserAdmin)

# Admin for Courier
@admin.register(Courier)
class CourierAdmin(admin.ModelAdmin):
    list_display = ('name', 'current_location', 'status', 'user', 'created_at', 'updated_at')
    list_filter = ('status', 'user')
    search_fields = ('name', 'current_location')

# Admin for Package

# Admin for Delivery
@admin.register(Delivery)
class DeliveryAdmin(admin.ModelAdmin):
    list_display = ('package', 'courier', 'delivery_time', 'scheduled_date', 'delivered_at', 'status')
    list_filter = ('status', 'scheduled_date', 'delivered_at')
@admin.register(Feedback)
class FeedbackAdmin(admin.ModelAdmin):
    list_display = ('user', 'content', 'created_at', 'get_refund_status')  # Add refund status
    search_fields = ('user__username', 'content')
    list_filter = ('created_at',)

    def get_refund_status(self, obj):
        refund = Refund.objects.filter(feedback=obj).first()
        return refund.processed if refund else 'No refund'
    get_refund_status.short_description = 'Refund Status'
# Admin for Refund
@admin.register(Refund)
class RefundAdmin(admin.ModelAdmin):
    list_display = ('feedback', 'amount', 'reason', 'processed', 'created_at')
    list_filter = ('processed',)
    search_fields = ('feedback__user__username', 'reason')

# Admin for Branch
@admin.register(Branch)
class BranchAdmin(admin.ModelAdmin):
    list_display = ('name', 'location', 'contact_email', 'phone_number', 'operating_hours')
    search_fields = ('name', 'location')

# Admin for Franchise
@admin.register(Franchise)
class FranchiseAdmin(admin.ModelAdmin):
    list_display = ('name', 'location', 'contact_email', 'phone_number')
    search_fields = ('name', 'location')

# Admin for Tracking
@admin.register(Tracking)
class TrackingAdmin(admin.ModelAdmin):
    list_display = ['tracking_id', 'courier', 'package', 'status', 'updated_at']

class PackageAdmin(admin.ModelAdmin):
    list_display = ('tracking_number', 'status', 'sender', 'receiver', 'assigned_staff', 'created_at')  # Include assigned staff in list
    list_filter = ('status', 'sender', 'receiver', 'assigned_staff')  # Allow filtering by staff
    search_fields = ('tracking_number', 'sender__username', 'receiver__username')  # Search by tracking number, sender, and receiver

    # Add the assigned_staff field to the form for packages
    fieldsets = (
        (None, {
            'fields': ('tracking_number', 'sender', 'receiver', 'status', 'pickup_location', 'delivery_address', 'assigned_staff')
        }),
    )

admin.site.register(Package, PackageAdmin)
admin.site.register(Staff)