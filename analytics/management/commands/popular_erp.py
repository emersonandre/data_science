import pandas as pd
import os
from django.core.management.base import BaseCommand
from analytics.models import Modulo, Tabela, Dependencia

class Command(BaseCommand):
    help = 'Popula os modelos Modulo, Tabela e Dependencia com base em transactions.csv'

    def handle(self, *args, **options):
        csv_path = './datasets/transactions.csv'
        if not os.path.exists(csv_path):
            self.stdout.write(self.style.ERROR(f'Arquivo {csv_path} não encontrado'))
            return

        df = pd.read_csv(csv_path)
        df.columns = df.columns.str.strip().str.lower().str.replace(' ', '_')

        # Criar módulo Vendas
        vendas_modulo, _ = Modulo.objects.get_or_create(nome='Vendas')

        # Criar tabela transactions
        transactions_tabela, _ = Tabela.objects.get_or_create(nome='transactions', modulo=vendas_modulo)

        # Criar tabelas fictícias referenciadas
        tabelas_referenciadas = ['products', 'customers', 'stores', 'sales_reps']
        for nome in tabelas_referenciadas:
            tabela_ref, _ = Tabela.objects.get_or_create(nome=nome, modulo=vendas_modulo)
            Dependencia.objects.get_or_create(
                tabela_origem=transactions_tabela,
                tabela_dependente=tabela_ref,
                tipo_relacao='foreign_key'
            )

        self.stdout.write(self.style.SUCCESS('Módulo, Tabelas e Dependências criadas com sucesso.'))
