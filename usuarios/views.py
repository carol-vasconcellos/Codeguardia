# usuarios/views.py

from django.shortcuts import render, redirect 
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm 
from django.contrib.auth import login
from .forms import CustomUserCreationForm 

# 🌟 CORREÇÃO: Importa a função de cálculo do app 'lessons' a partir do utils
from lessons.utils import get_progress_data 

# ----------------------------------------------------------------

@login_required
def bem_vindo(request):
    """View do Painel do Aluno, mostra o progresso, lendo do DB."""
    
    # CHAMA A FUNÇÃO QUE LÊ DO BANCO DE DADOS A PARTIR DO UTILS
    progress_data = get_progress_data(request.user) # Passa o objeto User
    
    context = {
        'nome_usuario': request.user.username,
        **progress_data, 
    }
    return render(request, 'usuarios/bem_vindo.html', context)


def criar_conta(request): 
    """View de Criação de Novo Usuário (Sign Up).""" 
    if request.method == 'POST': 
        # 🌟 USANDO O FORMULÁRIO CUSTOMIZADO 🌟
        form = CustomUserCreationForm(request.POST) 
        if form.is_valid(): 
            user = form.save() 
            # Loga o usuário automaticamente após o registro 
            login(request, user)  
            return redirect('bem_vindo')  
    else: 
        # 🌟 USANDO O FORMULÁRIO CUSTOMIZADO 🌟
        form = CustomUserCreationForm() 
      
    return render(request, 'usuarios/criar_conta.html', {'form': form})

def landing_page(request):
    """View da Página Principal (Landing Page)."""
    
    if request.user.is_authenticated:
        return redirect('bem_vindo') 
        
    mensagem = "CodeGuardia"
    botao_url = 'login' 
    botao_texto = "Comece Agora"

    context = {
        'mensagem': mensagem,
        'botao_url': botao_url,
        'botao_texto': botao_texto,
    }
    return render(request, 'usuarios/landing.html', context)
