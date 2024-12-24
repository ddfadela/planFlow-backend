from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.shortcuts import get_object_or_404
from .models import Project
from .serializers import ProjectSerializer

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def project_list(request):
    """Get all projects for the authenticated user"""
    projects = Project.objects.filter(user=request.user)
    serializer = ProjectSerializer(projects, many=True)
    return Response(serializer.data)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def project_create(request):
    """Create a new project"""
    serializer = ProjectSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save(user=request.user)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['PUT'])
@permission_classes([IsAuthenticated])
def project_update(request, pk):
    """Update a project"""
    project = get_object_or_404(Project, pk=pk, user=request.user)
    serializer = ProjectSerializer(project, data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def project_delete(request, pk):
    """Delete a project"""
    project = get_object_or_404(Project, pk=pk, user=request.user)
    project.delete()
    return Response(status=status.HTTP_204_NO_CONTENT)
