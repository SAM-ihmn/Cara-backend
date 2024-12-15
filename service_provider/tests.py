from rest_framework.test import APITestCase
from rest_framework import status
from django.contrib.auth.models import User
from .models import (
    SPCategory, Address, City, SPWorkTime, Weekday, SPTag, TagKey,
    ServiceProvider, SPOwner, SPReview, SPRate, Expert, SPExpert
)
