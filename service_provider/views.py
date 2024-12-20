from rest_framework.viewsets import ModelViewSet
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import (ServiceProvider,SPWorkTime,SPReview,SPRate,SPTag,SPCategory,Address
            ,SPWorkTime,SPImages,SPOwner,Expert,SPExpert)
from .serializers import(ServiceProviderSerializer, ServiceProviderShortSerializer,SPWorkTimeSerializer, SPWorkTimeWritableSerializer,SPReviewSerializer,
            SPRateSerializer,SPTagSerializer,SPCategorySerializer,AddressSerializer,SPImagesSerializer
            ,SPOwnerSerializer,ExpertSerializer,SPExpertSerializer)
from rest_framework.permissions import AllowAny, IsAuthenticated

class SPCategoryViewSet(ModelViewSet):
    """
    ViewSet برای مدیریت دسته‌بندی‌های ServiceProvider
    """
    queryset = SPCategory.objects.all()
    serializer_class = SPCategorySerializer
    permission_classes = [AllowAny]

class AddressViewSet(ModelViewSet):
    """
    ViewSet برای مدیریت آدرس‌ها
    """
    queryset = Address.objects.all()
    serializer_class = AddressSerializer
    permission_classes = [IsAuthenticated] 

class SPWorkTimeViewSet(ModelViewSet):
    """
    ViewSet برای مدیریت زمان‌های کاری
    """
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        sp_id = self.kSPWorkTimeViewSetwargs.get('sp_id')
        return SPWorkTime.objects.filter(SP_id=sp_id)

    def get_serializer_class(self):
        if self.action in ['create', 'update', 'partial_update']:
            return SPWorkTimeWritableSerializer
        return SPWorkTimeSerializer
    
class ServiceProviderViewSet(ModelViewSet):
    """
    ViewSet برای مدیریت ServiceProvider
    """
    queryset = ServiceProvider.objects.all()

    def get_queryset(self):
        """
        بازگرداندن داده‌ها بر اساس پارامترهای موجود در بدنه درخواست
        """
        if self.request.method == 'POST':  # درخواست‌های POST/PUT/PATCH
            category_id = self.request.data.get('category_id', None)
        else:  # برای GET
            category_id = self.request.data.get('category_id', None)

        if category_id:
            return ServiceProvider.objects.filter(category_id=category_id)
        return super().get_queryset()

    def get_serializer_class(self):
        if self.action in ['list']:
            return ServiceProviderShortSerializer
        return ServiceProviderSerializer

    def get_permissions(self):
        if self.action in ['list', 'retrieve']:
            return [AllowAny()]
        return [IsAuthenticated()]


    
class SPWorkTimeViewSet(ModelViewSet):
    """
    ViewSet برای مدیریت زمان‌های کاری (Work Times)
    """
    serializer_class = SPWorkTimeSerializer

    def get_queryset(self):
        sp_id = self.kwargs.get('sp_id')
        return SPWorkTime.objects.filter(SP_id=sp_id)

    def get_serializer_class(self):
        if self.action in ['create', 'update', 'partial_update']:
            return SPWorkTimeWritableSerializer
        return SPWorkTimeSerializer

class SPReviewViewSet(ModelViewSet):
    """
    ViewSet برای مدیریت نظرات (Reviews)
    """
    serializer_class = SPReviewSerializer

    def get_queryset(self):
        sp_id = self.kwargs.get('sp_id')
        return SPReview.objects.filter(SP_id=sp_id)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user, SP_id=self.kwargs['sp_id'])

class SPRateViewSet(ModelViewSet):
    """
    ViewSet برای مدیریت امتیازات (Ratings)
    """
    serializer_class = SPRateSerializer

    def get_queryset(self):
        sp_id = self.kwargs.get('sp_id')
        return SPRate.objects.filter(SP_id=sp_id)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user, SP_id=self.kwargs['sp_id'])

class SPRateViewSet(ModelViewSet):
    """
    ViewSet برای مدیریت امتیازات (Ratings)
    """
    serializer_class = SPRateSerializer

    def get_queryset(self):
        sp_id = self.kwargs.get('sp_id')
        return SPRate.objects.filter(SP_id=sp_id)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user, SP_id=self.kwargs['sp_id'])

class SPTagViewSet(ModelViewSet):
    """
    ViewSet برای مدیریت تگ‌ها
    """
    serializer_class = SPTagSerializer

    def get_queryset(self):
        sp_id = self.kwargs.get('sp_id')
        return SPTag.objects.filter(SP_id=sp_id)

    def perform_create(self, serializer):
        serializer.save(SP_id=self.kwargs['sp_id'])

class SPImagesViewSet(ModelViewSet):
    """
    ViewSet برای مدیریت تصاویر ServiceProvider
    """
    queryset = SPImages.objects.all()
    serializer_class = SPImagesSerializer
    permission_classes = [IsAuthenticated]

from .models import SPOwner

class SPOwnerViewSet(ModelViewSet):
    """
    ViewSet برای مدیریت مالکان ServiceProvider
    """
    queryset = SPOwner.objects.all()
    serializer_class = SPOwnerSerializer
    permission_classes = [IsAuthenticated]

class ExpertViewSet(ModelViewSet):
    """
    ViewSet برای مدیریت تخصص‌ها
    """
    queryset = Expert.objects.all()
    serializer_class = ExpertSerializer
    permission_classes = [AllowAny]

class SPExpertViewSet(ModelViewSet):
    """
    ViewSet برای مدیریت تخصص‌های ServiceProvider
    """
    serializer_class=[SPExpertSerializer]
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        sp_id = self.kwargs.get('sp_id')
        return SPExpert.objects.filter(SP_id=sp_id)

