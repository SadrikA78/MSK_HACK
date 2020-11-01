from django_filters import rest_framework as filters

from .models import BinaryFile

from loguru import logger


class BinaryFileFilter(filters.FilterSet):
    added = filters.DateFromToRangeFilter()

    class Meta:
        model = BinaryFile
        fields = ['added']