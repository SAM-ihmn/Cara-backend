from faker import Faker
from django.contrib.auth import get_user_model
from service_provider.models import (
    SPCategory, City, Address, ServiceProvider, SPWorkTime, SPTag, SPImages, SPOwner, SPReview, SPRate,
    Expert, SPExpert, SPCarExpert, CarCategory, Car, TagKey, Weekday, Gifts, SPGifts
)
import random
from django.db import transaction

fake = Faker()

# Function to create fake SPCategory
def create_fake_spcategory():
    while True:
        name = f"{fake.word()}_{random.randint(1, 10000)}"
        if not SPCategory.objects.filter(name=name).exists():
            break
    category = SPCategory.objects.create(
        name=name,
        icon=None  # Add logic for image if needed
    )
    return category

# Function to create fake City
def create_fake_city():
    city = City.objects.create(name=fake.city())
    return city

# Function to create fake Address
def create_fake_address():
    city = create_fake_city()
    address = Address.objects.create(
        district=fake.street_name(),
        city=city,
        neighbourhood=fake.word(),
        full_address=fake.address()
    )
    return address

# Function to create fake SPOwner
def create_fake_spowner():
    User = get_user_model()
    user, _ = User.objects.get_or_create(
        username=fake.user_name(),
        defaults={"email": fake.email(), "password": "securepassword"}
    )
    sp_owner = SPOwner.objects.create(user=user)
    return sp_owner

# Function to create fake ServiceProvider
def create_fake_service_provider():
    owner = create_fake_spowner()
    address = create_fake_address()
    category = create_fake_spcategory()
    service_provider = ServiceProvider.objects.create(
        name=fake.company(),
        logo_image=None,  # Add logic for image if needed
        main_image=None,  # Add logic for image if needed
        owner=owner,
        address=address,
        category=category,
        location=f"{fake.latitude()}, {fake.longitude()}"
    )
    return service_provider

# Function to create fake Weekday
def create_fake_weekday():
    days = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
    for day in days:
        Weekday.objects.get_or_create(name=day)

# Function to create fake SPWorkTime
def create_fake_spworktime(service_provider):
    weekdays = Weekday.objects.all()
    for _ in range(2):  # Two time slots per provider
        SPWorkTime.objects.create(
            SP=service_provider,
            weekday=random.choice(weekdays),
            time_start=fake.time(),
            time_end=fake.time(),
            is_active=True
        )

# Function to create fake TagKey
def create_fake_tagkey():
    tag_key = TagKey.objects.create(name=fake.word())
    return tag_key

# Function to create fake SPTag
def create_fake_sptag(service_provider):
    key = create_fake_tagkey()
    SPTag.objects.create(
        SP=service_provider,
        key=key,
        value=fake.word()
    )

# Function to create fake SPImages
def create_fake_spimages(service_provider):
    SPImages.objects.create(
        SP=service_provider,
        image=None  # Add logic for image if needed
    )

# Function to create fake SPReview
def create_fake_spreview(service_provider):
    User = get_user_model()
    user, _ = User.objects.get_or_create(
        username=fake.user_name(),
        defaults={"email": fake.email(), "password": "securepassword"}
    )
    SPReview.objects.create(
        user=user,
        SP=service_provider,
        title=fake.sentence(),
        description=fake.paragraph(),
        is_active=True
    )

# Function to create fake SPRate
def create_fake_sprate(service_provider):
    User = get_user_model()
    user, _ = User.objects.get_or_create(
        username=fake.user_name(),
        defaults={"email": fake.email(), "password": "securepassword"}
    )
    SPRate.objects.create(
        user=user,
        SP=service_provider,
        score=random.randint(1, 5)
    )

# Function to create fake Expert
def create_fake_expert():
    spcategory = create_fake_spcategory()  # ایجاد یک دسته‌بندی جدید برای Expert
    expert = Expert.objects.create(
        name=fake.name(),
        spcategory=spcategory,  # ارتباط Expert با دسته‌بندی
        icon=None  # افزودن تصویر اگر نیاز باشد
    )
    return expert


# Function to create fake SPExpert
def create_fake_spexpert(service_provider):
    expert = create_fake_expert()
    SPExpert.objects.create(
        SP=service_provider,
        expert=expert,
        is_active=True
    )


# Function to create fake CarCategory and Car
def create_fake_car():
    car_category = CarCategory.objects.create(name=fake.word())
    car = Car.objects.create(
        category=car_category,
        brand=fake.company(),
        model=fake.word(),
        sub_model=fake.word()
    )
    return car

# Function to create fake SPCarExpert
def create_fake_spcarexpert(service_provider):
    car = create_fake_car()  # ایجاد یک Car جدید
    expert = create_fake_expert()  # ایجاد یک Expert جدید
    SPCarExpert.objects.create(
        SP=service_provider,
        car=car,
        expert=expert
    )

def create_fake_gift():
    gift = Gifts.objects.create(
        name=fake.word(),
        description=fake.paragraph()
    )
    return gift

# ایجاد داده فیک برای SPGifts
def create_fake_spgift(service_provider):
    gift = create_fake_gift()
    SPGifts.objects.create(
        sp_id=service_provider,
        gift_id=gift,
        amout=random.uniform(10, 500)  # مقدار عددی تصادفی
    )
# Main function for creating fake data
def run():
    print("Creating fake data...")
    create_fake_weekday()  # Ensure weekdays are pre-created

    with transaction.atomic():
        for _ in range(10):  # Number of service providers to create
            service_provider = create_fake_service_provider()
            create_fake_spworktime(service_provider)
            create_fake_sptag(service_provider)
            create_fake_spimages(service_provider)
            create_fake_spreview(service_provider)
            create_fake_sprate(service_provider)
            create_fake_spexpert(service_provider)
            create_fake_spcarexpert(service_provider)
            create_fake_spgift(service_provider)  # اضافه کردن SPGifts

    print("Fake data creation completed.")