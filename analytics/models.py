from django.db import models

class Transaction(models.Model):
    inv_date = models.DateTimeField()
    invoice_number = models.CharField(max_length=100)
    account = models.CharField(max_length=100)
    part_number = models.CharField(max_length=100)
    qty = models.IntegerField()
    sell_price = models.FloatField()
    total_sale_value = models.FloatField()
    disc = models.FloatField()
    cost_price = models.FloatField()
    total_cost_value = models.FloatField()
    profit = models.FloatField()

    def __str__(self):
        return f"{self.invoice_number} - {self.part_number}"

class Modulo(models.Model):
    nome = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.nome

class Tabela(models.Model):
    nome = models.CharField(max_length=100, unique=True)
    modulo = models.ForeignKey(Modulo, on_delete=models.CASCADE, related_name='tabelas')
    criticidade = models.FloatField(default=0.0)  # pode ser calculada depois

    def __str__(self):
        return f"{self.nome} ({self.modulo.nome})"

class Dependencia(models.Model):
    tabela_origem = models.ForeignKey(Tabela, on_delete=models.CASCADE, related_name='dependencias_origem')
    tabela_dependente = models.ForeignKey(Tabela, on_delete=models.CASCADE, related_name='dependencias_dependente')
    tipo_relacao = models.CharField(max_length=50, default='foreign_key')  # ou "leitura", "escrita", etc.

    def __str__(self):
        return f"{self.tabela_origem.nome} → {self.tabela_dependente.nome}"