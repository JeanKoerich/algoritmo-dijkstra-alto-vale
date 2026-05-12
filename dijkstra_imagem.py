
import tkinter as tk
from tkinter import ttk, messagebox
from PIL import Image, ImageTk, ImageDraw
import heapq

# Nome da imagem do grafo
IMAGEM_GRAFO = "grafo_mapa.png"

# -----------------------------
# CIDADES
# -----------------------------
cidades = {
    "RSL": "Rio do Sul",
    "LON": "Lontras",
    "AGR": "Agronômica",
    "TCO": "Trombudo Central",
    "BTO": "Braço do Trombudo",
    "PDR": "Pouso Redondo",
    "LAU": "Laurentino",
    "IBR": "Ibirama",
    "PGT": "Presidente Getúlio",
    "AGD": "Agrolândia",
    "AUR": "Aurora",
    "ATL": "Atalanta",
    "ITU": "Ituporanga",
    "VRA": "Vidal Ramos",
    "PNR": "Presidente Nereu",
    "IMB": "Imbuia",
    "MDC": "Mirim Doce",
    "TAI": "Taió",
    "DEM": "Dona Emma",
    "JBT": "José Boiteux"
}

# -----------------------------
# POSIÇÕES EM PIXELS NA IMAGEM
# Ajuste se algum ponto ficar fora do lugar
# -----------------------------
posicoes = {
    "RSL": (625, 369),
    "LON": (728, 307),
    "AGR": (543, 390),
    "TCO": (456, 475),
    "BTO": (357, 545),
    "PDR": (307, 416),
    "LAU": (528, 366),
    "IBR": (765, 174),
    "PGT": (655, 156),
    "AGD": (420, 596),
    "AUR": (642, 483),
    "ATL": (475, 613),
    "ITU": (677, 588),
    "VRA": (933, 586),
    "PNR": (910, 444),
    "IMB": (879, 701),
    "MDC": (154, 347),
    "TAI": (232, 247),
    "DEM": (576, 90),
    "JBT": (653, 63)
}

# -----------------------------
# ARESTAS COM CUSTO
# -----------------------------
arestas = [
    ("RSL", "LON", 25.6),
    ("RSL", "AGR", 31.2),
    ("AGR", "TCO", 23.6),
    ("TCO", "BTO", 43.2),
    ("BTO", "PDR", 38.28),
    ("TCO", "PDR", 54.9),
    ("AGR", "PDR", 71.94),
    ("PDR", "MDC", 37.4),
    ("PDR", "TAI", 38.8),
    ("RSL", "LAU", 39.9),
    ("RSL", "PGT", 121.88),
    ("LON", "IBR", 35.0),
    ("IBR", "PGT", 25.2),
    ("PGT", "DEM", 33.4),
    ("PGT", "JBT", 32.4),
    ("RSL", "AUR", 28.0),
    ("RSL", "TCO", 79.64),
    ("TCO", "AGD", 14.1),
    ("AGD", "ATL", 12.2),
    ("ATL", "ITU", 43.6),
    ("AUR", "ITU", 39.9),
    ("ITU", "IMB", 76.5),
    ("ITU", "VRA", 63.2),
    ("VRA", "IMB", 39.6),
    ("VRA", "PNR", 42.0),
    ("LON", "PNR", 87.9)
]

# -----------------------------
# MONTA O GRAFO
# -----------------------------
grafo = {cidade: [] for cidade in cidades}

for origem, destino, custo in arestas:
    grafo[origem].append((destino, custo))
    grafo[destino].append((origem, custo))


# -----------------------------
# DIJKSTRA
# -----------------------------
def dijkstra(origem, destino):
    fila = [(0, origem)]
    custos = {cidade: float("inf") for cidade in cidades}
    anteriores = {cidade: None for cidade in cidades}

    custos[origem] = 0

    while fila:
        custo_atual, cidade_atual = heapq.heappop(fila)

        if cidade_atual == destino:
            break

        for vizinho, custo_aresta in grafo[cidade_atual]:
            novo_custo = custo_atual + custo_aresta

            if novo_custo < custos[vizinho]:
                custos[vizinho] = novo_custo
                anteriores[vizinho] = cidade_atual
                heapq.heappush(fila, (novo_custo, vizinho))

    caminho = []
    atual = destino

    while atual is not None:
        caminho.append(atual)
        atual = anteriores[atual]

    caminho.reverse()

    return caminho, custos[destino]


# -----------------------------
# DESENHA A ROTA NA IMAGEM
# -----------------------------
def gerar_imagem_com_rota(caminho):
    imagem = Image.open(IMAGEM_GRAFO).convert("RGB")
    desenho = ImageDraw.Draw(imagem)

    # Linha da rota
    for i in range(len(caminho) - 1):
        cidade_atual = caminho[i]
        proxima_cidade = caminho[i + 1]

        x1, y1 = posicoes[cidade_atual]
        x2, y2 = posicoes[proxima_cidade]

        desenho.line((x1, y1, x2, y2), fill="red", width=8)

    # Marca origem e destino
    origem = caminho[0]
    destino = caminho[-1]

    for cidade, cor in [(origem, "green"), (destino, "blue")]:
        x, y = posicoes[cidade]

        desenho.ellipse(
            (x - 14, y - 14, x + 14, y + 14),
            fill=cor,
            outline="white",
            width=3
        )

    return imagem


# -----------------------------
# INTERFACE
# -----------------------------
class App:
    def __init__(self, janela):
        self.janela = janela
        self.janela.title("Dijkstra com imagem do grafo")
        self.janela.geometry("1150x900")

        topo = tk.Frame(janela)
        topo.pack(pady=10)

        tk.Label(topo, text="Origem:").grid(row=0, column=0, padx=5)

        self.origem = ttk.Combobox(
            topo,
            values=list(cidades.keys()),
            state="readonly",
            width=10
        )
        self.origem.grid(row=0, column=1, padx=5)
        self.origem.set("RSL")

        tk.Label(topo, text="Destino:").grid(row=0, column=2, padx=5)

        self.destino = ttk.Combobox(
            topo,
            values=list(cidades.keys()),
            state="readonly",
            width=10
        )
        self.destino.grid(row=0, column=3, padx=5)
        self.destino.set("PNR")

        tk.Button(
            topo,
            text="Calcular menor rota",
            command=self.calcular
        ).grid(row=0, column=4, padx=10)

        self.label_resultado = tk.Label(
            janela,
            text="Escolha a origem e o destino.",
            font=("Arial", 12)
        )
        self.label_resultado.pack(pady=5)

        self.canvas = tk.Canvas(janela, width=1024, height=768)
        self.canvas.pack()

        self.carregar_imagem_original()

    def carregar_imagem_original(self):
        imagem = Image.open(IMAGEM_GRAFO).convert("RGB")
        self.imagem_tk = ImageTk.PhotoImage(imagem)

        self.canvas.create_image(
            0,
            0,
            anchor="nw",
            image=self.imagem_tk
        )

    def calcular(self):
        origem = self.origem.get()
        destino = self.destino.get()

        if origem == destino:
            messagebox.showwarning(
                "Atenção",
                "A origem e o destino não podem ser iguais."
            )
            return

        caminho, custo_total = dijkstra(origem, destino)

        imagem_rota = gerar_imagem_com_rota(caminho)
        self.imagem_tk = ImageTk.PhotoImage(imagem_rota)

        self.canvas.create_image(
            0,
            0,
            anchor="nw",
            image=self.imagem_tk
        )

        texto_caminho = " -> ".join(caminho)

        self.label_resultado.config(
            text=f"Menor rota: {texto_caminho} | Custo total: {custo_total:.2f}"
        )


# -----------------------------
# EXECUTAR
# -----------------------------
janela = tk.Tk()
app = App(janela)
janela.mainloop()