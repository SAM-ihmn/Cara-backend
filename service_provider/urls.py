from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    SPCategoryViewSet, AddressViewSet, SPWorkTimeViewSet, SPTagViewSet, SPImagesViewSet,
    SPOwnerViewSet, SPReviewViewSet, SPRateViewSet, ExpertViewSet, SPExpertViewSet,
    ServiceProviderViewSet
)

router = DefaultRouter()

# مسیرهای اصلی
router.register(r'service-providers', ServiceProviderViewSet, basename='service_provider')
router.register(r'categories', SPCategoryViewSet, basename='sp_category')
router.register(r'addresses', AddressViewSet, basename='address')
router.register(r'images', SPImagesViewSet, basename='sp_images')
router.register(r'owners', SPOwnerViewSet, basename='sp_owner')
router.register(r'experts', ExpertViewSet, basename='expert')

# مسیرهای مرتبط با ServiceProvider
router.register(r'service-providers/(?P<sp_id>\d+)/work-times', SPWorkTimeViewSet, basename='sp_work_time')
router.register(r'service-providers/(?P<sp_id>\d+)/tags', SPTagViewSet, basename='sp_tag')
router.register(r'service-providers/(?P<sp_id>\d+)/reviews', SPReviewViewSet, basename='sp_review')
router.register(r'service-providers/(?P<sp_id>\d+)/rates', SPRateViewSet, basename='sp_rate')
router.register(r'service-providers/(?P<sp_id>\d+)/experts', SPExpertViewSet, basename='sp_expert')

urlpatterns = [
    path('', include(router.urls)),
]
