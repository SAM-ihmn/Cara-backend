from django.contrib import admin
from .models import (
    ServiceProvider, SPCategory, Address, SPWorkTime, SPTag, TagKey, SPImages, SPOwner,
    SPReview, SPRate, Expert, SPExpert, SPCarExpert
)

@admin.register(SPCategory)
class SPCategoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'icon')  
    search_fields = ('name',)  
    list_per_page = 20  

@admin.register(Address)
class AddressAdmin(admin.ModelAdmin):
    list_display = ('id', 'district', 'city', 'neighbourhood', 'full_address')
    search_fields = ('district', 'city__name', 'neighbourhood', 'full_address')
    list_filter = ('city',)  
    list_per_page = 20


@admin.register(ServiceProvider)
class ServiceProviderAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'owner', 'category', 'address', 'location')
    search_fields = ('name', 'category__name', 'owner__user__username')
    list_filter = ('category', 'location')
    list_per_page = 20


@admin.register(SPWorkTime)
class SPWorkTimeAdmin(admin.ModelAdmin):
    list_display = ('id', 'SP', 'weekday', 'time_start', 'time_end', 'is_active')
    search_fields = ('SP__name', 'weekday__name')
    list_filter = ('weekday', 'is_active')
    list_per_page = 20


@admin.register(SPTag)
class SPTagAdmin(admin.ModelAdmin):
    list_display = ('id', 'SP', 'key', 'value')
    search_fields = ('SP__name', 'key__name', 'value')
    list_filter = ('key',)
    list_per_page = 20


@admin.register(TagKey)
class TagKeyAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')
    search_fields = ('name',)
    list_per_page = 20


@admin.register(SPImages)
class SPImagesAdmin(admin.ModelAdmin):
    list_display = ('id', 'SP', 'image')
    search_fields = ('SP__name',)
    list_per_page = 20


@admin.register(SPOwner)
class SPOwnerAdmin(admin.ModelAdmin):
    list_display = ('id', 'user')
    search_fields = ('user__username',)
    list_per_page = 20


@admin.register(SPReview)
class SPReviewAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'SP', 'title', 'created_at', 'is_active')
    search_fields = ('user__username', 'SP__name', 'title')
    list_filter = ('is_active', 'created_at')
    list_per_page = 20


@admin.register(SPRate)
class SPRateAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'SP', 'score')
    search_fields = ('user__username', 'SP__name')
    list_filter = ('score',)
    list_per_page = 20


@admin.register(Expert)
class ExpertAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'icon')
    search_fields = ('name',)
    list_per_page = 20


@admin.register(SPExpert)
class SPExpertAdmin(admin.ModelAdmin):
    list_display = ('id', 'SP', 'expert', 'is_active')
    search_fields = ('SP__name', 'expert__name')
    list_filter = ('is_active',)
    list_per_page = 20


@admin.register(SPCarExpert)
class SPCarExpertAdmin(admin.ModelAdmin):
    list_display = ('id', 'SP', 'car', 'expert')
    search_fields = ('SP__name', 'car__brand', 'expert__name')
    list_filter = ('car__tag',)
    list_per_page = 20