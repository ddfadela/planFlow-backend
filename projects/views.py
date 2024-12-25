from rest_framework import status
from rest_framework.decorators import api_view, permission_classes, parser_classes
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.parsers import MultiPartParser, FormParser
from django.shortcuts import get_object_or_404
from .models import Project
from .serializers import ProjectSerializer
from django.http import HttpResponse
from .utils import create_project_pdf

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def project_list(request):
    """Get all projects for the authenticated user"""
    projects = Project.objects.filter(user=request.user)
    serializer = ProjectSerializer(projects, many=True)
    return Response(serializer.data)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
@parser_classes([MultiPartParser, FormParser])
def project_create(request):
    """Create a new project"""
    serializer = ProjectSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save(user=request.user)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def project_detail(request, pk):
    """Retrieve a project by its ID"""
    project = get_object_or_404(Project, pk=pk, user=request.user)
    serializer = ProjectSerializer(project)
    return Response(serializer.data)

@api_view(['PUT'])
@permission_classes([IsAuthenticated])
@parser_classes([MultiPartParser, FormParser])
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
    return Response({"detail": "Project deleted successfully."}, status=status.HTTP_204_NO_CONTENT)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def export_project_pdf(request, pk):
    """Export project details as PDF"""
    project = get_object_or_404(Project, pk=pk, user=request.user)
    
    try:
        pdf = create_project_pdf(project)
        
        response = HttpResponse(pdf, content_type='application/pdf')
        response['Content-Disposition'] = f'attachment; filename="project_{project.id}.pdf"'
        
        return response
    except Exception as e:
        return Response(
            {"error": "Failed to generate PDF"},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )