# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as DjangoUserAdmin

from django.utils.translation import gettext_lazy as _

from .models import Product, Order, User, OrderItem


# USER ADMIN 
@admin.register(User)
class UserAdmin(DjangoUserAdmin):
    """
    Admin configuration for the User model, adding
    fields, permissions, and inline Media.
    """
    fieldsets = (
        (None, {'fields': ('email', 'first_name', 'last_name', 'password')}),
        (_('Permissions'), {'fields': ('is_active', 'is_staff', 'is_superuser',
                                       'groups', 'user_permissions')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'password1', 'password2'),
        }),
    )
    list_display = ('email', 'first_name', 'last_name', 'is_active', 'is_staff')
    search_fields = ('email', 'first_name', 'last_name', 'is_active', 'is_staff')
    ordering = ('email',)
    readonly_fields = ('last_login',)



class ProductAdmin(admin.ModelAdmin):
    """
    Admin interface for managing Product records.
    Provides display, filtering, and search functionality in the Django admin.
    """

    # Display a hierarchical navigation bar based on the 'created_at' date
    date_hierarchy      = 'created_at'

    # Specifies the fields to display in the list view
    list_display        = ['title', 'price', 'is_active', 'created_at']
    list_display_links  = ['title',]
    list_filter         = ['title', 'is_active', 'created_at']
    search_fields       = ['request_id', 'is_active']
    list_per_page       = 50

    class Meta:
        # Links this admin class to the SMS model
        model = Product
admin.site.register(Product, ProductAdmin)


class OrderAdmin(admin.ModelAdmin):
    """
    Admin interface for managing Order records.
    Provides display, filtering, and search functionality in the Django admin.
    """

    # Display a hierarchical navigation bar based on the 'created_at' date
    date_hierarchy      = 'created_at'

    # Specifies the fields to display in the list view
    list_display        = ['user', 'reference', 'is_active', 'created_at']
    list_display_links  = ['user',]
    list_filter         = ['user', 'is_active', 'created_at']
    search_fields       = ['user__username', 'is_active']
    list_per_page       = 50

    class Meta:
        # Links this admin class to the SMS model
        model = Order
admin.site.register(Order, OrderAdmin)


class OrderItemAdmin(admin.ModelAdmin):
    """
    Admin interface for managing Order Item records.
    Provides display, filtering, and search functionality in the Django admin.
    """

    # Display a hierarchical navigation bar based on the 'created_at' date
    date_hierarchy      = 'created_at'

    # Specifies the fields to display in the list view
    list_display        = ['order', 'product', 'is_active', 'created_at']
    list_display_links  = ['order',]
    list_filter         = ['order', 'is_active', 'created_at']
    search_fields       = ['order', 'is_active']
    list_per_page       = 50

    class Meta:
        # Links this admin class to the SMS model
        model = OrderItem
admin.site.register(OrderItem, OrderItemAdmin)
