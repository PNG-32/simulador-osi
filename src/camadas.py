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
        return pdu

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
    def encerrarCom(computador, pdu):
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
    _buffer_remontagem = {}

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

        fatias = [pdu.dados[i:i + Lay_4.LENGTH_LIMIT] for i in range(0, len(pdu.dados), Lay_4.LENGTH_LIMIT)]
        total = len(fatias)
        resultado = None
        for indice, fatia in enumerate(fatias, start=1):
            segmento = pdu.clonar_para_segmento(fatia, indice, total)
            print(f'[{computador.nome}] L4 SEGMENTA: porta {pdu.processo_origem} -> {pdu.processo_destino}, '
                    f'segmento {indice} de {total} ({len(fatia)} B)')
            resultado = Lay_3.encaminhar(computador, segmento)
        return resultado
    
    @staticmethod
    def remontar(computador, pdu):
        total = pdu.segmento_total or 1
        
        if total == 1:
            print(f'[{computador.nome}] L4 REMONTA: porta {pdu.portas[1]}, segmento unico recebido')
            return Lay_5.encerrarCom(computador, pdu)
        
        chave_fluxo = (pdu.logicos[0], pdu.portas[0], pdu.portas[1])  # (IP origem, porta origem, porta destino) - o "socket" da camada 4
        buffer = Lay_4._buffer_remontagem.setdefault(chave_fluxo, [])
        buffer.append((pdu.segmento_indice, pdu.dados))
        print(f'[{computador.nome}] L4 REMONTA: segmento {pdu.segmento_indice} de {total} recebido '
                f'({len(buffer)}/{total})')

        if len(buffer) < total:
            
            return None  # ainda faltam segmentos: so sobe quando tiver todos

        buffer.sort(key=lambda par: par[0])
        pdu.dados = b"".join(fatia for _, fatia in buffer)
        del Lay_4._buffer_remontagem[chave_fluxo]
        print(f'[{computador.nome}] L4 REMONTA: {total} segmentos reordenados, sessao {pdu.sessao_id} completa')
        return Lay_5.encerrarCom(computador, pdu)

# Camada 3
# Inserir o par de endereços lógicos e
# consultar a tabela de encaminhamento.
class Lay_3:
    @staticmethod
    def encaminhar(dispositivo, pdu):
        proximo, iface_saida, iface_entrada = proximo_salto(dispositivo, pdu.destino_nome)
        if proximo is None:
            print(f'[{dispositivo.nome}] L3 DESCARTA: destino {pdu.destino_nome} inalcancavel')
            return None

        if pdu.logicos is None:
            pdu.logicos = (dispositivo.interfaces[0]["IPv4"], ip_de(pdu.destino_nome))
            pdu.unidade = "pacote"

        pdu.proximo_dispositivo = proximo
        pdu.iface_saida = iface_saida
        pdu.iface_entrada = iface_entrada
        print(f'[{dispositivo.nome}] L3 ENCAPSULA/ROTEIA: {pdu.logicos} -> proximo salto {proximo.nome}')
        return Lay_2.enquadrar(dispositivo, pdu)

    @staticmethod
    def receber(dispositivo, pdu):
        pdu.unidade = "pacote"
        if dispositivo.nome == pdu.destino_nome:
            print(f'[{dispositivo.nome}] L3 ENTREGA: pacote chegou ao destino final')
            return Lay_4.remontar(dispositivo, pdu)
        print(f'[{dispositivo.nome}] L3 REPASSA: nao sou o destino, continuo roteando')
        return Lay_3.encaminhar(dispositivo, pdu)


# Camada 2
# Inserir o par de endereços físicos do salto,
# delimitar o quadro e calcular a
# verificação de erro.
class Lay_2:
    _contador_quadro = 0

    @staticmethod
    def enquadrar(dispositivo, pdu):
        pdu.unidade = "quadro"
        mac_origem = pdu.iface_saida["fisico"]
        mac_destino = pdu.iface_entrada["fisico"]
        pdu.fisicos = (mac_origem, mac_destino)
        Lay_2._contador_quadro += 1
        pdu.quadro_id = f"Q{Lay_2._contador_quadro}"
        print(f'[{dispositivo.nome}] L2 ENQUADRA: {mac_origem} -> {mac_destino}, quadro {pdu.quadro_id}')
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
        print(f'[{dispositivo.nome}] L1 TRANSMITE: {pdu.quadro_id} ({len(pdu.dados) if hasattr(pdu.dados, "__len__") else "?"} B)')
        proximo = pdu.proximo_dispositivo
        return Lay_1.receber(proximo, pdu)

    @staticmethod
    def receber(dispositivo, pdu):
        print(f'[{dispositivo.nome}] L1 RECEBE')
        return Lay_2.desenquadrar(dispositivo, pdu)