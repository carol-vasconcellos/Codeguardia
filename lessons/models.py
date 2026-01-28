from django.db import models

# Opções para o campo 'tipo'
TIPO_LICAO_CHOICES = [
    ('video', 'Vídeo de Conteúdo'),
    ('codigo', 'Desafio de Código'),
]

class Licao(models.Model):
    # Campos base
    titulo = models.CharField(max_length=200)
    slug = models.SlugField(unique=True, help_text="URL amigável (ex: intro-ao-python)")
    ordem = models.IntegerField(unique=True, help_text="Ordem em que a lição aparecerá")
    tipo = models.CharField(max_length=10, choices=TIPO_LICAO_CHOICES)

    # Conteúdo específico
    url_video = models.URLField(
        blank=True, null=True, 
        help_text="URL do Embed do YouTube (apenas se for 'Vídeo de Conteúdo')"
    )
    conselho = models.TextField(help_text="Descrição do desafio/instrução")
    esperado = models.TextField(
        blank=True, null=True, 
        help_text="Saída exata esperada no console (apenas se for 'Desafio de Código')"
    )
    codigo_padrao = models.TextField(
        blank=True, null=True, 
        help_text="Código inicial no editor (apenas se for 'Desafio de Código')"
    )

    class Meta:
        ordering = ['ordem']
        verbose_name_plural = "Lições"

    def __str__(self):
        return f"{self.ordem}. {self.titulo} ({self.get_tipo_display()})"