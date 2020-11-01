from loguru import logger

from rest_framework import serializers

from .models import BinaryFile, ImgFile
from ..learning.views import db


class DocField(serializers.Field):
    def get_attribute(self, instance):
        for i in db.classes.values():
            obj = i.get('model').objects.filter(file_id=instance.id)
            if obj:
                return i.get('serializer')(obj, many=True).data
        return None

    def to_representation(self, value):
        return value


class BinaryFileSerializer(serializers.ModelSerializer):
    author = serializers.HiddenField(default=serializers.CurrentUserDefault())
    pictures = serializers.SerializerMethodField(method_name='get_pictures')
    doc_fields = DocField()

    def get_pictures(self, obj):
        query_set = ImgFile.objects.filter(parent_file=obj.id)
        serializer = ImgFileFileSerializer(query_set, many=True)
        return serializer.data

    def create(self, **kwargs):
        return BinaryFile.objects.create(**kwargs)

    class Meta:
        model = BinaryFile
        fields = '__all__'


class ImgFileFileSerializer(serializers.ModelSerializer):
    class Meta:
        model = ImgFile
        fields = ['file']


def files_by_description(model):
    model_set = db.classes.get(model)
    queryset = model_set.get('model').objects.all()
    data = []
    for i in queryset:
        queryset = BinaryFile.objects.filter(file=i.file )
        data.append(BinaryFileSerializer(queryset, many=True).data)
    return data