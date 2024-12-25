from rest_framework import serializers
from .models import Project, ProjectImage

class ProjectImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProjectImage
        fields = ['id', 'image']

class ProjectSerializer(serializers.ModelSerializer):
    images = ProjectImageSerializer(many=True, read_only=True)
    image1 = serializers.ImageField(write_only=True, required=False)
    image2 = serializers.ImageField(write_only=True, required=False)

    class Meta:
        model = Project
        fields = ['id', 'title', 'description', 'start_date', 'end_date', 
                 'priority', 'category', 'status', 'created_at', 'updated_at',
                 'images', 'image1', 'image2']
        read_only_fields = ['created_at', 'updated_at']

    def validate(self, data):
        if data.get('start_date') and data.get('end_date'):
            if data['end_date'] < data['start_date']:
                raise serializers.ValidationError("End date must be after start date")
        return data

    def create(self, validated_data):
        image1 = validated_data.pop('image1', None)
        image2 = validated_data.pop('image2', None)
        
        project = Project.objects.create(**validated_data)
        
        if image1:
            ProjectImage.objects.create(
                project=project,
                image=image1,
            )
        if image2:
            ProjectImage.objects.create(
                project=project,
                image=image2,
            )
        return project

    def update(self, instance, validated_data):
        image1 = validated_data.pop('image1', None)
        image2 = validated_data.pop('image2', None)
        
        # Update project fields
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()
        
        # Update images
        if image1:
            ProjectImage.objects.filter(project=instance).delete()
            ProjectImage.objects.create(
                project=instance,
                image=image1,
            )
        if image2:
            ProjectImage.objects.filter(project=instance).delete()
            ProjectImage.objects.create(
                project=instance,
                image=image2,
                is_primary=False
            )
        return instance
