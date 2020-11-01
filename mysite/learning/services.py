import os
import json
import base64

from loguru import logger
import psycopg2
from psycopg2 import sql

from django.db import models
from django.http import HttpResponse
from wsgiref.util import FileWrapper

from rest_framework import serializers

from ..file_getter.models import BinaryFile

os.path.join(os.getcwd())
from config.settings import DATABASES


DIRPATH = os.getcwd()+'/apps/learning/pickles'


class DB:
    classes: dict = {}

    def __init__(self):
        files = filter(lambda x: x.endswith('.json'), os.listdir(DIRPATH))
        for file in files:
            if file != 'total.json':
                with open(DIRPATH+f'/{file}', 'r') as f:
                    model_params = json.load(f)
                    name = model_params.get('model_name')
                    fields = model_params.get('fields')
                    model = self._create_model(name, fields)
                    serializer = self._create_serializer(name, model)
                    self.classes[name] = {
                        'model': model,
                        'serializer': serializer
                    }
    
    def new_class(self, model_name: str, model_fields: list) -> dict:
        model = self._create_model(model_name, model_fields)
        serializer = self._create_serializer(model_name, model_fields)
        self._save_model(model_name, model_fields)
        self.classes[model_name] = {
            'model': model,
            'serializer': serializer
        }
        return {'name': model_name, 'fields': model_fields}

    def delete_model(self, model_name: str) -> None:
        try:
            os.remove(DIRPATH+f'/{model_name}.json')
            command = f'DROP TABLE IF EXISTS learning_{model_name}'
            self._sql_execute(command)
            return 'Success'
        except FileNotFoundError:
            return 'Model not exist'

    def add_field(self, model_name:str, fields: list) -> None:
        command = ''.join([f'ADD COLUMN {i} TEXT, ' for i in fields]).rstrip(', ')
        command = f'ALTER TABLE learning_{model_name} {command};'
        with open(DIRPATH + f'/{model_name}.json', 'r') as json_file:
                data = json.load(json_file)
        self._sql_execute(command)
        data['fields'] = data.get('fields') + fields
        with open(DIRPATH + f'/{model_name}.json', 'w') as f:
            json.dump(data, f)
        return data


    def _create_model(self, model_name: str, model_fields: list) -> models.Model:
        fields = {field: models.TextField(field) for field in model_fields}
        fields['file'] = models.ForeignKey(BinaryFile, on_delete=models.CASCADE)
        fields['__module__'] = 'apps.learning'
        return type(model_name, (models.Model,), fields)

    def _create_serializer(self, model_name:str, model: models.Model) -> serializers.ModelSerializer:
        meta = type(
            'Meta',
            tuple(), {
                "model": model,
                "exclude": ('id',)
            })
        serializer = type(
                f'{model_name}_serializer',
                (serializers.ModelSerializer,),
                {"Meta": meta}
            )
        return serializer

    def _save_model(self, model_name: str, model_fields: list) -> None:
        with open(DIRPATH + f'/{model_name}.json', 'w') as f:
            json.dump({
                'model_name': model_name,
                'fields': model_fields
            }, f)

        command = ''.join([f'{i} TEXT, ' for i in model_fields])
        command = f'CREATE TABLE IF NOT EXISTS\
            learning_{model_name} (id int GENERATED BY DEFAULT AS IDENTITY PRIMARY KEY,\
            {command}UNIQUE(file_id), file_id INTEGER REFERENCES file_getter_binaryfile(id))'
        self._sql_execute(command)

    def _sql_execute(self, command: str) -> None:
        con = psycopg2.connect(
                database=DATABASES.get('default').get('NAME'), 
                user=DATABASES.get('default').get('USER'), 
                password=DATABASES.get('default').get('PASSWORD'), 
                host=DATABASES.get('default').get('HOST'), 
                port=DATABASES.get('default').get('PORT')
            )
        cur = con.cursor()
        cur.execute(sql.SQL(command))
        con.commit()  
        con.close()


def get_structure(class_name: str = False):
    if not class_name:
        files = filter(lambda x: x.endswith('.json'), os.listdir(DIRPATH))
        for file in files:
            if file != 'total.json':
                with open(DIRPATH+f'/{file}', 'r') as f:
                    model_params = json.load(f)
                    name = model_params.get('model_name')
                    fields = model_params.get('fields')
                    yield {
                        'model': name,
                        'fields': fields
                    }
    else:
        with open(DIRPATH+f'/{class_name}.json', 'r') as f:
            model_params = json.load(f)
            name = model_params.get('model_name')
            fields = model_params.get('fields')
            yield {
                'model': name,
                'fields': fields
            }

def total_json():
    with open('total.json', 'w') as f:
        json.dump(list(get_structure()), f, ensure_ascii=False)
    return as_json('total')

def as_json(name):
    with open(DIRPATH+f'/{name}.json', 'rb') as data:
        response = HttpResponse(
                FileWrapper(data),
                content_type='application/json'
            )
        response['Content-Disposition'] = 'attachment; filename="structure.json"'
        return response