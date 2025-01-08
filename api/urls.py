from django.urls import path
from .views import (
    UploadFileView, ListImagesView, ListPDFsView, ImageDetailView, PDFDetailView,
    DeleteImageView, DeletePDFView, RotateImageView, ConvertPDFToImageView
)

urlpatterns = [
    path('upload/', UploadFileView.as_view()),
    path('images/', ListImagesView.as_view()),
    path('pdfs/', ListPDFsView.as_view()),
    path('images/<int:pk>/', ImageDetailView.as_view()),
    path('pdfs/<int:pk>/', PDFDetailView.as_view()),
    path('images/<int:pk>/delete/', DeleteImageView.as_view()),
    path('pdfs/<int:pk>/delete/', DeletePDFView.as_view()),
    path('rotate/', RotateImageView.as_view()),
    path('convert-pdf-to-image/', ConvertPDFToImageView.as_view()),
]