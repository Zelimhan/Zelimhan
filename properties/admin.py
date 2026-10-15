from django.contrib import admin

from .models import Property, SelectionRequest


@admin.register(Property)
class PropertyAdmin(admin.ModelAdmin):
    list_display = (
        'title',
        'deal_type',
        'property_type',
        'city',
        'price',
        'area',
        'rooms',
        'status',
        'realtor',
        'created_at',
    )
    list_filter = ('status', 'deal_type', 'property_type', 'city')
    search_fields = ('title', 'address', 'city', 'description')
    list_editable = ('status',)
    autocomplete_fields = ('realtor',)
    readonly_fields = ('created_at', 'updated_at')
    fieldsets = (
        (None, {
            'fields': ('title', 'deal_type', 'property_type', 'status', 'realtor'),
        }),
        ('Характеристики', {
            'fields': ('price', 'area', 'rooms', 'floor', 'floors_total'),
        }),
        ('Расположение', {
            'fields': ('city', 'address'),
        }),
        ('Описание и фото', {
            'fields': ('description', 'photo'),
        }),
        ('Служебное', {
            'fields': ('created_at', 'updated_at'),
        }),
    )


@admin.register(SelectionRequest)
class SelectionRequestAdmin(admin.ModelAdmin):
    list_display = (
        'name',
        'phone',
        'deal_type',
        'property_type',
        'city',
        'budget_max',
        'status',
        'assigned_to',
        'created_at',
    )
    list_filter = ('status', 'deal_type', 'property_type')
    search_fields = ('name', 'phone', 'email', 'city', 'comment')
    list_editable = ('status',)
    autocomplete_fields = ('assigned_to',)
    readonly_fields = ('created_at',)
