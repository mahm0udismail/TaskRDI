import base64
from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import UploadedFile, ImageMetadata, PDFMetadata
from .serializers import UploadedFileSerializer, ImageMetadataSerializer, PDFMetadataSerializer
from PIL import Image
from PyPDF2 import PdfReader
from io import BytesIO
import logging
import imghdr
import mimetypes
from pdf2image import convert_from_path

logger = logging.getLogger(__name__)


class UploadFileView(APIView):
    def post(self, request):
        file_data = request.data.get('file')
        file_type = request.data.get('file_type')

        if not file_data or not file_type:
            return Response({'error': 'File and file_type are required.'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            file_bytes = base64.b64decode(file_data)
            detected_extension = imghdr.what(None, h=file_bytes)
            if not detected_extension:
                mime_type = mimetypes.guess_type(f"dummy.{file_type}")[0]
                if mime_type:
                    detected_extension = mime_type.split('/')[-1]

            if not detected_extension:
                detected_extension = 'bin'

            file_name = f"uploads/{file_type}/{file_type}_{UploadedFile.objects.filter(file_type=file_type).count() + 1}.{detected_extension}"
            # file_name = f"uploads/{file_type}/{file_type}_{UploadedFile.objects.filter(file_type).count() + 1}"


            with open(file_name, 'wb') as f:
                f.write(file_bytes)

            uploaded_file = UploadedFile.objects.create(file_type=file_type, file_path=file_name)

            if file_type == 'image':
                image = Image.open(file_name)
                metadata = ImageMetadata.objects.create(
                    file=uploaded_file,
                    width=image.width,
                    height=image.height,
                    channels=len(image.getbands()),
                )
                image.close()

            elif file_type == 'pdf':
                pdf = PdfReader(BytesIO(file_bytes))
                page = pdf.pages[0]
                metadata = PDFMetadata.objects.create(
                    file=uploaded_file,
                    num_pages=len(pdf.pages),
                    page_width=page.mediabox.width,
                    page_height=page.mediabox.height,
                )

            return Response(UploadedFileSerializer(uploaded_file).data, status=status.HTTP_201_CREATED)

        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)

class ListUploudView(generics.ListAPIView):
    queryset = UploadedFile.objects.all()
    serializer_class = UploadedFileSerializer

class ListImagesView(generics.ListAPIView):
    queryset = UploadedFile.objects.filter(file_type='image')
    serializer_class = UploadedFileSerializer

class ListPDFsView(generics.ListAPIView):
    queryset = UploadedFile.objects.filter(file_type='pdf')
    serializer_class = UploadedFileSerializer

class ImageDetailView(generics.RetrieveAPIView):
    queryset = ImageMetadata.objects.all()
    serializer_class = ImageMetadataSerializer

class PDFDetailView(generics.RetrieveAPIView):
    queryset = PDFMetadata.objects.all()
    serializer_class = PDFMetadataSerializer

class DeleteImageView(generics.DestroyAPIView):
    queryset = UploadedFile.objects.filter(file_type='image')
    serializer_class = UploadedFileSerializer

class DeletePDFView(generics.DestroyAPIView):
    queryset = UploadedFile.objects.filter(file_type='pdf')
    serializer_class = UploadedFileSerializer

import logging

logger = logging.getLogger(__name__)

class RotateImageView(APIView):
    def post(self, request):
        image_id = request.data.get('image_id')
        angle = request.data.get('angle')

        if not image_id or not angle:
            return Response({'error': 'Image ID and angle are required.'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            image_metadata = ImageMetadata.objects.get(id=image_id)
            image_file = image_metadata.file

            with Image.open(image_file.file_path.path) as image:
                rotated_image = image.rotate(float(angle), expand=True)
                rotated_image.save(image_file.file_path.path)
            file_path = image_file.file_path.url
            return Response({
                'message': 'Image rotated successfully.',
                'file_path': file_path
            }, status=status.HTTP_200_OK)

        except ImageMetadata.DoesNotExist:
            return Response({'error': 'Image metadata not found.'}, status=status.HTTP_404_NOT_FOUND)

        except FileNotFoundError:
            return Response({'error': 'File not found.'}, status=status.HTTP_404_NOT_FOUND)

        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)
        

class ConvertPDFToImageView(APIView):
    def post(self, request):
        pdf_id = request.data.get('pdf_id')
        logger.error(pdf_id)
        if not pdf_id:
            logger.error('PDF ID is missing.')
            return Response({'error': 'PDF ID is required.'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            # Fetch the PDFMetadata object using the provided pdf_id
            pdf_metadata = PDFMetadata.objects.get(id=pdf_id)
            pdf_file = pdf_metadata.file  # Access the related UploadedFile object

            logger.info(f'Converting PDF file: {pdf_file.file_path.path}')
            
            # Convert all pages of the PDF
            images = convert_from_path(pdf_file.file_path.path)
            logger.info(f'Converted PDF to images. Total images: {len(images)}')
            
            # Calculate the total width and height for the combined image
            total_width = max(image.width for image in images)
            total_height = sum(image.height for image in images)

            # Create a new blank image with the total size
            combined_image = Image.new('RGB', (total_width, total_height))

            # Paste each image below the previous one
            y_offset = 0
            for image in images:
                combined_image.paste(image, (0, y_offset))
                y_offset += image.height

            # Save the combined image
            combined_image_file_path = pdf_file.file_path.path.replace('.pdf', '_combined.jpg')
            combined_image.save(combined_image_file_path, 'JPEG')

            return Response({'message': 'PDF converted to a single image successfully.', 'file': combined_image_file_path}, status=status.HTTP_200_OK)

        except PDFMetadata.DoesNotExist:
            logger.error(f'PDF metadata not found with ID: {pdf_id}')
            return Response({'error': 'PDF metadata not found.'}, status=status.HTTP_404_NOT_FOUND)

        except Exception as e:
            logger.error(f'Error converting PDF to a single image: {str(e)}')
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)