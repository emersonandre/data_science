from django.shortcuts import render
from django.http import JsonResponse
from .kaggle_loader import carregar_transacoes

# Create your views here.
from django.http import JsonResponse
from .kaggle_loader import carregar_transacoes, baixar_e_carregar_dataset

def eda_basico(request):
    df = carregar_transacoes()
    info = {
        "linhas_colunas": df.shape,
        "colunas": df.columns.tolist(),
        "tipos": df.dtypes.astype(str).to_dict(),
        "nulos": df.isnull().sum().to_dict(),
        "exemplo": df.head(5).to_dict(orient="records")
    }
    return JsonResponse(info)

def dataset_resumo(request):
    data = baixar_e_carregar_dataset()
    resumo = {
        'transactions_shape': list(data['transactions'].shape),
        'transactions_columns': list(data['transactions'].columns),
        'transactions_head': data['transactions'].to_dict(orient='records'),
    }
    return JsonResponse(resumo)


