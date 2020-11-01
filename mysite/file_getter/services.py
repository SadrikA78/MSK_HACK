import re
import os
import json

from loguru import logger
import transliterate
import pandas as pd

from django.http import HttpResponse
from wsgiref.util import FileWrapper


DIRPATH = os.getcwd()+'/apps/file_getter/files_structure'

def save_list(serializer, request):
    ''' 
    Получает запрос, сохраняет в сериализатор файлы,
    возвращает list(dict) сохраненных моделей
    '''
    response = []
    for file_number in range(len(request.data)-1):
        file = request.data.get(f'file{file_number}')
        saved = serializer.create(author=request.user, file=file)
        response.append({
            'id': saved.id,
            'path': saved.file.path,
            'format': saved.file.path.split('.')[-1]
        })

    return response

def get_file(file, content: str = None):
    ''' 
    Получает объкт queryset модели BinaryFiles и указание "отдавать/делать превью",
    возвращаем HttpResponse с файлом на скачивание/превью 
    '''
    file_format = file.file.path.split('.')[-1]
    with open(file.file.path, 'rb') as short_report:
        if not content:
            content = f'application/{file_format}'
        response = HttpResponse(
                FileWrapper(short_report),
                content_type=content
            )
        if content != 'application/pdf':
            filename = _transile_filename(file.file.name)
            response['Content-Disposition'] = f'attachment; filename="{filename}"'
        return response


def _transile_filename(filename: str):
    ''' Проверяем файл на латиницу, иначе транслитерируем '''
    filename = filename.split('/')[-1]
    if re.search(r'[а-яА-ЯёЁ]', filename):
        filename = transliterate.translit(filename, reversed=True)
    return filename

def json_to_file(filename, data):
    filename = DIRPATH+f'/{filename}.json'
    with open(filename, 'w') as f:
        json.dump(data, f, ensure_ascii=False)
    return _send(filename, 'json')

def transform_list(data):
    for i in data:
        yield transform(i[0])

def list_to_pd(pk, data, format):
    df = pd.DataFrame(columns = data[0].keys())
    for i in range(len(data)):
        df.loc[i+1] = data[i]
    return _send_df(pk, format, df)

def transform(data):
    if data['pictures']:
        data['pictures'] = list(data['pictures'][0].values())
    if data['doc_fields']:
        for i in data['doc_fields'][0]:
            data[i] = data['doc_fields'][0].get(i)
    data.pop('doc_fields')
    return data

def to_pd(pk, data, format):
    df = pd.DataFrame(columns = data.keys())
    df.loc[1] = data.values()
    return _send_df(pk, format, df)

def _send_df(pk, format, df):
    filename = DIRPATH+f'/{pk}.{format}'
    if format == 'xlsx':
        df.to_excel(filename)
    if format == 'csv':
        df.to_csv(DIRPATH+f'/{pk}.csv')
    return _send(filename, format)

def _send(filename, format):
    with open(filename, 'rb') as short_report:
        content = f'application/{format}'
        response = HttpResponse(
                FileWrapper(short_report),
                content_type=content
            )
        response['Content-Disposition'] = f'attachment; filename="{filename}"'
        return response