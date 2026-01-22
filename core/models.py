from django.db import models

# Create your models here.
# Create your models here. 
class Categoria(models.Model):
    TIPO_CHOICES = [
        ('receita', 'Receita'),
        ('despesa', 'Despesa'),
    ]

    nome = models.CharField(max_length=100)
    descricao = models.TextField(blank=True)
    tipo = models.CharField(max_length=20, choices=TIPO_CHOICES) #Especifico a variável que detem os tipos

    def __str__(self):
        return f"{self.nome} ({self.get_tipo_display()})" # get_tipo_display() pega o label 'Receita' ou 'Despesa'
    
    class Meta:
        verbose_name_plural = 'Categorias'


class Conta(models.Model):
    nome = models.CharField(max_length=20)
    saldo_inicial = models.DecimalField(decimal_places=2, max_digits=10, default=0) #DecimalField não tem arredondamento, melhor para valores monetários do que FloatField

    def __str__(self):
        return self.nome


class Transacao(models.Model):
    descricao = models.CharField(max_length=100)
    valor = models.DecimalField(decimal_places=2, max_digits=10, default=0)
    data = models.DateField()  # Só a data, sem hora
    categoria = models.ForeignKey(Categoria, on_delete=models.PROTECT)  # minúscula!
    conta = models.ForeignKey(Conta, on_delete=models.PROTECT)  # minúscula!
    observacao = models.TextField(blank=True)  # opcional
    criado_em = models.DateTimeField(auto_now_add=True)  # registra quando foi criado

    def __str__(self):
        return f"{self.descricao} - R$ {self.valor}"
    
    class Meta:
        verbose_name_plural = 'Transações'
        ordering = ['-data', '-criado_em']