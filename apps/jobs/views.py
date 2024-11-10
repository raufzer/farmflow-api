from django.shortcuts import get_object_or_404, render
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from .models import Job
from .serializers import JobSerializer
from rest_framework.permissions import IsAuthenticated
from rest_framework.pagination import PageNumberPagination
from rest_framework import status
from .filters import JobFilter

# Create your views here.

# Create
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def create_job(request):
    job_data = request.data
    job_serializer = JobSerializer(data=job_data)

    if job_serializer.is_valid():
        job = Job.objects.create(**job_data, user=request.user)
        res = JobSerializer(Job, many=False)
        return ({"Job": res.data}, status.HTTP_201_CREATED)
    else:
        return Response(job_serializer.errors,status=status.HTTP_400_BAD_REQUEST)
    
# Read    
@api_view(['GET'])
def get_all_jobs(request):
    paginator = PageNumberPagination()
    paginator.page_size = 1
    filterset = JobFilter(request.GET,queryset=Job.objects.all().order_by('id'))

    queryset = paginator.paginate_queryset(filterset.qs, request)
    job_serializer = JobSerializer(queryset, many=True)

    return Response({"Jobs": job_serializer.data},status=status.HTTP_200_OK)


@api_view(['GET'])
def get_by_id_job(request, pk):
    job = get_object_or_404(Job, pk=pk)
    job_serializer = JobSerializer(Job, many=False)

    return Response({"Job": job_serializer.data},status=status.HTTP_200_OK)

# Update
@api_view(['PUT'])
@permission_classes([IsAuthenticated])
def update_job(request, pk):
    job = get_object_or_404(Job, id=pk)

    if job.user != request.user:
        return Response({'error': 'You are not allowed to update this job'},status=status.HTTP_401_UNAUTHORIZED)

    job.Job_job = request.data['Job_job']
    job.location = request.data['location']
    job.studies_degree = request.data['studies_degree']
    job.contact_number = request.data['contact_number']
    job.save()

    job.save()
    job_serializer = JobSerializer(Job, many=False)
    return Response({"Job": job_serializer.data},status=status.HTTP_200_OK)


# delete
@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def delete_job(request, pk):
    job = get_object_or_404(Job, pk=pk)

    if job.user != request.user:
        return Response({'error': 'You are not allowed to delete this job'},status=status.HTTP_401_UNAUTHORIZED)

    job.delete()
    return Response({'details': 'job deleted successfully'},status=status.HTTP_200_OK)