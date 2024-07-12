#!/usr/bin/env python3

import io
import sys
import time
import csv

from collections import defaultdict
from heapq import heappop, heappush
from typing import Iterator, Optional


Graph = dict[str, dict[str, int]]
Route = dict[str, str]

def read_csv(csv_file: str) -> Optional[tuple[str, str, Graph]]:
    graph = defaultdict(dict)
    with open(csv_file, newline='') as graph_file:
        csvreader = csv.reader(graph_file, delimiter=' ')
        header = next(csvreader)
        origin, destination, edges = header[0].split(",")
        edges = int(edges)
        for row in csvreader:
            for i in range(0, edges):
                source, target, weight = row[0].split(",")
                graph[source][target] = int(weight)
        return origin, destination, graph

def random_graph_gen(n: int) -> tuple[Graph, str, str]:
    G = nx.Graph()
    randEdges = rand.randint(0, (n * (n - 1)) // 2)

    for _ in range(randEdges):
        addEdge = False
        while not addEdge:
            randx = rand.randint(0, n - 1)
            randy = rand.randint(0, n - 1)
            if randx != randy:
                G.add_edge(randx, randy, weight=rand.randint(1, 10))
                addEdge = True

    graph = defaultdict(dict)
    for u, v, data in G.edges(data=True):
        graph[str(u)][str(v)] = data['weight']
        graph[str(v)][str(u)] = data['weight']

    return graph, str(0), str(n - 1)

def dijkstra_sssp(origin: str, destination: str, graph: Graph) -> tuple[int, Route]:
    frontier: list[tuple[int, str, str]] = [(0, origin, origin)] 
    visited: dict[str, str] = {}
    while frontier:
        distance, target, source = heappop(frontier)
        if target in visited:
            continue
        visited[target] = source
        if target == destination:
            break
        for neighbor, weight in graph[target].items():
            heappush(frontier, (distance + weight, neighbor, target))
    del visited[origin]
    return distance, visited

def route(origin: str, destination: str, route: Route) -> Iterator[str]:
    path = []
    curr = destination
    while curr != origin:
        path.append(curr)
        curr = route[curr]
    path.append(origin)
    return reversed(path)


# def main(stream=sys.stdin) -> None:
tic = time.perf_counter()
origin, destination, graph = read_csv('graph.csv')
distance, visited = dijkstra_sssp(origin, destination, graph)
path = route(origin, destination, visited)
toc = time.perf_counter()
print(f'{graph}')
print(f'Distance: {distance}, Route: {"->".join(path)}')
print(f'Time takes to SSSP graph: {toc - tic:0.8f}')
        
    
