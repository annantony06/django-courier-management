from django.contrib import admin
from django.contrib.auth.models import User
from .models import Courier, Package, Delivery, Feedback, Tracking, Staff

# Inline model for Feedback
class FeedbackInline(admin.TabularInline):
    model = Feedback
    extra = 0
    fields = ('feedback_text', 'created_at', 'refund_requested')
    readonly_fields = ('created_at',)

# Inline model for Package
class PackageInline(admin.TabularInline):
    model = Package
    extra = 0
    fields = ('tracking_number', 'status', 'pickup_location', 'delivery_address')
    readonly_fields = ('tracking_number', 'status', 'pickup_location', 'delivery_address')

# Custom User Admin
class UserAdmin(admin.ModelAdmin):
    list_display = ('username', 'email', 'first_name', 'last_name', 'is_staff', 'is_active')
    list_filter = ('is_staff', 'is_active')
    search_fields = ('username', 'email', 'first_name', 'last_name')
    ordering = ('username',)
    inlines = [FeedbackInline, PackageInline]

# Unregister default User admin and register custom one
admin.site.unregister(User)
admin.site.register(User, UserAdmin)

# Courier Admin
class CourierAdmin(admin.ModelAdmin):
    list_display = ('name', 'status', 'current_location', 'created_at')
    search_fields = ('name', 'status', 'current_location')
    ordering = ('name',)

admin.site.register(Courier, CourierAdmin)

# Feedback Admin
@admin.register(Feedback)
class FeedbackAdmin(admin.ModelAdmin):
    list_display = ('user', 'created_at', 'refund_requested')
    search_fields = ('user__username', 'feedback_text')

# Tracking Admin
@admin.register(Tracking)
class TrackingAdmin(admin.ModelAdmin):
    list_display = ('tracking_id', 'courier', 'status', 'location', 'updated_at')
    search_fields = ('tracking_id', 'courier__name', 'location')

# Package Admin
@admin.register(Package)
class PackageAdmin(admin.ModelAdmin):
    list_display = (
        'tracking_number', 'status', 'user', 'staff',
        'pickup_location', 'delivery_address'
    )
    list_filter = ('status', 'staff')
    search_fields = (
        'tracking_number', 'pickup_location', 'delivery_address',
        'source_email', 'destination_email'
    )
    ordering = ('-tracking_number',)
    fields = (
        'user', 'staff', 'tracking_number', 'status', 'description',
        'pickup_location', 'delivery_address', 'weight', 'height',
        'source_email', 'source_phone', 'source_address',
        'destination_email', 'destination_phone', 'destination_address',
        'pickup_time', 'delivery_time'
    )

# Staff Admin
class StaffAdmin(admin.ModelAdmin):
    list_display = ('get_user_username',)

    def get_user_username(self, obj):
        return obj.user.username if obj.user else None

    get_user_username.short_description = 'Username'

admin.site.register(Staff, StaffAdmin)

# Delivery Admin
class DeliveryAdmin(admin.ModelAdmin):
    list_display = ('package', 'courier', 'scheduled_time', 'delivered', 'delivered_at')
    list_filter = ('delivered', 'scheduled_time', 'delivered_at')
    search_fields = ('package__tracking_number', 'courier__name')

admin.site.register(Delivery, DeliveryAdmin)
