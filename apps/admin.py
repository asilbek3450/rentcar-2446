from django.contrib import admin
from django.utils.html import format_html
from django.urls import reverse
from django.utils.safestring import mark_safe
from django.utils import timezone
from .models import Brand, Car, RentCar


@admin.register(Brand)
class BrandAdmin(admin.ModelAdmin):
    list_display = ['name', 'car_count', 'created_at']
    search_fields = ['name']
    list_filter = ['created_at']
    
    def car_count(self, obj):
        return obj.cars.count()
    car_count.short_description = "Avtomobillar soni"


@admin.register(Car)
class CarAdmin(admin.ModelAdmin):
    list_display = ['name', 'brand', 'year', 'price_per_day', 'status', 'is_featured', 'image_preview']
    list_filter = ['brand', 'status', 'fuel_type', 'transmission', 'is_featured', 'year']
    search_fields = ['name', 'brand__name', 'description']
    readonly_fields = ['created_at', 'updated_at', 'image_preview']
    fieldsets = (
        ('Asosiy ma\'lumotlar', {
            'fields': ('brand', 'name', 'year', 'price_per_day', 'image', 'image_preview')
        }),
        ('Texnik xususiyatlar', {
            'fields': ('mileage', 'fuel_type', 'transmission', 'seats', 'color')
        }),
        ('Qo\'shimcha', {
            'fields': ('description', 'status', 'is_featured', 'created_at', 'updated_at')
        }),
    )
    
    def image_preview(self, obj):
        if obj.image:
            return format_html('<img src="{}" style="max-width: 200px; max-height: 200px;" />', obj.image.url)
        return "Rasm yo'q"
    image_preview.short_description = "Rasm ko'rinishi"


@admin.register(RentCar)
class RentCarAdmin(admin.ModelAdmin):
    list_display = ['id', 'full_name', 'phone', 'car', 'start_date', 'end_date', 'total_price', 'status_badge', 'created_at']
    list_filter = ['status', 'created_at', 'start_date']
    search_fields = ['full_name', 'phone', 'email', 'car__name']
    readonly_fields = ['created_at', 'updated_at', 'total_days', 'total_price']
    fieldsets = (
        ('Ariza ma\'lumotlari', {
            'fields': ('car', 'full_name', 'phone', 'email', 'start_date', 'end_date', 'total_days', 'total_price', 'message')
        }),
        ('Boshqarish', {
            'fields': ('status', 'admin_notes', 'created_at', 'updated_at')
        }),
    )
    actions = ['approve_rentals', 'reject_rentals']
    
    def status_badge(self, obj):
        colors = {
            'pending': 'warning',
            'approved': 'success',
            'rejected': 'danger',
            'completed': 'info',
        }
        color = colors.get(obj.status, 'secondary')
        return format_html(
            '<span class="badge badge-{}">{}</span>',
            color,
            obj.get_status_display()
        )
    status_badge.short_description = "Holat"
    
    @admin.action(description='Tanlangan arizalarni tasdiqlash')
    def approve_rentals(self, request, queryset):
        updated = queryset.filter(status='pending').update(
            status='approved',
            admin_notes=f"Tasdiqlandi: {request.user.username} tomonidan {timezone.now().strftime('%Y-%m-%d %H:%M')}"
        )
        self.message_user(request, f'{updated} ta ariza tasdiqlandi.')
    
    @admin.action(description='Tanlangan arizalarni rad etish')
    def reject_rentals(self, request, queryset):
        updated = queryset.filter(status='pending').update(
            status='rejected',
            admin_notes=f"Rad etildi: {request.user.username} tomonidan {timezone.now().strftime('%Y-%m-%d %H:%M')}"
        )
        self.message_user(request, f'{updated} ta ariza rad etildi.')
