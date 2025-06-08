from django.urls import path
from .views import eda_basico, dataset_resumo

urlpatterns = [
    path('analytics/eda/', eda_basico),
    path('analytics/resumo/', dataset_resumo, name='dataset_resumo'),
]
