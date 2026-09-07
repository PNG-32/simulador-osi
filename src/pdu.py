import time


class OSISimulator:

    def __init__(self):
        self.layers = [
            "Aplicação",
            "Apresentação",
            "Sessão",
            "Transporte",
            "Rede",
            "Enlace",
            "Física",
        ]

    def transmitir(self, mensagem: str):
        print("\n=== 📤 TRANSMISSÃO (Encapsulamento) ===")
        dados = mensagem

        # 7. Aplicação
        print(f"[7. {self.layers[0]}] Dados originais: '{dados}'")
        time.sleep(0.4)

        # 6. Apresentação (Simula criptografia/conversão)
        dados = dados.encode("utf-8").hex()
        print(f"[6. {self.layers[1]}] Dados convertidos para Hex: {dados}")
        time.sleep(0.4)

        # 5. Sessão (Simula criação de ID de conexão)
        dados = f"SESSION_ID_9921__{dados}"
        print(f"[5. {self.layers[2]}] Sessão iniciada: {dados}")
        time.sleep(0.4)

        # 4. Transporte (Adiciona portas de origem/destino - TCP/UDP)
        dados = f"[Porta_Origem:443|Porta_Destino:5000] -> {dados}"
        print(f"[4. {self.layers[3]}] Segmento criado: {dados}")
        time.sleep(0.4)

        # 3. Rede (Adiciona IPs de origem/destino)
        dados = f"[IP_Origem:192.168.1.10|IP_Destino:8.8.8.8] -> {dados}"
        print(f"[3. {self.layers[4]}] Pacote criado: {dados}")
        time.sleep(0.4)

        # 2. Enlace (Adiciona MAC Address e checagem de erro CRC)
        dados = f"[MAC_Origem:AA-BB-CC|MAC_Destino:11-22-33] -> {dados} -> [CRC:OK]"
        print(f"[2. {self.layers[5]}] Quadro criado: {dados}")
        time.sleep(0.4)

        # 1. Física (Transforma tudo em bits)
        bits = "".join(format(ord(c), "08b") for c in dados)
        print(
            f"[1. {self.layers[6]}] Transmitindo Bits pelo cabo: {bits[:60]}..."
        )
        time.sleep(0.4)

        return bits

    def receber(self, bits: str):
        print("\n=== 📥 RECEPÇÃO (Desencapsulamento) ===")

        # O processo inverso exato exigiria regex complexo,
        # então simulamos visualmente a subida limpando os headers.
        time.sleep(0.4)
        print(f"[1. {self.layers[6]}] Bits recebidos do meio físico.")

        time.sleep(0.4)
        print(f"[2. {self.layers[5]}] Quadro identificado. CRC verificado.")

        time.sleep(0.4)
        print(f"[3. {self.layers[4]}] Cabeçalho IP removido. Destino correto.")

        time.sleep(0.4)
        print(f"[4. {self.layers[3]}] Portas checadas. Segmento remontado.")

        time.sleep(0.4)
        print(f"[5. {self.layers[2]}] Conexão de sessão encerrada.")

        time.sleep(0.4)
        print(f"[6. {self.layers[1]}] Dados hexadecimais decodificados.")

        time.sleep(0.4)
        print(f"[7. {self.layers[0]}] Mensagem entregue ao usuário final!")


# Execução do simulador
if __name__ == "__main__":
    simulador = OSISimulator()
    msg = "Ola Mundo"
    bits_transmitidos = simulador.transmitir(msg)
    simulador.receber(bits_transmitidos)
