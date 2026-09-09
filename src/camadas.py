import json


class PDU:
    def __init__(self, mensagem, destino_nome, processo_origem=None, processo_destino=None):
        self.dados = mensagem
        self.destino_nome = destino_nome
        self.processo_origem = processo_origem
        self.processo_destino = processo_destino
        self.cabecalhos = []
        self.unidade = "mensagem"
        self.sessao_id = None
        self.portas = None
        self.logicos = None
        self.fisicos = None

    def empilhar_cabecalho(self, camada, tamanho):
        self.cabecalhos.append({"camada": camada, "tamanho": tamanho})

# Camada 7
# Gerar a mensagem e identificar o
# processo pelo nome (endereço específico).
class Lay_7:
    def criar_mens():
        input_string = input('Digite um número: ')
        dados_atuais = Lay_6.Criptografar(input_string)
        return print(dados_atuais)

# Camada 6
# Converter texto em sequência de octetos, registrar o esquema de codificação 
# e cifrar o conteúdo, que só é decifrado na camada 6 do destino.
class Lay_6:
    @staticmethod
    def criptografar(computador, pdu):
        pdu.dados = pdu.dados.encode('utf-8')
        print(f'[{computador.nome}] L6 CODIFICA: octetos UTF-8, conteudo cifrado')
        return Lay_5.abrirCom(computador, pdu)

# Camada 5
# Abrir, manter e encerrar o diálogo,
# atribuindo um identificador de sessão.
class Lay_5:
    _contador_sessao = 0

    @staticmethod
    def abrirCom(computador, pdu):
        Lay_5._contador_sessao += 1
        pdu.sessao_id = f"S-{Lay_5._contador_sessao:04d}"
        print(f'[{computador.nome}] L5 ABRE: sessao {pdu.sessao_id} estabelecida')
        return Lay_4.segmentar(computador, pdu)

# Camada 4
#Numerar portas de origem e destino,
#segmentar a mensagem em pelo menos
#três segmentos numerados quando ela
#exceder o limite adotado, e remontá-los
#em ordem na camada 4 do destino
class Lay_4:
    @staticmethod
    def segmentar(computador, pdu):
        pdu.portas = (pdu.processo_origem, pdu.processo_destino)
        pdu.unidade = "segmento"
        # TODO (C7): dividir em >= 3 segmentos numerados quando exceder o limite adotado
        print(f'[{computador.nome}] L4 SEGMENTA: porta {pdu.processo_origem} -> {pdu.processo_destino}')
        return Lay_3.encaminhar(computador, pdu)

# Camada 3
# Inserir o par de endereços lógicos e
# consultar a tabela de encaminhamento.
class Lay_3:
    @staticmethod
    def encaminhar(dispositivo, pdu):
        destino_bruto = Lay_3.buscar_dispositivo(pdu.destino_nome)
        if destino_bruto is None:
            print(f'[{dispositivo.nome}] L3 DESCARTA: destino {pdu.destino_nome} inalcancavel')
            return None

        if pdu.logicos is None:
            pdu.logicos = (dispositivo.interfaces[0]["IPv4"], None)  # TODO: IP real do destino
            pdu.unidade = "pacote"

        print(f'[{dispositivo.nome}] L3 ENCAPSULA/ROTEIA: {pdu.logicos}')
        # TODO: consultar tabela de encaminhamento (rede.py) para decidir o proximo salto real
        return Lay_2.enquadrar(dispositivo, pdu)

    @staticmethod
    def buscar_dispositivo(nome):
        try:
            with open("topologia.json", "r") as file:
                data = json.load(file)
        except FileNotFoundError:
            print("Error: 'topologia.json' file was not found.")
            return None
        for bruto in data:
            if bruto["dispositivo"] == nome:
                return bruto
        return None

# Camada 2
# Inserir o par de endereços físicos do salto,
# delimitar o quadro e calcular a
# verificação de erro.
class Lay_2:
    @staticmethod
    def enquadrar(dispositivo, pdu):
        pdu.unidade = "quadro"
        # TODO: par de enderecos fisicos do salto corrente (rede.py fornece o proximo salto)
        print(f'[{dispositivo.nome}] L2 ENQUADRA')
        return Lay_1.transmitir(dispositivo, pdu)
    
# Camada 1
# Converter o quadro em uma sequência de
# bits e transportá-la pelo enlace 
class Lay_1:
    @staticmethod
    def transmitir(dispositivo, pdu):
        print(f'[{dispositivo.nome}] L1 TRANSMITE')
        return pdu