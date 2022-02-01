from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework_simplejwt.views import TokenObtainPairView

from users.category_serializer import CategorySerializer
from users.models import Category
from users.user_token_serializer import MyTokenObtainPairSerializer
from utility.api_helper import api_response


class LoginView(TokenObtainPairView):
    serializer_class = MyTokenObtainPairSerializer


class ListCategoryView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, _request):
        categories = Category.objects.filter(status="ACTIVE")
        serialized = CategorySerializer(categories, many=True)

        return api_response(status.HTTP_200_OK, "Request successful", serialized.data)
