from django.urls import path
from . import views
urlpatterns = [
    path("", views.ProductsListAPIView.as_view(), name="products_list"),
    path("<int:productId>/", views.ProductsDetailAPIView.as_view(),
         name="products_detail")
]
