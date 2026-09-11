
class PDU:
    def __init__(self, mensagem, destino_nome, processo_origem=None, processo_destino=None):
        self.dados = mensagem
        self.destino_nome = destino_nome
        self.processo_origem = processo_origem
        self.processo_destino = processo_destino
        self.cabecalhos = []       # lista de cabecalhos ja acrescentados
        self.unidade = "mensagem"  # mensagem | segmento | pacote | quadro
        self.sessao_id = None      # identificador de sessao (camada 5)
        self.portas = None         # (porta_origem, porta_destino) (camada 4)
        self.logicos = None        # (IP_origem, IP_destino) (camada 3) - fixo ate o destino
        self.fisicos = None        # (MAC_origem, MAC_destino) (camada 2) - muda a cada salto
        self.segmento_indice = None  # posicao deste segmento (1-based) na mensagem original (C7)
        self.segmento_total = None   # quantos segmentos ao todo compoem a mensagem original (C7)

    def clonar_para_segmento(self, dados_fatia, indice, total):
        segmento = PDU(dados_fatia, self.destino_nome, self.processo_origem, self.processo_destino)
        segmento.unidade = "segmento"
        segmento.sessao_id = self.sessao_id
        segmento.portas = self.portas
        segmento.segmento_indice = indice
        segmento.segmento_total = total
        return segmento

    def empilhar_cabecalho(self, camada, tamanho):
        self.cabecalhos.append({"camada": camada, "tamanho": tamanho})

    def desempilhar_cabecalho(self):
        if self.cabecalhos:
            return self.cabecalhos.pop()
        return None
