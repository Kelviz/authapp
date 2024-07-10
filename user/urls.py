from django.urls import path, include
from rest_framework import routers
from .views import RegisterView, LoginView, UserListAndDetailView, UserOrganizationView, home

router = routers.DefaultRouter(trailing_slash=False)

router.register('users', UserListAndDetailView,
                basename="users")
router.register('organisations', UserOrganizationView,
                basename="organisations")

urlpatterns = [
    path('', home, name="home"),
    path('auth/register', RegisterView.as_view(), name='register'),
    path('auth/login', LoginView.as_view(), name='login'),
    path('api/', include(router.urls)),
]
