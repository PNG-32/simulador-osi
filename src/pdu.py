
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

    def empilhar_cabecalho(self, camada, tamanho):
        self.cabecalhos.append({"camada": camada, "tamanho": tamanho})

    def desempilhar_cabecalho(self):
        """Remove e devolve o cabecalho mais externo (usado na subida da pilha)."""
        if self.cabecalhos:
            return self.cabecalhos.pop()
        return None
