from django.contrib import admin

from .models import Reservation


class ReservationAdmin(admin.ModelAdmin):
    """
    Admin interface options for the Reservation model.
    """
    list_display = ('name', 'mobile_no', 'date_of_travel', 'duration_type', 'journey_from', 'journey_to', 'vehicle_type')
    list_filter = ('duration_type', 'vehicle_type', 'journey_from', 'journey_to', 'date_of_travel')
    search_fields = ('name', 'mobile_no', 'journey_from', 'journey_to')
    date_hierarchy = 'date_of_travel'
    ordering = ('-date_of_travel',)

    fieldsets = (
        (None, {
            'fields': ('name', 'mobile_no', 'date_of_travel', 'duration_type', 'passenger_numbers')
        }),
        ('Journey Details', {
            'fields': ('journey_from', 'journey_to', 'vehicle_type', 'comment'),
        }),
    )


admin.site.register(Reservation, ReservationAdmin)
