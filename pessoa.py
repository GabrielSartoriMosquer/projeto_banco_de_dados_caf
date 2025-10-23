class Pessoa:
    def __init__(self, nome, filiacao1, filiacao2, data_nasc, doc_identidade, nacionalidade, telefone, email, endereco_residencial,endereco_trabalho, cpf=None, id_beneficiario=None):
        self.nome = nome
        self.filiacao1 = filiacao1
        self.filiacao2 = filiacao2
        self.cpf = cpf
        self.data_nasc = data_nasc
        self.doc_identidade = doc_identidade
        self.nacionalidade = nacionalidade
        self.telefone = telefone
        self.email = email
        self.endereco_residencial = endereco_residencial
        self.endereco_trabalho = endereco_trabalho
        self.id_beneficiario = id_beneficiario

    def __str__(self):
        return f"Nome: {self.nome}, CPF: {self.cpf}, Data Nasc: {self.data_nasc}"