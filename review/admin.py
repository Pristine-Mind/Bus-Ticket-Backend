from django.contrib import admin

from .models import FeedbackReview, FAQ


class FeedbackReviewAdmin(admin.ModelAdmin):
    list_display = ("user", "title", "rating", "created_at", "updated_at")
    search_fields = ("title", "content", "user__username")
    list_filter = ("rating", "created_at", "user")
    readonly_fields = ("created_at", "updated_at")


class FAQAdmin(admin.ModelAdmin):
    list_display = ("question", "created_at", "updated_at")
    search_fields = ("question", "answer")
    list_filter = ("created_at",)
    readonly_fields = ("created_at", "updated_at")


admin.site.register(FeedbackReview, FeedbackReviewAdmin)
admin.site.register(FAQ, FAQAdmin)
