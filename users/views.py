from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404
from rest_framework import generics, permissions
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework_simplejwt.tokens import RefreshToken
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorato
from rest_framework import status


from .serializers import (
    RegisterSerializer,
    UserSerializer,
    CustomTokenObtainPairSerializer,
)

User = get_user_model()


@method_decorator(csrf_exempt, name='dispatch')
class RegisterView(APIView):
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        serializer = RegisterSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            return Response(UserSerializer(user).data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class CustomLoginView(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer
    permission_classes = [permissions.AllowAny]

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        access = serializer.validated_data.get("access")
        refresh = serializer.validated_data.get("refresh")

        response = Response({
            "message": "You have been successfully logged in",
            "user": serializer.validated_data.get("user"),
        })

        response["Authorization"] = f"Bearer {access}"
        response["X-Refresh-Token"] = str(refresh)
        return response


class UserMeView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        serializer = UserSerializer(request.user)
        return Response(serializer.data)


class LogoutView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        try:
            refresh_token = request.data["refresh"]
            token = RefreshToken(refresh_token)
            token.blacklist()
            return Response({"detail": "Logout successful"}, status=205)
        except Exception as e:
            return Response({"error": str(e)}, status=400)


class UserListView(generics.ListAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated, permissions.IsAdminUser]


class UserDeleteView(generics.DestroyAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated, permissions.IsAdminUser]
    lookup_field = 'id'


class AvailableDriverView(APIView):
    permission_classes = [permissions.AllowAny]  # Adjust for production

    def get(self, request):
        driver = User.objects.filter(role='driver', is_available=True).order_by('current_parcels').first()
        if driver:
            return Response({'driver_id': driver.id})
        return Response({'error': 'No available drivers'}, status=404)


# Helper view for updating driver availability
class UpdateDriverAvailabilityView(APIView):
    def patch(self, request, driver_id, status):
        driver = get_object_or_404(User, id=driver_id, role='driver')
        if status == 'unavailable':
            driver.is_available = False
        elif status == 'available':
            driver.is_available = True
        else:
            return Response({'error': 'Invalid status'}, status=400)
        driver.save()
        return Response({'message': f'Driver marked {status}'})
