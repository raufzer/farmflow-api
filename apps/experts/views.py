from django.shortcuts import get_object_or_404, render
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from .models import Expert
from .serializers import ExpertSerializer
from rest_framework.permissions import IsAuthenticated
from rest_framework.pagination import PageNumberPagination
from rest_framework import status
from .filters import ExpertFilter

# Create your views here.

# Create
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def create_expert(request):
    expert_data = request.data
    expert_serializer = ExpertSerializer(data=expert_data)

    if expert_serializer.is_valid():
        expert = Expert.objects.create(**expert_data, user=request.user)
        res = ExpertSerializer(expert, many=False)
        return ({"expert": res.data}, status.HTTP_201_CREATED)
    else:
        return Response(expert_serializer.errors,status=status.HTTP_400_BAD_REQUEST)
    
# Read    
@api_view(['GET'])
def get_all_experts(request):
    paginator = PageNumberPagination()
    paginator.page_size = 1
    filterset = ExpertFilter(request.GET,queryset=Expert.objects.all().order_by('id'))

    queryset = paginator.paginate_queryset(filterset.qs, request)
    expert_serializer = ExpertSerializer(queryset, many=True)

    return Response({"experts": expert_serializer.data},status=status.HTTP_200_OK)


@api_view(['GET'])
def get_by_id_expert(request, pk):
    expert = get_object_or_404(Expert, pk=pk)
    expert_serializer = ExpertSerializer(expert, many=False)

    return Response({"expert": expert_serializer.data},status=status.HTTP_200_OK)

# Update
@api_view(['PUT'])
@permission_classes([IsAuthenticated])
def update_expert(request, pk):
    expert = get_object_or_404(Expert, id=pk)

    if expert.user != request.user:
        return Response({'error': 'You are not allowed to update this expert'},status=status.HTTP_401_UNAUTHORIZED)

    expert.expert_job = request.data['expert_job']
    expert.location = request.data['location']
    expert.studies_degree = request.data['studies_degree']
    expert.contact_number = request.data['contact_number']
    expert.save()

    expert.save()
    expert_serializer = ExpertSerializer(expert, many=False)
    return Response({"expert": expert_serializer.data},status=status.HTTP_200_OK)


# delete
@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def delete_expert(request, pk):
    expert = get_object_or_404(Expert, pk=pk)

    if expert.user != request.user:
        return Response({'error': 'You are not allowed to delete this expert'},status=status.HTTP_401_UNAUTHORIZED)

    expert.delete()
    return Response({'details': 'Expert deleted successfully'},status=status.HTTP_200_OK)