from rest_framework.serializers import ModelSerializer
from api_service.models import CustomUser

class CustomUserSerializer(ModelSerializer):
    """Serializers for customuser model """
    class Meta:
        model = CustomUser
        fields = "__all__"