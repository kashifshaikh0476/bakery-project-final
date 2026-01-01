import json
from django.contrib import admin
from django.core.serializers.json import DjangoJSONEncoder
from django.contrib.auth.models import Group
from .models import Product, Feedback, Order

# 1. Admin Header Setup
admin.site.site_header = "A1 Bakery Administration"
admin.site.site_title = "A1 Bakery Admin"
admin.site.index_title = "Dashboard"

# 2. Faltu 'Groups' hata diya
admin.site.unregister(Group)

# 3. Product Admin
@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'price', 'image_tag')
    search_fields = ('name',)
    
    def image_tag(self, obj):
        from django.utils.html import format_html
        if obj.image:
            return format_html('<img src="{}" style="width: 40px; height: 40px; border-radius: 5px;" />', obj.image.url)
        return "-"
    image_tag.short_description = 'Image'

# 4. Order Admin
@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('id', 'customer_name', 'status', 'user')
    list_filter = ('status',)
    search_fields = ('customer_name',)

# 5. FEEDBACK ADMIN (Charts + Read Only) 📊
@admin.register(Feedback)
class FeedbackAdmin(admin.ModelAdmin):
    list_display = ('customer_name', 'rating_stars', 'message_preview', 'created_at')
    list_filter = ('rating', 'created_at')
    search_fields = ('customer_name', 'message')
    readonly_fields = ('customer_name', 'email', 'rating', 'message', 'created_at')

    # === YE LINE CHART DIKHAYEGI ===
    change_list_template = "admin/feedback_chart.html"

    # === BUTTONS GAYAB KARNE KA LOGIC ===
    def has_add_permission(self, request):
        return False
    def has_change_permission(self, request, obj=None):
        return False

    # Rating Stars Display
    def rating_stars(self, obj):
        return "⭐" * obj.rating
    rating_stars.short_description = "Rating"

    def message_preview(self, obj):
        return obj.message[:60] + "..." if obj.message else ""

    # === CHART DATA CALCULATION ===
    def changelist_view(self, request, extra_context=None):
        # Good/Medium/Bad count karo
        good = Feedback.objects.filter(rating__gte=4).count()
        medium = Feedback.objects.filter(rating=3).count()
        bad = Feedback.objects.filter(rating__lte=2).count()

        # JSON Data Banao
        chart_data = json.dumps({
            "good": good,
            "medium": medium,
            "bad": bad,
        }, cls=DjangoJSONEncoder)

        extra_context = extra_context or {"chart_data": chart_data}
        return super().changelist_view(request, extra_context=extra_context)