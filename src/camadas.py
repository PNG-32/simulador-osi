class CamadaOSI:
    def __init__(self, nome):
        self.nome = nome

    def encapsular(self, dados):
        # Adiciona o cabeçalho da camada atual aos dados
        return f"[{self.nome} Header] + ({dados})"

    def decapsular(self, dados):
        # Remove o cabeçalho da camada atual
        partes = dados.split(" + ")
        return partes[1][1:-1] if len(partes) > 1 else dados

# As 7 camadas do modelo
camadas = [
    CamadaOSI("7 - Aplicação"),
    CamadaOSI("6 - Apresentação"),
    CamadaOSI("5 - Sessão"),
    CamadaOSI("4 - Transporte"),
    CamadaOSI("3 - Rede"),
    CamadaOSI("2 - Enlace"),
    CamadaOSI("1 - Física")
]