from loguru import logger

from rest_framework import status
from rest_framework.views import APIView
from rest_framework.generics import CreateAPIView, ListAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend

from .services import DB, get_structure, as_json, total_json
from .filter import create_filter
from ..log_in.permissions import IsTeacher, IsEmployee


db = DB()

class CreateDocClass(APIView):
    # permission_classes = [IsTeacher]

    def post(self, request, format=None):
        name = request.data.get('name')
        fields = request.data.get('fields')
        response = db.new_class(name, fields)
        return Response(response, status=status.HTTP_201_CREATED)


class DeleteDocClass(APIView):
    # permission_classes = [IsTeacher]

    def post(self, request, format=None):
        name = request.data.get('name')
        response = db.delete_model(name)
        return Response(response, status=status.HTTP_205_RESET_CONTENT)


class GetAllClassStructure(APIView):
    # permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        response = list(get_structure())
        return Response(response, status=status.HTTP_200_OK)


class GetAllClassStructureByFile(APIView):
    # permission_classes = [IsEmployee]
    
    def get(self, request, *args, **kwargs):
        expansion = kwargs.get('format')
        if expansion == 'json':
            response = total_json()
        return response


class GetClassStructure(APIView):
    # permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        response = list(get_structure(kwargs['name']))[0]
        return Response(response, status=status.HTTP_200_OK)


class GetClassStructureByFile(APIView):
    # permission_classes = [IsEmployee]

    def get(self, request, *args, **kwargs):
        name = kwargs.get('name')
        expansion = kwargs.get('format')
        if expansion == 'json':
            response = as_json(name)
        return response


class GetAllFields(APIView):
    # permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        response = []
        for i in get_structure():
            for j in i.get('fields'):
                response.append(j)
        return Response(response, status=status.HTTP_200_OK)


class GetAllClasses(APIView):
    # permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        response = []
        for i in get_structure():
            response.append(i.get('model'))
        return Response(response, status=status.HTTP_200_OK)


class CreateModelObject(CreateAPIView):
    # permission_classes = [IsTeacher]

    model = None
    queryset = None
    serializer_class = None

    def get_queryset(self):
        queryset = db.classes.get(self.model).get('model').objects.all()
        return queryset

    def get_serializer_class(self):
        serializer_class = db.classes.get(self.model).get('serializer')
        return serializer_class

    def post(self, request, *args, **kwargs):
        try:
            self.model = kwargs.get('model')
            return self.create(request, *args, **kwargs)
        except AttributeError:
            return Response(status = status.HTTP_404_NOT_FOUND)

    def get(self, request, *args, **kwargs):
        try:
            self.model = kwargs.get('model')
            return self.create(request, *args, **kwargs)
        except AttributeError:
            return Response(status = status.HTTP_404_NOT_FOUND)


class GetModelObjects(ListAPIView):
    # permission_classes = [IsEmployee]
    model = None
    queryset = None
    serializer_class = None

    filter_backends = (DjangoFilterBackend,)
    filterset_class = None

    @logger.catch
    def get_queryset(self):
        model = db.classes.get(self.model).get('model')
        queryset = model.objects.all()
        self.filterset_class = create_filter(model)
        return queryset

    def get_serializer_class(self):
        serializer_class = db.classes.get(self.model).get('serializer')
        return serializer_class

    def get(self, request, *args, **kwargs):
        try:
            self.model = kwargs.get('model')
            return self.list(request, *args, **kwargs)
        except AttributeError:
            return Response(status = status.HTTP_404_NOT_FOUND)


class AddModelFields(APIView):
    # permission_classes = [IsEmployee]

    def post(self, request, format=None):
        name = request.data.get('name')
        fields = request.data.get('fields')
        try:
            response = db.add_field(name, fields)
            return Response(response, status=status.HTTP_201_CREATED)
        except Exception:
            return Response(status=status.HTTP_409_CONFLICT)
        