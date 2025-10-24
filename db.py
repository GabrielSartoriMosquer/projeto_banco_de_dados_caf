import sqlite3

def get_conexao():
    return sqlite3.connect("banco.db")

def inicializar_banco():
    """Executa o script SQL se o banco ainda não existir."""
    conexao = get_conexao()
    cursor = conexao.cursor()
    try:
        with open("bd_caf.sql", "r", encoding="utf-8") as f:
            script_sql = f.read()
        cursor.executescript(script_sql)
        conexao.commit()
        print("Banco inicializado com sucesso.")
    except Exception as e:
        print(f"Erro ao inicializar banco: {e}")
    finally:
        conexao.close()

def inserir_beneficiario(pessoa):
    conexao = get_conexao()
    cursor = conexao.cursor()

    cursor.execute("""
    INSERT INTO beneficiarios
    (nome, filiacao1, filiacao2, cpf, data_nascimento, documento_identidade, nacionalidade, email)
    VALUES (?, ?, ?, ?, ?, ?, ?, ?)
    """, (
        pessoa.nome,
        pessoa.filiacao1,
        pessoa.filiacao2,
        pessoa.cpf,
        pessoa.data_nasc,
        pessoa.doc_identidade,
        pessoa.nacionalidade,
        pessoa.email
    ))

    id_beneficiario = cursor.lastrowid

    # Simples: telefone armazenado em um campo único
    cursor.execute("""
    INSERT INTO telefone (codigo_pais, ddd, numero, descricao, fk_beneficiarios_id_beneficiario)
    VALUES (?, ?, ?, ?, ?)
    """, (55, 11, pessoa.telefone, "Residencial", id_beneficiario))

    conexao.commit()
    conexao.close()
    return id_beneficiario

def listar_beneficiarios():
    conexao = get_conexao()
    cursor = conexao.cursor()
    cursor.execute("""
        SELECT id_beneficiario, nome, cpf, data_nascimento 
        FROM beneficiarios
    """)
    resultados = cursor.fetchall()
    conexao.close()
    return resultados

def buscar_beneficiario_por_id(id_beneficiario):
    """Busca um beneficiário completo pelo ID, incluindo o telefone."""
    conexao = get_conexao()
    cursor = conexao.cursor()
    
    cursor.execute("""
        SELECT 
            b.id_beneficiario, b.nome, b.filiacao1, b.filiacao2, b.cpf, 
            b.data_nascimento, b.documento_identidade, b.nacionalidade, b.email,
            t.numero as telefone
        FROM 
            beneficiarios b
        LEFT JOIN 
            telefone t ON b.id_beneficiario = t.fk_beneficiarios_id_beneficiario
        WHERE 
            b.id_beneficiario = ?
        LIMIT 1
    """, (id_beneficiario,))
    
    resultado = cursor.fetchone()
    
    if resultado:
        # Converte a tupla em um dicionário para facilitar o uso
        colunas = [desc[0] for desc in cursor.description]
        conexao.close()
        return dict(zip(colunas, resultado))
    
    conexao.close()
    return None

def atualizar_beneficiario(pessoa):
    """Atualiza os dados de um beneficiário e seu telefone."""
    conexao = get_conexao()
    cursor = conexao.cursor()
    
    try:
        # 1. Atualiza a tabela 'beneficiarios'
        cursor.execute("""
        UPDATE beneficiarios
        SET 
            nome = ?, filiacao1 = ?, filiacao2 = ?, cpf = ?, 
            data_nascimento = ?, documento_identidade = ?, 
            nacionalidade = ?, email = ?
        WHERE 
            id_beneficiario = ?
        """, (
            pessoa.nome, pessoa.filiacao1, pessoa.filiacao2, pessoa.cpf,
            pessoa.data_nasc, pessoa.doc_identidade, pessoa.nacionalidade,
            pessoa.email, pessoa.id_beneficiario
        ))
        
        # 2. Atualiza ou Insere o telefone
        if pessoa.telefone:
            cursor.execute("""
            UPDATE telefone SET numero = ?
            WHERE fk_beneficiarios_id_beneficiario = ?
            """, (pessoa.telefone, pessoa.id_beneficiario))
            
            # Se 'rowcount' for 0, o beneficiário não tinha telefone; então, insira
            if cursor.rowcount == 0:
                 cursor.execute("""
                 INSERT INTO telefone (codigo_pais, ddd, numero, descricao, fk_beneficiarios_id_beneficiario)
                 VALUES (?, ?, ?, ?, ?)
                 """, (55, 48, pessoa.telefone, "Celular", pessoa.id_beneficiario))

        conexao.commit()
    except Exception as e:
        conexao.rollback()
        raise e
    finally:
        conexao.close()

def deletar_beneficiario(id_beneficiario):
    """Deleta um beneficiário e seus dados associados (telefone, etc.)."""
    conexao = get_conexao()
    cursor = conexao.cursor()
    
    try:
        # 1. Deleta das tabelas "filhas" primeiro (devido ao ON DELETE RESTRICT)
        cursor.execute("DELETE FROM telefone WHERE fk_beneficiarios_id_beneficiario = ?", (id_beneficiario,))
        cursor.execute("DELETE FROM atendimentos WHERE fk_beneficiarios_id_beneficiario = ?", (id_beneficiario,))
        cursor.execute("DELETE FROM endereco_beneficiario_tem WHERE fk_beneficiarios_id_beneficiario = ?", (id_beneficiario,))
        
        # 2. Deleta da tabela "pai" (beneficiarios)
        cursor.execute("DELETE FROM beneficiarios WHERE id_beneficiario = ?", (id_beneficiario,))
        
        conexao.commit()
    except Exception as e:
        conexao.rollback()
        raise e
    finally:
        conexao.close()