
class Dispositivo:
    #Base para qualquer nó da rede. Guarda só o que é comum:
    #nome e a lista de interfaces (endereço lógico + físico)

    def __init__(self, nome, interfaces):
        self.nome = nome
        self.interfaces = interfaces  # lista de dicts: {interface, IPv4, fisico}

    def interface_por_nome(self, nome_interface):
        for iface in self.interfaces:
            if iface["interface"] == nome_interface:
                return iface
        return None

    def __repr__(self):
        return f"<{self.__class__.__name__} {self.nome}>"

class Computador(Dispositivo):
    # Implementa as 7 camadas (Tabela 2 do enunciado).

    def enviar(self, mensagem, destino_nome, processo_origem=None, processo_destino=None):
        from camadas import Lay_7
        return Lay_7.criar_mens(self, mensagem, destino_nome, processo_origem, processo_destino)


class Roteador(Dispositivo):
    #Implementa só L1-L3. Por design, esta classe não tem
    #nenhum atributo ou método relacionado a L4-L7 — é assim que
    #a restrição R1 do enunciado ('o roteador não lê o que não
    #lhe pertence') fica garantida pela própria estrutura, e não
    #por uma checagem manual.

    def encaminhar(self, pacote):
        from camadas import Lay_3
        return Lay_3.encaminhar(self, pacote)
