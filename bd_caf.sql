-- Tabelas sem chaves estrangeiras (iguais ao original)
CREATE TABLE beneficiarios (
    id_beneficiario INTEGER PRIMARY KEY,
    nome VARCHAR,
    filiacao1 VARCHAR,
    filiacao2 VARCHAR,
    cpf VARCHAR,
    data_nascimento DATE,
    documento_identidade VARCHAR,
    nacionalidade VARCHAR,
    email VARCHAR
);

CREATE TABLE atendentes (
    id_atendente INTEGER PRIMARY KEY,
    nome VARCHAR
);

CREATE TABLE pais (
    nome VARCHAR,
    id_pais INTEGER PRIMARY KEY,
    sigla VARCHAR
);

CREATE TABLE tipo_logradouro (
    nome VARCHAR,
    id_tipo_logradouro INTEGER PRIMARY KEY
);


-- Tabelas COM chaves estrangeiras (SINTAXE CORRIGIDA PARA SQLITE)
CREATE TABLE estado (
    id_estado INTEGER PRIMARY KEY,
    nome VARCHAR,
    fk_pais_id_pais INTEGER,
    FOREIGN KEY (fk_pais_id_pais)
        REFERENCES pais (id_pais)
        ON DELETE RESTRICT
);

CREATE TABLE cidade (
    nome VARCHAR,
    id_cidade INTEGER PRIMARY KEY,
    fk_estado_id_estado INTEGER,
    FOREIGN KEY (fk_estado_id_estado)
        REFERENCES estado (id_estado)
        ON DELETE RESTRICT
);

CREATE TABLE bairro (
    id_bairro INTEGER PRIMARY KEY,
    nome VARCHAR,
    fk_cidade_id_cidade INTEGER,
    FOREIGN KEY (fk_cidade_id_cidade)
        REFERENCES cidade (id_cidade)
        ON DELETE RESTRICT
);

CREATE TABLE endereco (
    numero INTEGER,
    nome_logradouro VARCHAR,
    CEP INTEGER,
    complemento VARCHAR,
    id_endereco INTEGER PRIMARY KEY,
    fk_bairro_id_bairro INTEGER,
    fk_tipo_logradouro_id_tipo_logradouro INTEGER,
    FOREIGN KEY (fk_bairro_id_bairro)
        REFERENCES bairro (id_bairro)
        ON DELETE RESTRICT,
    FOREIGN KEY (fk_tipo_logradouro_id_tipo_logradouro)
        REFERENCES tipo_logradouro (id_tipo_logradouro)
        ON DELETE RESTRICT
);

CREATE TABLE atendimentos (
    id_atendimento INTEGER PRIMARY KEY,
    data DATE,
    hora TIME,
    observacao VARCHAR,
    fk_beneficiarios_id_beneficiario INTEGER,
    fk_atendentes_id_atendente INTEGER,
    FOREIGN KEY (fk_beneficiarios_id_beneficiario)
        REFERENCES beneficiarios (id_beneficiario)
        ON DELETE RESTRICT,
    FOREIGN KEY (fk_atendentes_id_atendente)
        REFERENCES atendentes (id_atendente)
        ON DELETE RESTRICT
);
 
CREATE TABLE telefone (
    id_telefone INTEGER PRIMARY KEY,
    codigo_pais INTEGER,
    ddd INTEGER,
    numero INTEGER,
    descricao VARCHAR,
    fk_beneficiarios_id_beneficiario INTEGER,
    FOREIGN KEY (fk_beneficiarios_id_beneficiario)
        REFERENCES beneficiarios (id_beneficiario)
        ON DELETE RESTRICT
);
 
CREATE TABLE endereco_beneficiario_tem (
    tipo_endereco VARCHAR,
    fk_beneficiarios_id_beneficiario INTEGER,
    fk_endereco_id_endereco INTEGER,
    FOREIGN KEY (fk_beneficiarios_id_beneficiario)
        REFERENCES beneficiarios (id_beneficiario),
    FOREIGN KEY (fk_endereco_id_endereco)
        REFERENCES endereco (id_endereco)
);

--CRIAÇÃO DE USUÁRIOS FICTÍCIOS

-- Inserindo dados na tabela pais
INSERT INTO pais (id_pais, nome, sigla) VALUES
(1, 'Brasil', 'BRA'),
(2, 'Argentina', 'ARG'),
(3, 'Uruguai', 'URY'),
(4, 'Chile', 'CHL'),
(5, 'Peru', 'PER'),
(6, 'Colômbia', 'COL'),
(7, 'Bolívia', 'BOL'),
(8, 'Venezuela', 'VEN'),
(9, 'Paraguai', 'PRY');

-- Inserindo dados na tabela estado (Apenas Santa Catarina, pois todos os endereços são em Florianópolis)
INSERT INTO estado (id_estado, nome, fk_pais_id_pais) VALUES
(1, 'Santa Catarina', 1);

-- Inserindo dados na tabela cidade (Apenas Florianópolis)
INSERT INTO cidade (id_cidade, nome, fk_estado_id_estado) VALUES
(1, 'Florianópolis', 1);

-- Inserindo dados na tabela tipo_logradouro
INSERT INTO tipo_logradouro (id_tipo_logradouro, nome) VALUES
(1, 'Rua'),
(2, 'Avenida'),
(3, 'Servidão'),
(4, 'Travessa');

-- Inserindo dados na tabela bairro (Bairros de Florianópolis)
INSERT INTO bairro (id_bairro, nome, fk_cidade_id_cidade) VALUES
(1, 'Centro', 1),
(2, 'Trindade', 1),
(3, 'Campeche', 1),
(4, 'Ingleses do Rio Vermelho', 1),
(5, 'Canasvieiras', 1);

-- Inserindo dados na tabela atendentes
INSERT INTO atendentes (id_atendente, nome) VALUES
(1, 'Carlos Andrade'),
(2, 'Mariana Oliveira'),
(3, 'Pedro Santos');

-- Inserindo dados na tabela beneficiarios (20 pessoas fictícias)
INSERT INTO beneficiarios (id_beneficiario, nome, filiacao1, filiacao2, cpf, data_nascimento, documento_identidade, nacionalidade, email) VALUES
(1, 'Javier Morales', 'Ricardo Morales', 'Elena Fernandez', '11122233344', '1990-05-15', 'ARG-23456789', 'Argentina', 'javier.morales@email.com'),
(2, 'Sofia Rojas', 'Mateo Rojas', 'Valentina Gomez', '22233344455', '1988-11-20', 'CHL-18901234', 'Chilena', 'sofia.rojas@email.com'),
(3, 'Mateo Ferreira', 'Lucas Ferreira', 'Isabella Acosta', '33344455566', '1995-02-10', 'URY-45678901', 'Uruguaia', 'mateo.ferreira@email.com'),
(4, 'Camila Flores', 'Sebastian Flores', 'Gabriela Quispe', '44455566677', '1992-09-30', 'PER-78901234', 'Peruana', 'camila.flores@email.com'),
(5, 'Santiago Diaz', 'Alejandro Diaz', 'Valeria Torres', '55566677788', '1985-07-25', 'COL-56789012', 'Colombiana', 'santiago.diaz@email.com'),
(6, 'Valentina Chavez', 'Daniel Chavez', 'Lucia Mendoza', '66677788899', '1998-01-12', 'VEN-90123456', 'Venezuelana', 'valentina.chavez@email.com'),
(7, 'Lucas Mamani', 'Miguel Mamani', 'Beatriz Vargas', '77788899900', '1991-04-05', 'BOL-34567890', 'Boliviana', 'lucas.mamani@email.com'),
(8, 'Isabella Romero', 'Carlos Romero', 'Paula Benitez', '88899900011', '1993-08-18', 'PRY-67890123', 'Paraguaia', 'isabella.romero@email.com'),
(9, 'Benjamin Soto', 'Jorge Soto', 'Andrea Castro', '99900011122', '1987-03-22', 'CHL-19876543', 'Chilena', 'benjamin.soto@email.com'),
(10, 'Martina Castillo', 'Luis Castillo', 'Jimena Ortiz', '10101010101', '1996-12-01', 'ARG-34567890', 'Argentina', 'martina.castillo@email.com'),
(11, 'Agustin Gimenez', 'Roberto Gimenez', 'Laura Sosa', '20202020202', '1989-10-14', 'URY-56789012', 'Uruguaia', 'agustin.gimenez@email.com'),
(12, 'Florencia Paredes', 'Gustavo Paredes', 'Silvia Rios', '30303030303', '1994-06-08', 'PRY-89012345', 'Paraguaia', 'florencia.paredes@email.com'),
(13, 'Matias Garcia', 'Hernan Garcia', 'Monica Rodriguez', '40404040404', '1990-11-27', 'ARG-45678901', 'Argentina', 'matias.garcia@email.com'),
(14, 'Catalina Vega', 'Andres Vega', 'Constanza Reyes', '50505050505', '1997-05-19', 'CHL-20987654', 'Chilena', 'catalina.vega@email.com'),
(15, 'Juan Ramirez', 'Diego Ramirez', 'Carmen Sanchez', '60606060606', '1986-02-28', 'COL-67890123', 'Colombiana', 'juan.ramirez@email.com'),
(16, 'Daniela Cruz', 'Oscar Cruz', 'Adriana Lopez', '70707070707', '1991-07-03', 'PER-90123456', 'Peruana', 'daniela.cruz@email.com'),
(17, 'Emilio Herrera', 'Fernando Herrera', 'Marcela Navarro', '80808080808', '1984-09-09', 'VEN-23456789', 'Venezuelana', 'emilio.herrera@email.com'),
(18, 'Renata Guzman', 'Raul Guzman', 'Teresa Pinto', '90909090909', '1999-03-16', 'BOL-45678901', 'Boliviana', 'renata.guzman@email.com'),
(19, 'Facundo Ibañez', 'Sergio Ibañez', 'Norma Pereyra', '12121212121', '1992-10-21', 'ARG-56789012', 'Argentina', 'facundo.ibanez@email.com'),
(20, 'Valeria Morales', 'Jose Morales', 'Pilar Silva', '23232323232', '1993-12-30', 'CHL-21098765', 'Chilena', 'valeria.morales@email.com');

-- Inserindo dados na tabela endereco (20 endereços fictícios em Florianópolis)
INSERT INTO endereco (id_endereco, nome_logradouro, numero, CEP, complemento, fk_bairro_id_bairro, fk_tipo_logradouro_id_tipo_logradouro) VALUES
(1, 'Felipe Schmidt', 100, 88010001, 'Apto 101', 1, 1),
(2, 'Lauro Linhares', 2050, 88036002, 'Bloco A', 2, 2),
(3, 'Pequeno Príncipe', 300, 88063000, 'Casa', 3, 2),
(4, 'das Gaivotas', 450, 88058100, 'Fundos', 4, 1),
(5, 'das Nações', 120, 88054010, 'Sala 3', 5, 2),
(6, 'Conselheiro Mafra', 220, 88010101, 'Apto 202', 1, 1),
(7, 'Madre Benvenuta', 1500, 88035000, 'Casa 5', 2, 2),
(8, 'dos Eucaliptos', 80, 88063100, 'Perto da praia', 3, 3),
(9, 'Intendente João Nunes Vieira', 1800, 88058500, 'Loja 1', 4, 1),
(10, 'Maria Villarim', 330, 88054601, 'Apto 5B', 5, 1),
(11, 'Deodoro', 50, 88010020, 'Sobreloja', 1, 1),
(12, 'Córrego Grande', 1234, 88037000, 'Apto 301', 2, 1),
(13, 'Avenida Campeche', 2500, 88065000, NULL, 3, 2),
(14, 'Dário Manoel Cardoso', 670, 88058400, 'Casa Amarela', 4, 1),
(15, 'Manoel de Menezes', 90, 88054300, NULL, 5, 3),
(16, 'Tenente Silveira', 300, 88010300, 'Andar 4', 1, 1),
(17, 'João Pio Duarte Silva', 555, 88037001, 'Bloco C, Apto 10', 2, 1),
(18, 'do Gramal', 199, 88065160, NULL, 3, 1),
(19, 'Dom João Becker', 700, 88058075, 'Apto 707', 4, 1),
(20, 'dos Lordes', 12, 88054520, 'Casa Verde', 5, 1);

-- Inserindo dados na tabela telefone (um para cada beneficiário)
INSERT INTO telefone (id_telefone, codigo_pais, ddd, numero, descricao, fk_beneficiarios_id_beneficiario) VALUES
(1, 55, 48, 991234567, 'Celular', 1), (2, 55, 48, 992345678, 'Celular', 2), (3, 55, 48, 993456789, 'Celular', 3), (4, 55, 48, 994567890, 'Celular', 4), (5, 55, 48, 995678901, 'Celular', 5), (6, 55, 48, 996789012, 'Celular', 6), (7, 55, 48, 997890123, 'Celular', 7), (8, 55, 48, 998901234, 'Celular', 8), (9, 55, 48, 989012345, 'Celular', 9), (10, 55, 48, 980123456, 'Celular', 10), (11, 55, 48, 981234567, 'Celular', 11), (12, 55, 48, 982345678, 'Celular', 12), (13, 55, 48, 983456789, 'Celular', 13), (14, 55, 48, 984567890, 'Celular', 14), (15, 55, 48, 985678901, 'Celular', 15), (16, 55, 48, 986789012, 'Celular', 16), (17, 55, 48, 987890123, 'Celular', 17), (18, 55, 48, 988901234, 'Celular', 18), (19, 55, 48, 979012345, 'Celular', 19), (20, 55, 48, 970123456, 'Celular', 20);

-- Inserindo dados na tabela endereco_beneficiario_tem (ligando cada beneficiário a um endereço)
INSERT INTO endereco_beneficiario_tem (fk_beneficiarios_id_beneficiario, fk_endereco_id_endereco, tipo_endereco) VALUES
(1, 1, 'Residencial'), (2, 2, 'Residencial'), (3, 3, 'Residencial'), (4, 4, 'Residencial'), (5, 5, 'Comercial'), (6, 6, 'Residencial'), (7, 7, 'Residencial'), (8, 8, 'Residencial'), (9, 9, 'Comercial'), (10, 10, 'Residencial'), (11, 11, 'Residencial'), (12, 12, 'Residencial'), (13, 13, 'Residencial'), (14, 14, 'Residencial'), (15, 15, 'Residencial'), (16, 16, 'Residencial'), (17, 17, 'Comercial'), (18, 18, 'Residencial'), (19, 19, 'Residencial'), (20, 20, 'Residencial');

-- Inserindo dados na tabela atendimentos (um atendimento para cada beneficiário)
INSERT INTO atendimentos (id_atendimento, data, hora, observacao, fk_beneficiarios_id_beneficiario, fk_atendentes_id_atendente) VALUES
(1, '2025-09-22', '09:30:00', 'Primeiro contato, agendado retorno.', 1, 1),
(2, '2025-09-22', '10:00:00', 'Verificação de documentos.', 2, 2),
(3, '2025-09-22', '11:15:00', 'Pendente entregar comprovante.', 3, 3),
(4, '2025-09-23', '08:45:00', 'Solicitação de informações.', 4, 1),
(5, '2025-09-23', '09:00:00', 'Análise de cadastro.', 5, 2),
(6, '2025-09-23', '10:30:00', 'Documentação OK.', 6, 1),
(7, '2025-09-23', '11:00:00', 'Encaminhado para setor responsável.', 7, 3),
(8, '2025-09-24', '14:00:00', 'Retorno para assinatura.', 8, 2),
(9, '2025-09-24', '14:30:00', 'Cadastro finalizado com sucesso.', 9, 1),
(10, '2025-09-24', '15:00:00', 'Tirou dúvidas sobre o processo.', 10, 3),
(11, '2025-09-24', '16:00:00', 'Atualização de dados cadastrais.', 11, 2),
(12, '2025-09-25', '09:00:00', 'Entregou documentação pendente.', 12, 1),
(13, '2025-09-25', '09:45:00', 'Consulta sobre andamento.', 13, 1),
(14, '2025-09-25', '10:15:00', 'Solicitou cópia do protocolo.', 14, 3),
(15, '2025-09-25', '11:30:00', 'Informações gerais.', 15, 2),
(16, '2025-09-26', '08:30:00', 'Agendamento de nova visita.', 16, 2),
(17, '2025-09-26', '09:00:00', 'Verificação de endereço comercial.', 17, 3),
(18, '2025-09-26', '10:00:00', 'Aguardando liberação.', 18, 1),
(19, '2025-09-26', '10:45:00', 'Protocolo aberto.', 19, 1),
(20, '2025-09-26', '11:00:00', 'Finalização do atendimento.', 20, 2);