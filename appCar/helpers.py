#Função criada para retornar em texto o enum
TIPOS_DESCRICAO = {
    1: 'Motocicleta',
    2: 'Carro',
    3: 'Utilitarios',
    4: 'Caminhão',
    5: 'Outros'
}

def get_tipo_descricao(tipo):
    return TIPOS_DESCRICAO.get(tipo, 'Descrição')

ORIGEM = {
    0: 'Proprio',
    1: 'Alugado',
    2: 'Outros'
}

def get_tipo_origem(tipo):
    return ORIGEM.get(tipo, 'Origem')
