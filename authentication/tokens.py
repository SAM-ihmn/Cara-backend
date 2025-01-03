from rest_framework_simplejwt.tokens import RefreshToken
from django.utils.translation import gettext_lazy as _

def generate_tokens_for_user(user):

    refresh = RefreshToken.for_user(user)
    return {
        'refresh': str(refresh),
        'access': str(refresh.access_token),
    }