# 🚜 Planejamento de Rotas em Fazenda Inteligente com Robôs

---

## 👥 Integrantes

| Nome | RA |
|------|----|
| Sydhiney Silva | G75EJI5 |
| Eduardo Theodoro | R153FJ3 |
| Ariane Veras | R197123 |
| Victor Donadi | G593IC1 |

---

## 📌 Objetivo

Implementar e comparar os algoritmos:

- A* (A-Star)
- IDA* (Iterative Deepening A*)
- RBFS (Recursive Best-First Search)

Considerando restrições de energia, obstáculos e diferentes geometrias de terreno.

---

## 🧠 Contexto do Problema

O cenário simula um drone agrícola que precisa navegar em uma fazenda representada por um grid 2D.

A fazenda possui duas regiões distintas:

- 🔲 Região Retangular  
- 🔵 Região Circular  

Cada região pode conter obstáculos e diferentes custos de movimentação.

O drone possui energia limitada (**E_max**) e cada movimento consome energia. Caminhos que excedem esse limite são descartados.

---

## 🗺️ Modelagem do Ambiente

- Representação: matriz (grid 2D)
- Tipos de terreno:
  - Células livres
  - Obstáculos
  - Custos variáveis
- Regiões:
  - Retangular: definida por (linhas x colunas)
  - Circular: definida por centro (cx, cy) e raio r

---

## ⚙️ Algoritmos Implementados

### 🔹 A* (A-Star)
- Busca informada com heurística  
- Utiliza a função:  
  ```
  f(n) = g(n) + h(n)
  ```
- Garante caminho ótimo (se heurística admissível)

---

### 🔹 IDA* (Iterative Deepening A*)
- Combina A* com busca em profundidade  
- Utiliza limites progressivos de custo  
- Menor consumo de memória  

---

### 🔹 RBFS (Recursive Best-First Search)
- Versão recursiva do Best-First  
- Mantém uso de memória reduzido  
- Pode revisitar nós  

---

## 📊 Métricas de Avaliação

Os algoritmos foram comparados com base em:

- ⏱ Tempo de execução (`time.perf_counter()`)
- 💾 Uso de memória (`tracemalloc` / `memory_profiler`)
- ⚡ Energia consumida
- 📈 Eficiência global

---

## 📉 Cálculo da Eficiência

A eficiência é dada por:

```
Score = α * Tempo_normalizado + β * Memoria_normalizada
```

Onde:
- α e β são pesos definidos no experimento  
- Valores menores indicam melhor desempenho  

---

## 📁 Estrutura do Projeto

```
📦 projeto
 ┣ 📜 pygame_vizual.py   # Visualização do ambiente e execução com interface gráfica
 ┣ 📜 mapa.py            # Definição do grid, regiões e obstáculos
 ┣ 📜 config.py          # Configurações do ambiente (energia, dimensões, etc)
 ┣ 📜 requirements.txt   # Dependências do projeto
 ┗ 📜 README.md
```

---

## 📌 Resultados Esperados

- A* tende a ser mais rápido e encontrar soluções ótimas  
- IDA* consome menos memória, porém pode ser mais lento  
- RBFS equilibra memória e desempenho, mas pode revisitar estados  

---

## 🧪 Discussão Técnica

### ✔️ A*
O A* apresenta excelente desempenho quando há uma boa heurística, sendo capaz de encontrar o caminho ótimo rapidamente. Porém, seu principal problema é o alto consumo de memória, pois armazena muitos nós na estrutura de dados.

---

### ✔️ IDA*
O IDA* reduz drasticamente o uso de memória ao utilizar busca em profundidade com limites incrementais. Entretanto, ele pode reexplorar vários estados, o que aumenta o tempo de execução.

---

### ✔️ RBFS
O RBFS busca equilibrar memória e desempenho, mantendo apenas o caminho atual em memória. Porém, pode revisitar estados e sofrer com custo adicional devido à recursividade.

---

### ⚖️ Comparação Geral

| Algoritmo | Tempo | Memória | Caminho Ótimo |
|----------|------|--------|--------------|
| A*       | ⭐⭐⭐⭐ | ⭐⭐     | Sim |
| IDA*     | ⭐⭐   | ⭐⭐⭐⭐   | Sim |
| RBFS     | ⭐⭐⭐  | ⭐⭐⭐    | Sim |

---

## 🧠 Conclusão Técnica

- Para cenários com memória suficiente → **A\*** é o mais eficiente  
- Para cenários com memória limitada → **IDA\*** é mais adequado  
- Para equilíbrio entre memória e desempenho → **RBFS**  

---
