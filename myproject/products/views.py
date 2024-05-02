from django.shortcuts import get_object_or_404, render
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import permission_classes
from .models import Product
from .serializers import ProductSerializer
from django.core.cache import cache


# Create your views here.


class ProductsListAPIView(APIView):
    # product 리스트
    def get(self, request):
        cache_key = "product_list"
        if not cache.get(cache_key):
            products = Product.objects.all()
            serializers = ProductSerializer(products, many=True)
            product_data = serializers.data
            cache.set(cache_key, product_data)

        product_data = cache.get(cache_key)
        return Response(product_data)

    @permission_classes([IsAuthenticated])  # 상품 등록
    def post(self, request):
        serializer = ProductSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save(account=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ProductsDetailAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get_object(self, productId):
        return get_object_or_404(Product, pk=productId)

    # 디테일 게시글

    def get(self, request, productId):
        product_de = self.get_object(productId)
        serializer = ProductSerializer(product_de)
        return Response(serializer.data)

    # 게시글 수정
    def put(self, request, productId):
        products = self.get_object(productId)
        user = request.user.id
        up_user = products.account.id
        print(user, up_user)
        if user == up_user:
            serializer = ProductSerializer(
                products, data=request.data, partial=True)
            if serializer.is_valid(raise_exception=True):
                serializer.save()
                return Response(serializer.data)
        return Response(status=status.HTTP_400_BAD_REQUEST)

        # 게시글 삭제
    def delete(self, request, productId):
        products = self.get_object(productId)
        user = request.user.id
        up_user = products.account.id
        print(user, up_user)
        if user == up_user:
            products.delete
            return Response(status=status.HTTP_204_NO_CONTENT)
        return Response(status=status.HTTP_400_BAD_REQUEST)
