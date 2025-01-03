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
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi

class SPCategoryViewSet(ModelViewSet):
    """
    ViewSet برای مدیریت دسته‌بندی‌های ServiceProvider
    """
    queryset = SPCategory.objects.all()
    serializer_class = SPCategorySerializer
    permission_classes = [AllowAny]

    @swagger_auto_schema(
        operation_description="Retrieve all categories of Service Providers.",
        responses={
            200: "List of Service Provider categories.",
        }
    )
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_description="Create a new category for Service Providers.",
        responses={
            201: "Category created successfully.",
            400: "Invalid input data.",
        }
    )
    def create(self, request, *args, **kwargs):
        return super().create(request, *args, **kwargs)

class AddressViewSet(ModelViewSet):
    """
    ViewSet برای مدیریت آدرس‌ها
    """
    queryset = Address.objects.all()
    serializer_class = AddressSerializer
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(
        operation_description="Retrieve the list of addresses.",
        responses={
            200: "List of addresses.",
        }
    )
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_description="Create a new address.",
        responses={
            201: "Address created successfully.",
            400: "Invalid input data.",
        }
    )
    def create(self, request, *args, **kwargs):
        return super().create(request, *args, **kwargs)

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
    @swagger_auto_schema(
        operation_description="Retrieve a list of Service Providers with optional filtering by category.",
        manual_parameters=[
            openapi.Parameter(
                'category_id',
                openapi.IN_QUERY,
                description="Filter Service Providers by category ID.",
                type=openapi.TYPE_INTEGER
            ),
        ],
        responses={
            200: "List of Service Providers.",
        }
    )
    def get_queryset(self):
        """
        بازگرداندن داده‌ها بر اساس پارامترهای موجود در بدنه درخواست
        """
        if self.request.method == 'POST':  
            category_id = self.request.data.get('category_id', None)
        else:  
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
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(
        operation_description="Retrieve work times for a specific Service Provider.",
        manual_parameters=[
            openapi.Parameter(
                'sp_id',
                openapi.IN_QUERY,
                description="Service Provider ID to filter work times.",
                type=openapi.TYPE_INTEGER,
                required=True
            )
        ],
        responses={
            200: "List of work times for the specified Service Provider.",
        }
    )
    def get_queryset(self):
        sp_id = self.kwargs.get('sp_id')
        return SPWorkTime.objects.filter(SP_id=sp_id)

    @swagger_auto_schema(
        operation_description="Add or update a work time for a specific Service Provider.",
        responses={
            201: "Work time created/updated successfully.",
            400: "Invalid input data.",
        }
    )
    def get_serializer_class(self):
        if self.action in ['create', 'update', 'partial_update']:
            return SPWorkTimeWritableSerializer
        return SPWorkTimeSerializer

class SPReviewViewSet(ModelViewSet):
    """
    ViewSet برای مدیریت نظرات (Reviews)
    """
    serializer_class = SPReviewSerializer

    @swagger_auto_schema(
        operation_description="Retrieve reviews for a specific Service Provider.",
        responses={
            200: "List of reviews for the specified Service Provider.",
        }
    )

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
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(
        operation_description="Retrieve ratings for a specific Service Provider.",
        responses={
            200: "List of ratings for the specified Service Provider.",
        }
    )
    def get_queryset(self):
        sp_id = self.kwargs.get('sp_id')
        return SPRate.objects.filter(SP_id=sp_id)

    @swagger_auto_schema(
        operation_description="Submit a new rating for a specific Service Provider.",
        responses={
            201: "Rating created successfully.",
            400: "Invalid input data.",
        }
    )
    def perform_create(self, serializer):
        serializer.save(user=self.request.user, SP_id=self.kwargs['sp_id'])


class SPTagViewSet(ModelViewSet):
    """
    ViewSet برای مدیریت تگ‌ها
    """
    serializer_class = SPTagSerializer
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(
        operation_description="Retrieve the list of tags for a specific Service Provider.",
        responses={
            200: "List of tags for the specified Service Provider.",
        }
    )
    def get_queryset(self):
        sp_id = self.kwargs.get('sp_id')
        return SPTag.objects.filter(SP_id=sp_id)

    @swagger_auto_schema(
        operation_description="Add a new tag for a specific Service Provider.",
        responses={
            201: "Tag created successfully.",
            400: "Invalid input data.",
        }
    )
    def perform_create(self, serializer):
        serializer.save(SP_id=self.kwargs['sp_id'])

class SPImagesViewSet(ModelViewSet):
    """
    ViewSet برای مدیریت تصاویر ServiceProvider
    """
    queryset = SPImages.objects.all()
    serializer_class = SPImagesSerializer
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(
        operation_description="Retrieve images for all Service Providers.",
        responses={
            200: "List of Service Provider images.",
        }
    )
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_description="Upload an image for a specific Service Provider.",
        responses={
            201: "Image uploaded successfully.",
            400: "Invalid input data.",
        }
    )
    def create(self, request, *args, **kwargs):
        return super().create(request, *args, **kwargs)

class SPOwnerViewSet(ModelViewSet):
    """
    ViewSet برای مدیریت مالکان ServiceProvider
    """
    queryset = SPOwner.objects.all()
    serializer_class = SPOwnerSerializer
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(
        operation_description="Retrieve all owners of Service Providers.",
        responses={
            200: "List of owners.",
        }
    )
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_description="Assign a new owner to a Service Provider.",
        responses={
            201: "Owner assigned successfully.",
            400: "Invalid input data.",
        }
    )
    def create(self, request, *args, **kwargs):
        return super().create(request, *args, **kwargs)

class ExpertViewSet(ModelViewSet):
    """
    ViewSet برای مدیریت تخصص‌ها
    """
    queryset = Expert.objects.all()
    serializer_class = ExpertSerializer
    permission_classes = [AllowAny]

    @swagger_auto_schema(
        operation_description="Retrieve all experts.",
        responses={
            200: "List of experts.",
        }
    )
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_description="Create a new expert.",
        responses={
            201: "Expert created successfully.",
            400: "Invalid input data.",
        }
    )
    def create(self, request, *args, **kwargs):
        return super().create(request, *args, **kwargs)

class SPExpertViewSet(ModelViewSet):
    """
    ViewSet برای مدیریت تخصص‌های ServiceProvider
    """
    serializer_class = SPExpertSerializer
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(
        operation_description="Retrieve the list of experts for a specific Service Provider.",
        responses={
            200: "List of experts for the specified Service Provider.",
        }
    )
    def get_queryset(self):
        sp_id = self.kwargs.get('sp_id')
        return SPExpert.objects.filter(SP_id=sp_id)

    @swagger_auto_schema(
        operation_description="Assign an expert to a specific Service Provider.",
        responses={
            201: "Expert assigned successfully.",
            400: "Invalid input data.",
        }
    )
    def perform_create(self, serializer):
        serializer.save(SP_id=self.kwargs['sp_id'])
