from django.urls import path

from . import views


urlpatterns = [
    path('object/create/<str:model>/', views.CreateModelObject.as_view()),
    path('object/get/<str:model>/', views.GetModelObjects.as_view()),

    path('class/create/', views.CreateDocClass.as_view()),
    path('class/delete/', views.DeleteDocClass.as_view()),
    path('class/structure/', views.GetAllClassStructure.as_view()),
    path('class/all/', views.GetAllClasses.as_view()),

    path('file/structure/<str:format>/', views.GetAllClassStructureByFile.as_view()), # json | csv | xlsx
    path('file/structure/<str:format>/<str:name>/', views.GetClassStructure.as_view()), # json | csv | xlsx

    path('field/all/', views.GetAllFields.as_view()),
    path('field/add/', views.AddModelFields.as_view()),
]