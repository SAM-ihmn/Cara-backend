from django.db import models
from django.db import models
from django.conf import settings


class SPCategory(models.Model):
    name = models.CharField(max_length=255, unique=True, verbose_name="Category Name")
    icon = models.ImageField(upload_to='SPCategory_icons/', blank=True, null=True)

    class Meta:
        verbose_name = "Service Provider Category"
        verbose_name_plural = "Service Provider Categories"

    def __str__(self):
        return self.name


class City(models.Model):
    name = models.CharField(max_length=255, verbose_name="City Name")

    class Meta:
        verbose_name = "City"
        verbose_name_plural = "Cities"

    def __str__(self):
        return self.name


class Address(models.Model):
    district = models.CharField(max_length=255)
    city = models.ForeignKey(City, on_delete=models.DO_NOTHING, verbose_name="City")
    neighbourhood = models.CharField(max_length=150)
    full_address = models.CharField(max_length=255, verbose_name="Full Address")

    class Meta:
        verbose_name = "Address"
        verbose_name_plural = "Addresses"

    def __str__(self):
        return f"{self.full_address}, {self.neighbourhood}, {self.city.name}"


class Weekday(models.Model):
    name = models.CharField(max_length=50, unique=True)

    class Meta:
        verbose_name = "Weekday"
        verbose_name_plural = "Weekdays"

    def __str__(self):
        return self.name


class SPWorkTime(models.Model):
    SP = models.ForeignKey('ServiceProvider', on_delete=models.CASCADE, related_name='work_times')
    weekday = models.ForeignKey(Weekday, on_delete=models.CASCADE)
    time_start = models.TimeField()
    time_end = models.TimeField()
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Service Provider Work Time"
        verbose_name_plural = "Service Provider Work Times"

    def __str__(self):
        return f"{self.SP.name} - {self.weekday.name}: {self.time_start} to {self.time_end}"


class TagKey(models.Model):
    name = models.CharField(max_length=100, unique=True)

    class Meta:
        verbose_name = "Tag Key"
        verbose_name_plural = "Tag Keys"

    def __str__(self):
        return self.name


class SPTag(models.Model):
    SP = models.ForeignKey('ServiceProvider', on_delete=models.CASCADE, related_name='tags')
    key = models.ForeignKey(TagKey, on_delete=models.CASCADE, related_name='SP_tags')
    value = models.CharField(max_length=255)

    class Meta:
        verbose_name = "Service Provider Tag"
        verbose_name_plural = "Service Provider Tags"
        unique_together = ('SP', 'key', 'value')  # جلوگیری از تکراری بودن

    def __str__(self):
        return f"{self.SP.name} - {self.key.name}: {self.value}"
    
class CarCategory(models.Model):
    name=models.CharField(max_length=200)

class Car(models.Model):
    category = models.ForeignKey(CarCategory, on_delete=models.DO_NOTHING,null=True)
    brand = models.CharField(max_length=255)
    model = models.CharField(max_length=255)
    sub_model = models.CharField(max_length=255, blank=True, null=True)

    class Meta:
        verbose_name = "Car"
        verbose_name_plural = "Cars"

    def __str__(self):
        return f"{self.brand} {self.model} ({self.tag})"


class ServiceProvider(models.Model):
    name = models.CharField(max_length=255)
    logo_image = models.ImageField(upload_to='SP_logos/')
    main_image = models.ImageField(upload_to='SP_main_images/', blank=True, null=True)
    owner = models.ForeignKey('SPOwner', on_delete=models.CASCADE)
    address = models.ForeignKey(Address, on_delete=models.SET_NULL, null=True)
    category = models.ForeignKey(SPCategory, on_delete=models.SET_NULL, null=True)
    location = models.CharField(max_length=255)

    class Meta:
        verbose_name = "Service Provider"
        verbose_name_plural = "Service Providers"

    def __str__(self):
        return self.name


class SPImages(models.Model):
    SP = models.ForeignKey(ServiceProvider, on_delete=models.CASCADE, related_name='images')
    image = models.ImageField(upload_to='SP_images/')

    class Meta:
        verbose_name = "Service Provider Image"
        verbose_name_plural = "Service Provider Images"

    def __str__(self):
        return f"Image for {self.SP.name}"


class SPOwner(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

    class Meta:
        verbose_name = "Service Provider Owner"
        verbose_name_plural = "Service Provider Owners"

    def __str__(self):
        return self.user.username


class SPReview(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    SP = models.ForeignKey(ServiceProvider, on_delete=models.CASCADE, related_name='reviews')
    title = models.CharField(max_length=255)
    description = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True)

    class Meta:
        verbose_name = "Service Provider Review"
        verbose_name_plural = "Service Provider Reviews"

    def __str__(self):
        return f"Review by {self.user.username} for {self.SP.name}"


class SPRate(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True)
    SP = models.ForeignKey(ServiceProvider, on_delete=models.CASCADE, related_name='rates')
    score = models.IntegerField(choices=[(i, str(i)) for i in range(1, 6)])

    class Meta:
        verbose_name = "Service Provider Rating"
        verbose_name_plural = "Service Provider Ratings"

    def __str__(self):
        return f"{self.score} for {self.SP.name}"


class Expert(models.Model):
    name = models.CharField(max_length=255)
    spcategory=models.ForeignKey(SPCategory,on_delete=models.CASCADE,related_name='expertise',null=True)
    icon = models.ImageField(upload_to='expert_icons/', blank=True, null=True)

    class Meta:
        verbose_name = "Expert"
        verbose_name_plural = "Experts"

    def __str__(self):
        return self.name


class SPExpert(models.Model):
    SP = models.ForeignKey(ServiceProvider, on_delete=models.CASCADE, related_name='expertises')
    expert = models.ForeignKey(Expert, on_delete=models.CASCADE, related_name='SPs')
    is_active = models.BooleanField(default=True)

    class Meta:
        verbose_name = "Service Provider Expertise"
        verbose_name_plural = "Service Provider Expertises"

    def __str__(self):
        return f"{self.SP.name} - {self.expert.name}"


class SPCarExpert(models.Model):
    SP = models.ForeignKey(ServiceProvider, on_delete=models.CASCADE)
    car = models.ForeignKey(Car, on_delete=models.CASCADE)
    expert = models.ForeignKey(Expert, on_delete=models.CASCADE)

    class Meta:
        verbose_name = "Service Provider Car Expertise"
        verbose_name_plural = "Service Provider Car Expertises"

    def __str__(self):
        return f"{self.expert.name} expertise for {self.car.brand}"

class Gifts(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()

class SPGifts(models.Model):
    sp_id=models.ForeignKey(ServiceProvider,on_delete=models.CASCADE)
    gift_id=models.ForeignKey(Gifts,on_delete=models.CASCADE)
    amout=models.FloatField()


# class GaragePriceRange(models.Model):
#     price_start = models.DecimalField(max_digits=10, decimal_places=2)
#     price_end = models.DecimalField(max_digits=10, decimal_places=2)
#     garage_car_expert = models.ForeignKey(GarageCarExpert, on_delete=models.CASCADE)
#     service = models.ForeignKey('Services', on_delete=models.CASCADE)
#     is_active = models.BooleanField(default=True)

#     def __str__(self):
#         return f"{self.price_start} - {self.price_end} for {self.service.name}"

