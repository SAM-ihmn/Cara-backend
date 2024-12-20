from rest_framework import serializers
from .models import (
    SPCategory, City, Address, Weekday, SPWorkTime, TagKey, SPTag, CarCategory, Car,
    ServiceProvider, SPImages, SPOwner, SPReview, SPRate, Expert, SPExpert, SPCarExpert
)
from django.db.models import Exists, OuterRef

class SPCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = SPCategory
        fields = '__all__'


class AddressSerializer(serializers.ModelSerializer):
    city_name = serializers.CharField(source='city.name', read_only=True)

    class Meta:
        model = Address
        fields = ['id', 'district', 'city', 'city_name', 'full_address']


class SPWorkTimeSerializer(serializers.ModelSerializer):
    weekday_name = serializers.CharField(source='weekday.name', read_only=True)

    class Meta:
        model = SPWorkTime
        fields = ['id', 'weekday', 'weekday_name', 'time_start', 'time_end', 'is_active']

class SPWorkTimeWritableSerializer(serializers.ModelSerializer):
    class Meta:
        model = SPWorkTime
        fields = ['weekday', 'time_start', 'time_end', 'is_active']

class SPTagSerializer(serializers.ModelSerializer):
    key_name = serializers.CharField(source='key.name')  # نام key

    class Meta:
        model = SPTag
        fields = ['key_name', 'value']


class SPImagesSerializer(serializers.ModelSerializer):
    class Meta:
        model = SPImages
        fields = ['image']


class SPOwnerSerializer(serializers.ModelSerializer):
    username = serializers.CharField(source='user.username', read_only=True)
    
    class Meta:
        model = SPOwner
        fields = ['username']


class SPReviewSerializer(serializers.ModelSerializer):
    username = serializers.CharField(source='user.username', read_only=True)

    class Meta:
        model = SPReview
        fields = ['username', 'title', 'description', 'created_at', 'is_active']


class SPRateSerializer(serializers.ModelSerializer):
    username = serializers.CharField(source='user.username', read_only=True)

    class Meta:
        model = SPRate
        fields = ['username', 'score']


class ExpertSerializer(serializers.ModelSerializer):
    class Meta:
        model = Expert
        fields = ['name', 'icon']


class SPExpertSerializer(serializers.ModelSerializer):
    expert = ExpertSerializer(read_only=True)

    class Meta:
        model = SPExpert
        fields = ['expert', 'is_active']

class ServiceProviderSerializer(serializers.ModelSerializer):
    category = SPCategorySerializer(read_only=True)
    address = AddressSerializer(read_only=True)
    owner = SPOwnerSerializer(read_only=True)
    work_times = SPWorkTimeSerializer(many=True, read_only=True)
    tags = SPTagSerializer(many=True, read_only=True)
    images = SPImagesSerializer(many=True, read_only=True)
    reviews = SPReviewSerializer(many=True, read_only=True)
    rates = SPRateSerializer(many=True, read_only=True)
    expertises = SPExpertSerializer(many=True, read_only=True)
    average_rating = serializers.SerializerMethodField() 
    user_review = serializers.SerializerMethodField()
    user_rate = serializers.SerializerMethodField()

    class Meta:
        model = ServiceProvider
        fields = [
            'id',
            'name',
            'logo_image',
            'main_image',
            'owner',
            'address',
            'category',
            'location',
            'work_times',
            'tags',
            'images',
            'reviews',
            'user_rate',
            'rates',
            'user_review',
            'expertises',
            'average_rating'
        ]

    def get_average_rating(self, obj):
        rates = obj.rates.all()
        if rates.exists():
            return sum(rate.score for rate in rates) / rates.count()
        return None
    
    def get_user_review(self, obj):
        """
        این متد کامنت‌ها را بر اساس وجود نمره مرتب می‌کند
        """
        user_rates = SPRate.objects.filter(SP=obj, user=OuterRef('user'))
        reviews = obj.reviews.annotate(has_rate=Exists(user_rates)).order_by('-has_rate')
        return SPReviewSerializer(reviews, many=True).data

    def get_user_rate(self, obj):
        user = self.context.get('request').user
        if user.is_authenticated:
            rate = obj.rates.filter(user=user).first()
            return SPRateSerializer(rate).data if rate else None
        return None

        
class ServiceProviderShortSerializer(serializers.ModelSerializer):
    category_name = serializers.CharField(source='category.name', read_only=True)
    rate_count = serializers.IntegerField(source='rates.count', read_only=True)
    user_rate = serializers.SerializerMethodField()
    tags = serializers.SerializerMethodField()

    class Meta:
        model = ServiceProvider
        fields = [
            'id',
            'name',
            'logo_image',
            'main_image',
            'category_name',
            'rate_count',
            'user_rate', 
            'tags', 
        ]

    def get_user_rate(self, obj): 
        rates = obj.rates.all()
        if rates.exists():
            return sum(rate.score for rate in rates) / rates.count()
        return None

    def get_tags(self, obj):
        tags = obj.tags.select_related('key').all()
        return [{
            'key': tag.key.name,
            'value': tag.value
        } for tag in tags]

