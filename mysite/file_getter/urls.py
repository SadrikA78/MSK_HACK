from django.urls import path

from . import views


urlpatterns = [
    path('', views.UploadFile.as_view()),
    path('my/', views.GetFilesHistory.as_view()),
    path('get/', views.GetAllFiles.as_view()),
    path('get/<int:pk>/', views.GetFile.as_view()),
    path('get/download/<int:pk>/', views.DownloadFile.as_view()),
    path('get/download/pdf/<int:pk>/', views.DownloadFile.as_view(content = 'application/octet-stream')),
    path('img/create/', views.CreateImage.as_view()),
    path('get/structure/<int:pk>/<str:form>/', views.DownloadFileInfo.as_view()),
    path('get/structure/<str:model>/', views.DownloadAllStructure.as_view()),
    path('get/structure/<str:model>/<str:form>/', views.DownloadAllFilesStructure.as_view()),
]
