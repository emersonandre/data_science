# analytics/kaggle_loader.py

import kagglehub
import os
from django.conf import settings
import zipfile
import pandas as pd
from kaggle.api.kaggle_api_extended import KaggleApi

def baixar_e_carregar_dataset():
    dataset = 'milootis/10-years-of-synthesized-erp-sales-data'
    download_path = os.path.join(settings.BASE_DIR, 'datasets')
    zip_file = os.path.join(download_path, '10-years-of-synthesized-erp-sales-data.zip')

    if not os.path.exists(download_path):
        os.makedirs(download_path, exist_ok=True)

    # Baixar o zip se ainda não existir
    if not os.path.exists(zip_file):
        api = KaggleApi()
        api.authenticate()
        api.dataset_download_files(dataset, path=download_path, unzip=False, quiet=False)

    # Extrair CSVs se não existirem
    #expected_files = ['customers.csv', 'transactions.csv', 'products.csv', 'stores.csv', 'sales_reps.csv']
    expected_files = ['transactions.csv']
    if not all(os.path.exists(os.path.join(download_path, f)) for f in expected_files):
        with zipfile.ZipFile(zip_file, 'r') as zip_ref:
            zip_ref.extractall(download_path)

    # Carregar os CSVs com caminho absoluto
    transactions = pd.read_csv(os.path.join(download_path, 'transactions.csv'))
    #customers = pd.read_csv(os.path.join(download_path, 'customers.csv'))
    #products = pd.read_csv(os.path.join(download_path, 'products.csv'))
    #stores = pd.read_csv(os.path.join(download_path, 'stores.csv'))
    #sales_reps = pd.read_csv(os.path.join(download_path, 'sales_reps.csv'))

    return {
        'transactions': transactions,
        #'customers': customers,
        #'products': products,
        #'stores': stores,
        #'sales_reps': sales_reps,
    }


def baixar_dataset_erp():
    path = kagglehub.dataset_download("milootis/10-years-of-synthesized-erp-sales-data", download_all=True)
    return path

def carregar_transacoes():
    pasta = baixar_dataset_erp()
    caminho_csv = os.path.join(pasta, "transactions.csv")
    df = pd.read_csv(caminho_csv)
    return df
