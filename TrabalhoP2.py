import matplotlib
matplotlib.use('TkAgg')
import networkx as nx
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import heapq
import time
import tkinter as tk
from tkinter import ttk

class PathfinderApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Pathfinders Solutions - Otimização de Rotas")
        
        self.grafo = self.criar_grafo()
        self.caminho = []
        self.distancia = 0
        
        self.criar_interface()
        self.atualizar_visualizacao()
    
    def criar_grafo(self):
        """Cria o grafo com pesos corretamente formatados"""
        G = nx.Graph()
        
        # Adicionando nós
        locais = ["Maricá (Centro)", "Itaipuaçu", "Barra de Maricá", 
                 "Niterói (Centro)", "Icaraí", "Ingá", "São Francisco", "Charitas"]
        G.add_nodes_from(locais)
        
        # Adicionando arestas com pesos de forma consistente
        rotas = [
            ("Maricá (Centro)", "Itaipuaçu", {"normal": 20, "rush": 30}),
            ("Maricá (Centro)", "Barra de Maricá", {"normal": 15, "rush": 20}),
            ("Itaipuaçu", "Niterói (Centro)", {"normal": 45, "rush": 65}),
            ("Barra de Maricá", "São Francisco", {"normal": 35, "rush": 45}),
            ("São Francisco", "Niterói (Centro)", {"normal": 20, "rush": 40}),
            ("Niterói (Centro)", "Icaraí", {"normal": 10, "rush": 30}),
            ("Niterói (Centro)", "Ingá", {"normal": 15, "rush": 25}),
            ("Icaraí", "Charitas", {"normal": 8, "rush": 10}),
            ("Ingá", "Charitas", {"normal": 12, "rush": 15}),
            ("Charitas", "São Francisco", {"normal": 20, "rush": 25})
        ]
        
        for origem, destino, pesos in rotas:
            G.add_edge(origem, destino, **pesos)
        
        return G
    
    def dijkstra(self, inicio, fim, horario='normal'):
        """Implementação corrigida do Dijkstra"""
        pesos = horario  # Usaremos isso para acessar o peso correto
        
        distancias = {no: float('inf') for no in self.grafo.nodes()}
        distancias[inicio] = 0
        predecessores = {no: None for no in self.grafo.nodes()}
        fila = [(0, inicio)]
        
        while fila:
            dist_atual, no_atual = heapq.heappop(fila)
            
            if dist_atual > distancias[no_atual]:
                continue
                
            for vizinho, dados in self.grafo[no_atual].items():
                # Acessando o peso corretamente
                peso = dados.get(pesos, float('inf'))
                distancia = dist_atual + peso
                
                if distancia < distancias[vizinho]:
                    distancias[vizinho] = distancia
                    predecessores[vizinho] = no_atual
                    heapq.heappush(fila, (distancia, vizinho))
        
        # Reconstrói o caminho
        caminho = []
        no_atual = fim
        while no_atual is not None:
            caminho.insert(0, no_atual)
            no_atual = predecessores.get(no_atual, None)
        
        if not caminho or caminho[0] != inicio:
            return None, None
        
        return distancias[fim], caminho
    
    def criar_interface(self):
        """Interface do usuário"""
        control_frame = ttk.Frame(self.root, padding="10")
        control_frame.grid(row=0, column=0, sticky="nsew")
        
        # Origem
        ttk.Label(control_frame, text="Origem:").grid(row=0, column=0)
        self.origem_var = tk.StringVar(value="Maricá (Centro)")
        origem_cb = ttk.Combobox(control_frame, textvariable=self.origem_var, 
                                values=list(self.grafo.nodes()))
        origem_cb.grid(row=0, column=1, pady=5)
        
        # Destino
        ttk.Label(control_frame, text="Destino:").grid(row=1, column=0)
        self.destino_var = tk.StringVar(value="Niterói (Centro)")
        destino_cb = ttk.Combobox(control_frame, textvariable=self.destino_var,
                                 values=list(self.grafo.nodes()))
        destino_cb.grid(row=1, column=1, pady=5)
        
        # Horário
        ttk.Label(control_frame, text="Horário:").grid(row=2, column=0)
        self.horario_var = tk.StringVar(value="normal")
        ttk.Radiobutton(control_frame, text="Normal", variable=self.horario_var, value="normal").grid(row=2, column=1, sticky="w")
        ttk.Radiobutton(control_frame, text="Rush", variable=self.horario_var, value="rush").grid(row=3, column=1, sticky="w")
        
        # Botão
        ttk.Button(control_frame, text="Calcular Rota", command=self.calcular_rota).grid(row=4, column=0, columnspan=2, pady=10)
        
        # Resultado
        self.resultado_var = tk.StringVar(value="Selecione origem e destino")
        ttk.Label(control_frame, textvariable=self.resultado_var, wraplength=300).grid(row=5, column=0, columnspan=2)
        
        # Visualização
        viz_frame = ttk.Frame(self.root, padding="10")
        viz_frame.grid(row=0, column=1, sticky="nsew")
        
        self.fig, self.ax = plt.subplots(figsize=(8, 6))
        self.canvas = FigureCanvasTkAgg(self.fig, master=viz_frame)
        self.canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)
        
        self.root.columnconfigure(1, weight=1)
        self.root.rowconfigure(0, weight=1)
    
    def calcular_rota(self):
        """Calcula a rota e exibe resultados"""
        inicio = self.origem_var.get()
        fim = self.destino_var.get()
        horario = self.horario_var.get()
        
        if inicio == fim:
            self.resultado_var.set("Origem e destino devem ser diferentes!")
            return
        
        start_time = time.time()
        self.distancia, self.caminho = self.dijkstra(inicio, fim, horario)
        tempo_exec = time.time() - start_time
        
        if self.caminho:
            resultado = (f"Rota mais curta: {' → '.join(self.caminho)}\n"
                       f"Tempo total: {self.distancia} minutos\n"
                       f"Cálculo em: {tempo_exec:.4f} segundos")
            self.resultado_var.set(resultado)
        else:
            self.resultado_var.set(f"Não há caminho entre {inicio} e {fim} no horário {horario}")
        
        self.atualizar_visualizacao()
    
    def atualizar_visualizacao(self):
        """Atualiza a visualização do grafo"""
        self.ax.clear()
        
        pos = nx.spring_layout(self.grafo, seed=42)
        
        # Desenha o grafo completo
        nx.draw_networkx_nodes(self.grafo, pos, ax=self.ax, node_size=500, node_color='lightblue')
        nx.draw_networkx_labels(self.grafo, pos, ax=self.ax)
        nx.draw_networkx_edges(self.grafo, pos, ax=self.ax, width=1, edge_color='gray')
        
        # Destaca o caminho se existir
        if self.caminho:
            arestas_caminho = [(self.caminho[i], self.caminho[i+1]) for i in range(len(self.caminho)-1)]
            nx.draw_networkx_edges(
                self.grafo, pos, edgelist=arestas_caminho, 
                ax=self.ax, edge_color='red', width=3
            )
            nx.draw_networkx_nodes(
                self.grafo, pos, nodelist=self.caminho,
                ax=self.ax, node_size=700, node_color='orange'
            )
        
        # Destaca origem e destino
        origem = self.origem_var.get()
        destino = self.destino_var.get()
        nx.draw_networkx_nodes(
            self.grafo, pos, nodelist=[origem],
            ax=self.ax, node_size=800, node_color='green'
        )
        nx.draw_networkx_nodes(
            self.grafo, pos, nodelist=[destino],
            ax=self.ax, node_size=800, node_color='blue'
        )
        
        self.ax.set_title("Mapa de Rotas - Maricá/Niterói")
        self.ax.axis('off')
        self.canvas.draw()

def main():
    root = tk.Tk()
    app = PathfinderApp(root)
    root.mainloop()

if __name__ == "__main__":
    main()