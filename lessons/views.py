import sys
import io
import traceback
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Licao 
# Importando do utils conforme sua estrutura
from .utils import get_progress_data, set_lesson_completed, is_lesson_completed, set_lesson_pending

# --- AUXILIARES ---

def get_next_slug(current_slug):
    """Busca o slug da próxima lição no banco de dados pela ordem."""
    try:
        current_lesson = Licao.objects.get(slug=current_slug)
        next_lesson = Licao.objects.filter(ordem__gt=current_lesson.ordem).order_by('ordem').first()
        if next_lesson:
            return next_lesson.slug
    except Licao.DoesNotExist:
        pass
    return None

# --- VIEWS ---

@login_required
def lista_licoes(request):
    user = request.user
    licoes_db = Licao.objects.all().order_by('ordem')
    
    licoes_status = [
        (licao.slug, licao, is_lesson_completed(user, licao))
        for licao in licoes_db
    ]
    return render(request, 'lessons/lista_licoes.html', {'licoes_status': licoes_status})

@login_required
def licao_detalhe(request, slug):
    user = request.user 
    licao = get_object_or_404(Licao, slug=slug)
    
    output = ""
    sucesso = is_lesson_completed(user, licao)
    dica_erro = None
    feedback_tipo = None
    # Sincronizado com o seu HTML (codigo_usuario)
    codigo_usuario = request.POST.get('codigo_editor', licao.codigo_padrao or "")

    if request.method == 'POST':
        # A. Lição de vídeo
        if licao.tipo == 'video' and 'marcar_concluida' in request.POST:
            set_lesson_completed(user, licao)
            return redirect('lessons:licao_detalhe', slug=slug) 
        
        # B. Lição de código
        elif licao.tipo == 'codigo':
            # Captura de saída para o console
            buffer_saida = io.StringIO()
            sys.stdout = buffer_saida

            try:
                # Executa o código em ambiente isolado
                exec(codigo_usuario, {"__builtins__": __builtins__}, {})
                output = buffer_saida.getvalue().strip()
                
                # Validação
                esperado = licao.esperado.strip() if licao.esperado else ""
                if output == esperado:
                    set_lesson_completed(user, licao)
                    sucesso = True
                    feedback_tipo = 'SUCESSO'
                else:
                    feedback_tipo = 'ERRO_SAIDA'
                    dica_erro = f"O console retornou '{output}', mas esperávamos '{esperado}'."
            
            except Exception as e:
                output = traceback.format_exc().splitlines()[-1]
                feedback_tipo = 'ERRO_CODIGO'
                dica_erro = "Erro de sintaxe no seu código Python."
            
            finally:
                sys.stdout = sys.__stdout__

    context = {
        'licao': licao, 
        'codigo_usuario': codigo_usuario,
        'output': output,
        'sucesso': sucesso,
        'proximo_slug': get_next_slug(slug),
        'dica_erro': dica_erro, 
        'feedback_tipo': feedback_tipo,
        'slug': slug,
        'forum_link': "https://forum.codeguardia.com", 
    }
    return render(request, 'lessons/licao_detalhe.html', context)

@login_required
def refazer_licao(request, slug):
    user = request.user
    licao = get_object_or_404(Licao, slug=slug)
    set_lesson_pending(user, licao)
    return redirect('lessons:licao_detalhe', slug=slug)