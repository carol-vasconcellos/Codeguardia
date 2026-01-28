import sys
import io
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from .models import Licao

def detalhe_licao(request, slug):
    # Busca a lição pelo slug (ex: seu-primeiro-codigo)
    licao = get_object_or_404(Licao, slug=slug)
    
    # Variáveis para o template
    output = ""
    sucesso = False
    codigo_enviado = licao.codigo_padrao or ""

    if request.method == "POST":
        codigo_enviado = request.POST.get("codigo", "")
        
        # --- LÓGICA DE EXECUÇÃO DO PYTHON ---
        # 1. Criamos um "buffer" para capturar os prints do aluno
        buffer_saida = io.StringIO()
        sys.stdout = buffer_saida  # Redireciona o print para o buffer

        try:
            # 2. Executa o código enviado pelo aluno
            # O dicionário vazio {} serve para isolar o ambiente de execução
            exec(codigo_enviado, {})
            
            # 3. Pega o texto que saiu nos prints e remove espaços extras
            output = buffer_saida.getvalue().strip()
        except Exception as e:
            # Se o código do aluno tiver erro de digitação, mostra o erro no console
            output = f"Erro no código: {str(e)}"
        finally:
            # 4. IMPORTANTE: Volta o console do servidor ao normal
            sys.stdout = sys.__stdout__

        # --- VALIDAÇÃO ---
        # Compara o que o aluno imprimiu com o que você cadastrou no Admin
        if licao.tipo == 'codigo':
            if output == licao.esperado.strip():
                sucesso = True
                messages.success(request, "Parabéns! Você acertou o desafio.")
            else:
                messages.error(request, "O código rodou, mas o resultado não é o esperado.")

    return render(request, "lessons/detalhe_licao.html", {
        "licao": licao,
        "codigo": codigo_enviado,
        "output": output,
        "sucesso": sucesso
    })