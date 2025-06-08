# Pathfinder Solutions - Otimização de Rotas

Este projeto é uma aplicação gráfica interativa desenvolvida em Python, que utiliza algoritmos de caminho mínimo para encontrar a melhor rota entre bairros das regiões de **Maricá** e **Niterói**, no Rio de Janeiro. O algoritmo utilizado é o **Dijkstra**, e a aplicação permite visualizar os resultados em um grafo usando o `matplotlib` e `networkx`.

---

## 🧠 Funcionalidades

- Seleção de **origem** e **destino** entre 8 bairros.
- Escolha do **horário** (normal ou horário de pico "rush").
- Cálculo do caminho mais curto com base nos tempos de deslocamento.
- Visualização gráfica do grafo com destaque para a rota mais eficiente.
- Interface gráfica simples e intuitiva utilizando `tkinter`.

---

## 🛠️ Tecnologias e Bibliotecas

- Python 3.x
- [NetworkX](https://networkx.org/) – modelagem de grafos
- [Matplotlib](https://matplotlib.org/) – visualização do grafo
- [Tkinter](https://docs.python.org/3/library/tkinter.html) – interface gráfica
- [Heapq](https://docs.python.org/3/library/heapq.html) – fila de prioridade para o algoritmo Dijkstra

---

## ⚙️ Como executar o projeto

1. **Clone o repositório**:

```bash
git clone https://github.com/Theuss21/trabalho-eda-p2.git
cd trabalho-eda-p2

Instale as dependências:

pip install matplotlib networkx

Execute o programa:

python TrabalhoP2.py

📌 Estrutura do Grafo
Nós: representam bairros como "Maricá (Centro)", "Itaipuaçu", "Charitas", etc.

Arestas: representam conexões entre os bairros com tempo estimado de deslocamento.

Dois modos de tráfego:

normal: tempo em minutos padrão.

rush: tempo em minutos durante horários de pico.

💡 Exemplo de uso
Selecione Maricá (Centro) como origem.

Escolha Niterói (Centro) como destino.

Marque o horário: Normal ou Rush.

Clique em Calcular Rota.

Veja a rota mais curta destacada em vermelho no grafo e o tempo total estimado.
