# Dijkstra Alto Vale

Este projeto foi desenvolvido para demonstrar a aplicação do algoritmo de Dijkstra na região do Alto Vale do Itajaí.

A ideia principal é representar algumas cidades da região em forma de grafo, onde cada cidade é um vértice e cada ligação entre elas é uma aresta. A partir disso, o sistema calcula a menor rota entre uma cidade de origem e uma cidade de destino.

## Objetivo

Aplicar o algoritmo de Dijkstra para encontrar o caminho de menor custo entre municípios do Alto Vale do Itajaí, utilizando uma representação visual do grafo.

## Como funciona

O programa utiliza uma imagem do mapa como base e desenha a menor rota encontrada por cima dela.

O custo de cada ligação foi calculado considerando:

```text
Custo = distância × pavimentação × tráfego
