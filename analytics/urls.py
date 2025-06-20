from django.urls import path
from .views import eda_basico, dataset_resumo, grafo_dependencias

urlpatterns = [
    path('analytics/eda/', eda_basico),
    path('analytics/resumo/', dataset_resumo, name='dataset_resumo'),
    path('analytics/grafo/', grafo_dependencias, name='grafo_dependencias'),
]
