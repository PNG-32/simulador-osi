from pdu import *
from rede import *

# Camada 7
# Gerar a mensagem e identificar o
# processo pelo nome (endereço específico).
class Lay_7:
    @staticmethod
    def criar_mens(computador, mensagem, destino_nome, processo_origem=None, processo_destino=None):
        pdu = PDU(mensagem, destino_nome, processo_origem, processo_destino)
        print(f'[{computador.nome}] L7 GERA: destino -> {destino_nome}')
        return Lay_6.criptografar(computador, pdu)

    @staticmethod
    def receb_mens(computador, pdu):
        print(f'[{pdu.destino_nome}] L7 ENTREGA: receber -> {computador.nome}')
        print(f'[{pdu.destino_nome}] MENSAGEM DO {computador.nome} -> {pdu.dados}\n')

# Camada 6
# Converter texto em sequência de octetos, registrar o esquema de codificação 
# e cifrar o conteúdo, que só é decifrado na camada 6 do destino.
class Lay_6:
    @staticmethod
    def criptografar(computador, pdu):
        pdu.dados = pdu.dados.encode('utf-8')
        print(f'[{computador.nome}] L6 CODIFICA: octetos UTF-8, conteudo cifrado')
        return Lay_5.abrirCom(computador, pdu)

    @staticmethod
    def descriptografar(computador, pdu):
        pdu.dados = pdu.dados.decode('utf-8')
        print(f'[{pdu.destino_nome}] L6 DECODIFICA: octetos UTF-8, conteudo cifrado')
        return Lay_7.receb_mens(computador, pdu)

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

    @staticmethod
    def FecharCom(computador, pdu):
        print(f'[{pdu.destino_nome}] L5 FECHA: sessao {pdu.sessao_id} estabelecida')
        return Lay_6.descriptografar(computador, pdu)

# Camada 4
#Numerar portas de origem e destino,
#segmentar a mensagem em pelo menos
#três segmentos numerados quando ela
#exceder o limite adotado, e remontá-los
#em ordem na camada 4 do destino
class Lay_4:

    LENGTH_LIMIT = 40

    @staticmethod
    def segmentar(computador, pdu):
        pdu.portas = (pdu.processo_origem, pdu.processo_destino)
        pdu.unidade = "segmento"

        if len(pdu.dados) <= Lay_4.LENGTH_LIMIT:
            pdu.segmento_indice = 1
            pdu.segmento_total = 1
            print(f'[{computador.nome}] L4 SEGMENTA: porta {pdu.processo_origem} -> {pdu.processo_destino}, '
                    f'segmento 1 de 1 ({len(pdu.dados)} B)')
            return Lay_3.encaminhar(computador, pdu)

        fatias = [pdu.dados[i:i + Lay_4.LENGTH_LIMIT] for i in range(0, len(dados), Lay_4.LENGTH_LIMIT)]
        total = len(fatias)
        resultado = None
        for indice, fatia in enumerate(fatias, start=1):
            segmento = pdu.clonar_para_segmento(fatia, indice, total)
            print(f'[{computador.nome}] L4 SEGMENTA: porta {pdu.processo_origem} -> {pdu.processo_destino}, '
                    f'segmento {indice} de {total} ({len(fatia)} B)')
            resultado = Lay_3.encaminhar(computador, segmento)
        return resultado
    
    @staticmethod
    def remonta(computador, pdu):
        pdu.portas = (pdu.processo_origem, pdu.processo_destino)
        pdu.unidade = "segmento"
        pdu.dados = "".join(pdu.dados)
        # TODO (C7): dividir em >= 3 segmentos numerados quando exceder o limite adotado
        print(f'[{pdu.destino_nome}] L4 REMONTA: porta {pdu.processo_destino} -> {pdu.processo_origem}')
        return Lay_5.FecharCom(computador, pdu)

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
            pdu.logicos = (dispositivo.interfaces[0]["IPv4"], None) 
            pdu.unidade = "pacote"

        print(f'[{dispositivo.nome}] L3 ENCAPSULA/ROTEIA: {pdu.logicos}')
        return Lay_2.enquadrar(dispositivo, pdu)

    @staticmethod
    def receber(dispositivo, pdu):
        pdu.unidade = "pacote"
        if dispositivo.nome == pdu.destino_nome:
            print(f'[{pdu.destino_nome}] L3 ENTREGA: pacote chegou ao destino final')
            return Lay_4.remontar(dispositivo, pdu)
        print(f'[{pdu.destino_nome}] L3 REPASSA: nao sou o destino, continuo roteando')
        return Lay_4.remonta(dispositivo, pdu)

    @staticmethod
    def buscar_dispositivo(nome):
        try:
            with open(Topologia, "r") as file:
                data = json.load(file)
        except FileNotFoundError:
            print(f"Error: '{Topologia}' file was not found.")
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
        print(f'[{dispositivo.nome}] L2 ENQUADRA')
        return Lay_1.transmitir(dispositivo, pdu)

    @staticmethod
    def desenquadrar(dispositivo, pdu):
        pdu.unidade = "pacote"
        print(f'[{pdu.destino_nome}] L2 DESENQUADRA')
        return Lay_3.receber(dispositivo, pdu)

    
    
# Camada 1
# Converter o quadro em uma sequência de
# bits e transportá-la pelo enlace 
class Lay_1:
    @staticmethod
    def transmitir(dispositivo, pdu):
        print(f'[{dispositivo.nome}] L1 TRANSMITE')
        return Lay_1.receber(dispositivo, pdu)

    @staticmethod
    def receber(dispositivo, pdu):
        print(f'[{pdu.destino_nome}] L1 RECEBE')
        return Lay_2.desenquadrar(dispositivo, pdu)