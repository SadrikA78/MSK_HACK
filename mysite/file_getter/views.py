from rest_framework.generics import (
    ListCreateAPIView,
    ListAPIView,
    RetrieveAPIView,
    CreateAPIView
)
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.parsers import MultiPartParser
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend

from .models import BinaryFile, ImgFile
from .serializers import BinaryFileSerializer, ImgFileFileSerializer, files_by_description
from .filters import BinaryFileFilter
from .services import save_list, get_file, transform, to_pd, transform_list, list_to_pd, json_to_file
from ..log_in.permissions import IsEmployee

from loguru import logger


class UploadFile(ListCreateAPIView):
    parser_classes = (MultiPartParser, )
    # permission_classes = (IsAuthenticated, )
    queryset = BinaryFile.objects.all()
    serializer_class = BinaryFileSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        response = save_list(serializer, self.request)
        return Response(response, status=status.HTTP_201_CREATED)


class GetFile(RetrieveAPIView):
    # permission_classes = (IsAuthenticated, )
    queryset = BinaryFile.objects.all()
    serializer_class = BinaryFileSerializer


class DownloadFile(RetrieveAPIView):
    # permission_classes = (IsAuthenticated, )
    content: str = None

    queryset = BinaryFile.objects.all()
    serializer_class = BinaryFileSerializer

    def get(self, request, *args, **kwargs):
        file = BinaryFile.objects.get(id=kwargs['pk'])
        response = get_file(file, self.content)
        return response


class GetAllFiles(ListAPIView):
    # permission_classes = (IsEmployee, )
    queryset = BinaryFile.objects.all().order_by('-added')
    serializer_class = BinaryFileSerializer
    filter_backends = (DjangoFilterBackend,)
    filterset_class = BinaryFileFilter


class GetFilesHistory(ListAPIView):
    # permission_classes = (IsAuthenticated,)
    queryset = BinaryFile.objects.all()
    serializer_class = BinaryFileSerializer
    filter_backends = (DjangoFilterBackend,)
    filterset_class = BinaryFileFilter

    def get_queryset(self):
        return self.queryset.filter(author=self.request.user).order_by('-added')


class CreateImage(CreateAPIView):
    # permission_classes = (IsAuthenticated,)
    queryset = ImgFile.objects.all()
    serializer_class = ImgFileFileSerializer


class DownloadFileInfo(RetrieveAPIView):
    # permission_classes = (IsEmployee, )
    queryset = BinaryFile.objects.all()
    serializer_class = BinaryFileSerializer

    def get(self, request, *args, **kwargs):
        logger.debug('here')
        file = BinaryFile.objects.get(id=kwargs['pk'])
        data = BinaryFileSerializer(file).data
        file_type = kwargs['form']
        data = transform(data)
        if file_type == 'json':
            response = json_to_file(kwargs['pk'], data)
        else:
            response = to_pd(kwargs['pk'], data, file_type)
        return response


class DownloadAllFilesStructure(APIView):
    # permission_classes = (IsEmployee, )
    
    def get(self, request, *args, **kwargs):
        data = files_by_description(kwargs.get('model'))
        file_type = kwargs['form']
        data = list(transform_list(data))
        if file_type == 'json':
            response = json_to_file(kwargs['model'], data)
        else:
            response = list_to_pd(kwargs['model'], data, 'xlsx')
        return response


class DownloadAllStructure(APIView):
    # permission_classes = (IsEmployee, )

    def get(self, request, *args, **kwargs):
        data = files_by_description(kwargs.get('model'))
        return Response(data, status=status.HTTP_200_OK)