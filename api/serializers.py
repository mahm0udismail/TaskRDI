from rest_framework import serializers
from .models import UploadedFile, ImageMetadata, PDFMetadata

class ImageMetadataSerializer(serializers.ModelSerializer):
    class Meta:
        model = ImageMetadata
        exclude = ['file']

class PDFMetadataSerializer(serializers.ModelSerializer):
    class Meta:
        model = PDFMetadata
        exclude = ['file']

class UploadedFileSerializer(serializers.ModelSerializer):
    image_id = serializers.SerializerMethodField()
    pdf_id = serializers.SerializerMethodField()

    class Meta:
        model = UploadedFile
        fields = ['image_id','pdf_id', 'file_type', 'file_path', 'uploaded_at']

    def get_image_id(self, obj):
        # Return the id of the related ImageMetadata, or None if not exists
        if hasattr(obj, 'imagemetadata'):
            return obj.imagemetadata.id
        return None
    
    def get_pdf_id(self, obj):
        # Return the id of the related PDFMetadata, or None if not exists
        if hasattr(obj, 'pdfmetadata'):
            return obj.pdfmetadata.id
        return None
    
    def to_representation(self, instance):
        # Get the serialized data
        data = super().to_representation(instance)

        # Remove image_id from fields if its value is None
        if data.get('image_id') is None:
            data.pop('image_id')

        # Remove pdf_metadata_id from fields if its value is None
        if data.get('pdf_id') is None:
            data.pop('pdf_id')

        return data