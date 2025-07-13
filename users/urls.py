from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView
from .views import (
    RegisterView,
    CustomLoginView,
    UserMeView,
    LogoutView,
    UserListView,
    UserDeleteView,
    AvailableDriverView,
    UpdateDriverAvailabilityView,
)

urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', CustomLoginView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('me/', UserMeView.as_view(), name='me'),
    path('available-driver/', AvailableDriverView.as_view(), name='available-driver'),

    path('<int:driver_id>/mark-<str:status>/', UpdateDriverAvailabilityView.as_view(), name='update-driver-status'),
    path('users/available-driver/', AvailableDriverView.as_view(), name='available-driver'),
    path('users/<int:driver_id>/mark-<str:status>/', UpdateDriverAvailabilityView.as_view(), name='update-driver-status'),
    # Admin-only
    path('', UserListView.as_view(), name='user-list'),
    path('<int:id>/', UserDeleteView.as_view(), name='user-delete'),
]
