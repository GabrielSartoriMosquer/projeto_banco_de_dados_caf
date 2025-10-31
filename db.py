import streamlit as st
from supabase import create_client, Client
from pessoa import Pessoa

# Função para inicializar o cliente Supabase
# @st.cache_resource é crucial para manter uma única conexão
@st.cache_resource
def get_supabase_client() -> Client:
    """
    Cria e retorna o cliente Supabase usando as credenciais
    armazenadas no st.secrets.
    """
    try:
        supabase_url = st.secrets["supabase_url"]
        supabase_key = st.secrets["supabase_key"]
            
        if not supabase_url or not supabase_key:
            raise ValueError("Credenciais do Supabase não encontradas no st.secrets")
                
        return create_client(supabase_url, supabase_key)
        
    except Exception as e:
        st.error(f"Erro ao conectar com Supabase: {e}")
        return None

    # Função de inicialização não é mais necessária para criar tabelas,
    # mas podemos usá-la para verificar a conexão.
def inicializar_banco():
    """
    Verifica se o cliente Supabase pode ser obtido.
    A tabela agora é gerenciada no dashboard do Supabase.
    """
    client = get_supabase_client()
    if client:
        print("Conexão com Supabase estabelecida com sucesso.")
        return True
    else:
        print("Falha ao estabelecer conexão com Supabase.")
        return False

def inserir_beneficiario(p: Pessoa) -> int:
    """
    Insere um novo beneficiário no banco de dados Supabase.
    Retorna o ID do beneficiário inserido.
    """
    client = get_supabase_client()
    dados_dict = p.to_dict()
        
    try:
        # .insert() insere os dados.
        # .execute() envia a requisição.
        response = client.table('beneficiarios').insert(dados_dict).execute()
            
        if response.data:
            # Retorna o ID do registro inserido
            id_gerado = response.data[0]['id']
            return id_gerado
        else:
            raise Exception("Nenhum dado retornado do Supabase após inserção.")
                
    except Exception as e:
        raise Exception(f"Erro ao inserir no Supabase: {e}")

def listar_beneficiarios() -> list:
    """
    Lista ID, Nome, CPF e Data de Nascimento de todos os beneficiários.
    """
    client = get_supabase_client()
    try:
        # Seleciona colunas específicas
        response = client.table('beneficiarios').select('id, nome, cpf, data_nascimento').execute()
            
        # O .data já é uma lista de dicionários, perfeito para o Pandas
        return response.data
            
    except Exception as e:
        raise Exception(f"Erro ao listar no Supabase: {e}")
    
def buscar_beneficiario_por_id(id_beneficiario: int) -> dict:
    """
    Busca um beneficiário completo pelo seu ID.
    Retorna um dicionário.
    """
    client = get_supabase_client()
    try:
        # .eq() é o "equals" (onde id = id_beneficiario)
        # .single() garante que apenas um resultado é esperado
        response = client.table('beneficiarios').select('*').eq('id', id_beneficiario).single().execute()
            
        return response.data # Já é um dicionário
            
    except Exception as e:
        raise Exception(f"Erro ao buscar por ID no Supabase: {e}")

def atualizar_beneficiario(p: Pessoa):
    """
    Atualiza um beneficiário existente com base no seu ID.
    """
    client = get_supabase_client()
    dados_dict = p.to_dict()
        
    try:
        # .update() atualiza os dados
        # .eq() especifica o WHERE
        response = client.table('beneficiarios').update(dados_dict).eq('id', p.id_beneficiario).execute()
            
        if not response.data:
                raise Exception("Falha ao atualizar: beneficiário não encontrado ou erro na query.")

    except Exception as e:
        raise Exception(f"Erro ao atualizar no Supabase: {e}")

def deletar_beneficiario(id_beneficiario: int):
    """
    Deleta um beneficiário pelo seu ID.
    """
    client = get_supabase_client()
    try:
        # .delete() deleta
        # .eq() especifica o WHERE
        response = client.table('beneficiarios').delete().eq('id', id_beneficiario).execute()
            
        if not response.data:
                raise Exception("Falha ao deletar: beneficiário não encontrado ou erro na query.")

    except Exception as e:
        # Supabase pode falhar se houver restrições de chave estrangeira
        # (ex: atendimentos vinculados)
        raise Exception(f"Erro ao deletar no Supabase: {e}")