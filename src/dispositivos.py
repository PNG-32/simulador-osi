import json


class Dispositivo:
    """Base para qualquer nó da rede. Guarda só o que é comum:
    nome e a lista de interfaces (endereço lógico + físico)."""

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
    """Implementa as 7 camadas (Tabela 2 do enunciado)."""

    def enviar(self, mensagem, destino_nome):
        from camadas import Lay_7
        return Lay_7.criar_mens(self, mensagem, destino_nome)


class Roteador(Dispositivo):
    """Implementa só L1-L3. Por design, esta classe não tem
    nenhum atributo ou método relacionado a L4-L7 — é assim que
    a restrição R1 do enunciado ('o roteador não lê o que não
    lhe pertence') fica garantida pela própria estrutura, e não
    por uma checagem manual."""

    def encaminhar(self, pacote):
        from camadas import Lay_3
        return Lay_3.encaminhar(self, pacote)


def _normalizar_interfaces(bruto):
    """Uniformiza o formato do topologia.json. Computador vs
    Roteador é decidido pelo formato do dado (str = uma interface,
    list = várias), não pelo nome do dispositivo — assim o arquivo
    de topologia continua podendo ser trocado livremente (R obrigatório
    do enunciado: trocar a rede só trocando o JSON)."""
    if isinstance(bruto["interface"], str):
        return [{
            "interface": bruto["interface"],
            "IPv4": bruto["IPv4"],
            "fisico": bruto["Physical Address"],
        }]

    interfaces = []
    for i, iface in enumerate(bruto["interface"]):
        interfaces.append({
            "interface": iface[""],
            "info": iface.get("info", ""),
            "IPv4": bruto["IPv4"][i][""],
            "fisico": bruto["Physical Address"][i][""],
        })
    return interfaces


def carregar_dispositivos(caminho="topologia.json"):
    """Lê o arquivo de topologia e devolve {nome: Dispositivo}."""
    try:
        with open(caminho, "r") as file:
            data = json.load(file)
    except FileNotFoundError:
        print(f"Error: '{caminho}' file was not found.")
        return {}

    dispositivos = {}
    for bruto in data:
        nome = bruto["dispositivo"]
        interfaces = _normalizar_interfaces(bruto)
        eh_computador = isinstance(bruto["interface"], str)
        classe = Computador if eh_computador else Roteador
        dispositivos[nome] = classe(nome, interfaces)
    return dispositivos