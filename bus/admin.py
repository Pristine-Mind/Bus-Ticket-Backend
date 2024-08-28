from django.contrib import admin

from .models import Booking, BookingDetail, Bus, BusRoute, Route


class BusAdmin(admin.ModelAdmin):
    list_display = ("bus_number", "bus_type", "capacity", "availability_status")
    list_filter = ("bus_type", "availability_status")
    search_fields = ("bus_number",)
    ordering = ("bus_number",)


class RouteAdmin(admin.ModelAdmin):
    list_display = ("start_location", "end_location", "scheduled_time")
    search_fields = ("start_location", "end_location")
    ordering = ("start_location", "end_location")


class BusRouteAdmin(admin.ModelAdmin):
    list_display = ("bus", "route", "date", "available_seats")
    list_filter = ("date", "bus__bus_type", "route__start_location", "route__end_location")
    search_fields = ("bus__bus_number", "route__start_location", "route__end_location")
    ordering = ("date",)


class BookingAdmin(admin.ModelAdmin):
    list_display = ("user", "booking_time")
    list_filter = ("booking_time", "user__username")
    search_fields = ("user__username",)
    ordering = ("-booking_time",)


class BookingDetailAdmin(admin.ModelAdmin):
    list_display = ("bus_route", "seat_numbers")
    list_filter = ("bus_route__date", "bus_route__bus__bus_type", "bus_route__route__start_location")
    search_fields = ("bus_route__bus__bus_number", "bus_route__route__start_location", "bus_route__route__end_location")
    ordering = ("bus_route__date",)


admin.site.register(Bus, BusAdmin)
admin.site.register(Route, RouteAdmin)
admin.site.register(BusRoute, BusRouteAdmin)
admin.site.register(Booking, BookingAdmin)
admin.site.register(BookingDetail, BookingDetailAdmin)
