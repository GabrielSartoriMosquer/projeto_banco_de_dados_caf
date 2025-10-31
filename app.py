import streamlit as st
import streamlit.components.v1 as components
import datetime
import pandas as pd
from pessoa import Pessoa
from db import (
    inicializar_banco, p_atualizada = Pessoa(
                            nome, filiacao1, filiacao2, data_nasc_str, doc_identidade,
                            nacionalidade, telefone, email,
                            endereco_residencial, endereco_trabalho, # <--- CORRIGIDO
                            cpf, id_beneficiario=id_selecionado 
                        )
    inserir_beneficiario, 
    listar_beneficiarios,
    buscar_beneficiario_por_id,
    atualizar_beneficiario,
    deletar_beneficiario
)

# --- 1. INICIALIZAÇÃO E CONFIGURAÇÃO ---
st.set_page_config(layout="wide")

if 'pagina' not in st.session_state:
    st.session_state['pagina'] = 'inicial'

try:
    inicializar_banco()
except Exception as e:
    st.sidebar.error(f"Erro ao conectar com o banco: {e}")

if 'pagina' not in st.session_state:
    st.session_state['pagina'] = 'inicial'

# Função auxiliar para mudar de página
def mudar_pagina(pagina):
    st.session_state['pagina'] = pagina

# --- 2. NAVEGAÇÃO NA BARRA LATERAL (SIDEBAR) ---

st.sidebar.title('Menu de Navegação')
st.sidebar.button('Página Inicial', on_click=mudar_pagina, width='stretch', args=('inicial',))
st.sidebar.button('Adicionar Usuário', on_click=mudar_pagina, width='stretch', args=('adicionar',))
st.sidebar.button('Gerenciar Usuários (Editar/Excluir)', on_click=mudar_pagina, width='stretch', args=('gerenciar',))
st.sidebar.button('Listar Usuários', on_click=mudar_pagina, width='stretch', args=('listar',))
st.sidebar.button('Gerar Dashboard', on_click=mudar_pagina, width='stretch', args=('dashboard',))

# --- 3. DEFINIÇÃO DAS PÁGINAS ---

def pagina_inicial():
    st.title('Projeto CAF - Sistema de Cadastro de Beneficiários')
    st.write('Interface para cadastro, edição e exclusão de beneficiários no banco de dados.')
    st.write('Use o menu lateral para navegar entre as páginas.')
    st.divider()

    try:
        total_beneficiarios = len(listar_beneficiarios())
        st.metric('Total de Beneficiários Cadastrados', total_beneficiarios)
    except Exception as e:
        st.error(f'Não foi possível carregar as métricas: {e}')

def pagina_adicionar():
    st.title('➕ Adicionar Novo Beneficiário')
    st.write('Preencha os dados abaixo para cadastrar uma nova pessoa.')
    
    with st.form(key='cadastro_form'):
        st.subheader('Dados Pessoais')
        nome = st.text_input('Nome completo:')
        filiacao1 = st.text_input('Filiação 1:')
        filiacao2 = st.text_input('Filiação 2:')
        cpf = st.text_input('CPF (Quando disponível):')
        
        data_nasc_dt = st.date_input(
            'Data de nascimento:',
            value=datetime.date(2000, 1, 1),
            min_value=datetime.date(1900, 1, 1),
            max_value=datetime.date.today(),
            format='DD/MM/YYYY'
        )
        
        doc_identidade = st.text_input('Documento de identidade:')
        nacionalidade = st.text_input('Nacionalidade:', 'Brasileira')
        
        st.subheader('Contato e Endereço')
        telefone = st.text_input('Telefone (apenas números):')
        email = st.text_input('E-mail:')
        endereco_residencial = st.text_area('Endereço residencial:')
        endereco_trabalho = st.text_area('Endereço do trabalho:')

        submit_button = st.form_submit_button(label='Cadastrar Pessoa')

    if submit_button:
        if not nome or not filiacao1:
            st.error('Por favor, preencha pelo menos o Nome e a Filiação 1.')
        else:
            try:
                data_nasc_str = data_nasc_dt.strftime('%Y-%m-%d')
                p = Pessoa(nome, filiacao1, filiacao2, data_nasc_str, doc_identidade,
                            nacionalidade, telefone, email,
                            endereco_residencial, endereco_trabalho, cpf, 
                            id_beneficiario=None) # ID é None na criação

                id_gerado = inserir_beneficiario(p)
                st.success(f'Pessoa {p.nome} cadastrada com sucesso (ID {id_gerado})')
                st.balloons()
            except Exception as e:
                st.error(f'Erro ao cadastrar: {e}')

def pagina_listar():
    st.title('📋 Listar Beneficiários Cadastrados')
    st.write('Aqui estão os beneficiários já cadastrados no sistema.')

    try:
        beneficiarios = listar_beneficiarios()
        if not beneficiarios:
            st.info('Nenhuma pessoa cadastrada no banco de dados.')
        else:
            df = pd.DataFrame(
                beneficiarios,
                columns=['ID', 'Nome', 'CPF', 'Data Nascimento']
            )
            st.dataframe(df, width='stretch')
    except Exception as e:
        st.error(f'Erro ao listar beneficiários: {e}')

def pagina_gerenciar():
    st.title('✏️ Gerenciar Beneficiários (Editar/Excluir)')
    
    try:
        beneficiarios_lista = listar_beneficiarios()
        if not beneficiarios_lista:
            st.info('Nenhum beneficiário cadastrado para gerenciar.')
            return

        df = pd.DataFrame(beneficiarios_lista, columns=['id', 'nome', 'cpf', 'data_nasc'])
        opcoes = [f"{row['id']} - {row['nome']}" for _, row in df.iterrows()]
        
        # Seleção de usuário
        opcao_selecionada = st.selectbox('Selecione um beneficiário para editar ou excluir:', 
                                            options=['Selecione...'] + opcoes,
                                            key='select_gerenciar')
        
        if opcao_selecionada != 'Selecione...':
            id_selecionado = int(opcao_selecionada.split(' - ')[0])
            
            # --- SEÇÃO DE EDIÇÃO ---
            st.subheader(f'Editando Usuário (ID: {id_selecionado})')
            dados_usuario = buscar_beneficiario_por_id(id_selecionado)
            
            if not dados_usuario:
                st.error('Erro: Não foi possível encontrar os dados deste usuário.')
                return

            # Trata data que vem do banco
            try:
                data_nasc_val = datetime.datetime.strptime(dados_usuario.get('data_nascimento'), '%Y-%m-%d').date()
            except:
                data_nasc_val = datetime.date(2000, 1, 1)

            with st.form(key='edit_form'):
                nome = st.text_input('Nome completo:', value=dados_usuario.get('nome', ''))
                filiacao1 = st.text_input('Filiação 1:', value=dados_usuario.get('filiacao1', ''))
                filiacao2 = st.text_input('Filiação 2:', value=dados_usuario.get('filiacao2', ''))
                cpf = st.text_input('CPF:', value=dados_usuario.get('cpf', ''))
                
                data_nasc_dt = st.date_input(
                    'Data de nascimento:', value=data_nasc_val, format='DD/MM/YYYY'
                )
                
                doc_identidade = st.text_input('Doc. identidade:', value=dados_usuario.get('documento_identidade', ''))
                nacionalidade = st.text_input('Nacionalidade:', value=dados_usuario.get('nacionalidade', ''))
                telefone = st.text_input('Telefone:', value=dados_usuario.get('telefone', ''))
                email = st.text_input('E-mail:', value=dados_usuario.get('email', ''))
                st.subheader('Endereços')
                endereco_residencial = st.text_area('Endereço residencial:', 
                                                    value=dados_usuario.get('endereco_residencial', ''))
                endereco_trabalho = st.text_area('Endereço do trabalho:', 
                                                 value=dados_usuario.get('endereco_trabalho', ''))
                
                update_button = st.form_submit_button(label='Atualizar Dados')

                if update_button:
                    try:
                        data_nasc_str = data_nasc_dt.strftime('%Y-%m-%d')
                        p_atualizada = Pessoa(
                            nome, filiacao1, filiacao2, data_nasc_str, doc_identidade,
                            nacionalidade, telefone, email,
                            endereco_residencial, endereco_trabalho, # <--- CORRIGIDO
                            cpf, id_beneficiario=id_selecionado 
                        )
                        
                        atualizar_beneficiario(p_atualizada)
                        st.success(f'Beneficiário {nome} (ID {id_selecionado}) atualizado com sucesso!')
                        st.rerun()
                        
                    except Exception as e:
                        st.error(f'Erro ao atualizar: {e}')

            # --- SEÇÃO DE EXCLUSÃO ---
            st.divider()
            with st.expander('🚨 Zona de Perigo - Excluir Beneficiário'):
                st.write(f'Cuidado: esta ação é irreversível e excluirá {dados_usuario['nome']} (ID {id_selecionado}).')
                
                delete_button = st.button(f'Excluir Permanentemente (ID {id_selecionado})', type='primary')

                if delete_button:
                    try:
                        deletar_beneficiario(id_selecionado)
                        st.success(f'Beneficiário (ID {id_selecionado}) excluído com sucesso!')
                        st.rerun()
                    except Exception as e:
                        st.error(f'Erro ao excluir: {e}. Verifique se há atendimentos vinculados.')
                        
    except Exception as e:
        st.error(f'Erro ao carregar gerenciador: {e}')

def gerar_dashboard():
    iframe_code = """
<iframe title="Dashboards de Atendimentos CAF" width="100%" height="650" 
src="https://app.powerbi.com/view?r=eyJrIjoiMDU2ZTBhNDEtZWI0ZS00ZGRiLThmZTgtYmQ5YTRjYmE5YTk3IiwidCI6IjJjZjdkNGQ1LWJkMWItNDk1Ni1hY2Y4LTI5OTUzOTliMjE2OCJ9" 
frameborder="0" allowFullScreen="true"></iframe>
""" 

    st.title("Análise de Atendimentos")

    components.html(iframe_code, height=650, width=1800, scrolling=False)

# --- 4. ROTEADOR PRINCIPAL ---
pagina_atual = st.session_state['pagina']

if pagina_atual == 'inicial':
    pagina_inicial()
elif pagina_atual == 'adicionar':
    pagina_adicionar()
elif pagina_atual == 'listar':
    pagina_listar()
elif pagina_atual == 'gerenciar':
    pagina_gerenciar()
elif pagina_atual == 'dashboard':
    gerar_dashboard()
else:
    pagina_inicial()