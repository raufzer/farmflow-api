from django.shortcuts import render
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from .models import Product
from .serializers import ProductSerializer
from django.shortcuts import get_object_or_404
from rest_framework.permissions import IsAuthenticated
from .filters import ProductFilter
from rest_framework.pagination import PageNumberPagination
from rest_framework import status
# Create your views here.


# Create
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def create_product(request):
    product_data = request.data
    product_serializer = ProductSerializer(data=product_data)

    if product_serializer.is_valid():
        product = Product.objects.create(**product_data, user=request.user)
        res = ProductSerializer(product, many=False)
        return ({"product": res.data}, status.HTTP_201_CREATED)
    else:
        return Response(product_serializer.errors,status=status.HTTP_400_BAD_REQUEST)


# Read
@api_view(['GET'])
def get_all_products(request):
    paginator = PageNumberPagination()
    paginator.page_size = 1
    filterset = ProductFilter(request.GET,queryset=Product.objects.all().order_by('id'))

    queryset = paginator.paginate_queryset(filterset.qs, request)
    product_serializer = ProductSerializer(queryset, many=True)

    return Response({"products": product_serializer.data},status=status.HTTP_200_OK)


@api_view(['GET'])
def get_by_id_product(request, pk):
    product = get_object_or_404(Product, pk=pk)
    product_serializer = ProductSerializer(product, many=False)

    return Response({"product": product_serializer.data},status=status.HTTP_200_OK)


# Update
@api_view(['PUT'])
@permission_classes([IsAuthenticated])
def update_product(request, pk):
    product = get_object_or_404(Product, id=pk)

    if product.user != request.user:
        return Response({'error': 'You are not allowed to update this product'},status=status.HTTP_401_UNAUTHORIZED)

    product.name = request.data['name']
    product.category = request.data['category']
    product.description = request.data['description']
    product.rating = request.data['rating']
    product.price = request.data['price']
    product.status = request.data['status']
    product.location = request.data['location']
    product.stock = request.data['stock']

    product.save()
    product_serializer = ProductSerializer(product, many=False)
    return Response({"product": product_serializer.data},status=status.HTTP_200_OK)


# Delete
@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def delete_product(request, pk):
    product = get_object_or_404(Product, pk=pk)

    if product.user != request.user:
        return Response({'error': 'You are not allowed to delete this product'},status=status.HTTP_401_UNAUTHORIZED)

    product.delete()
    return Response({'details': 'Product deleted successfully'},status=status.HTTP_200_OK)
