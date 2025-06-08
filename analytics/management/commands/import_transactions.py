import os
import pandas as pd
from django.core.management.base import BaseCommand
from analytics.models import Transaction  # Altere para o nome correto do seu app
from django.utils.dateparse import parse_datetime

class Command(BaseCommand):
    help = 'Importa dados do transactions.csv para o banco de dados'

    def handle(self, *args, **kwargs):
        csv_path = os.path.join('datasets', 'transactions.csv')

        # Carrega e normaliza os nomes das colunas
        df = pd.read_csv(csv_path)
        df.columns = df.columns.str.strip().str.lower().str.replace(' ', '_')

        # Converte data
        df['inv_date'] = pd.to_datetime(df['inv_date'])

        # Importa linha por linha
        for _, row in df.iterrows():
            Transaction.objects.create(
                inv_date=row['inv_date'],
                invoice_number=row['invoice_number'],
                account=row['account'],
                part_number=row['part_number'],
                qty=row['qty'],
                sell_price=row['sell_price'],
                total_sale_value=row['total_sale_value'],
                disc=row['disc'],
                cost_price=row['cost_price'],
                total_cost_value=row['total_cost_value'],
                profit=row['profit'],
            )

        self.stdout.write(self.style.SUCCESS("Transações importadas com sucesso!"))
