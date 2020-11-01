from django_filters import rest_framework as filters

from loguru import logger


def create_filter(model) -> filters.FilterSet:
    fields = [i.strip().rstrip(')') for i in model.__doc__.split(',')[1:]]
    fields.remove('file')
    fields = {i: ['exact', 'contains'] for i in fields}

    meta = type(
            'Meta',
            tuple(), {
                "model": model,
                "fields": fields
            })
    fields = {i: filters.CharFilter() for i in fields.keys()}
    fields['Meta'] = meta
    my_filter = type(
                f'filter',
                (filters.FilterSet,),
                fields
            )
    return my_filter