from django.urls import path
from . import views
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)
urlpatterns = [
    path("login/", TokenObtainPairView.as_view(), name="login"),
    path("token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
    path("", views.AccountSiginAPIView.as_view(), name='sigin'),
    path("<str:username>/", views.AccountProfileAPIView.as_view(), name="profile"),
    path("del/<str:username>/", views.DelteUserAPIView.as_view(), name="delete"),
    path("update/password/", views.ChangePasswordAPIView.as_view(), name="password"),

]
