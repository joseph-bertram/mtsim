#!/usr/bin/env python3

import io
import sys
import time
import csv

from collections import defaultdict
from heapq import heappop, heappush
from typing import Iterator, Optional
from mtsim import *


Graph = dict[str, dict[str, int]]
Route = dict[str, str]

def read_csv(csv_file: str) -> Optional[tuple[str, str, Graph]]:
    graph = defaultdict(dict)
    vertices = []
    with open(csv_file, newline='') as graph_file:
        csvreader = csv.reader(graph_file, delimiter=' ')
        header = next(csvreader)
        origin, destination, edges = header[0].split(",")
        edges = int(edges)
        for row in csvreader:
            for i in range(0, edges):
                source, target, weight = row[0].split(",")
                graph[source][target] = int(weight)
                # graph[target][source] = int(weight)
    return origin, destination, graph
    

def dijkstra_sssp(args) -> tuple[int, Route]:
    origin, destination, graph = args
    frontier: list[tuple[int, str, str]] = [(0, origin, origin)] 
    visited: dict[str, str] = {}
    
    while frontier:
        vertex = []
        distance, target, source = heappop(frontier)
        for char in target:
            vertex.append(ord(char))
        mt_array_malloc(graph, level_1_hash, [vertex, len(vertex), 16])
        if target in visited:
            continue
        visited[target] = source
        if target == destination:
            break
        x = mt_array_read(graph, target, True)
        for neighbor, weight in x.items():
            heappush(frontier, (distance + weight, neighbor, target))
    del visited[origin]
    return (distance, visited)

def route(origin: str, destination: str, route: dict) -> Iterator[str]:
    # origin, destination, route = args
    path = []
    curr = destination
    while curr in route and curr != origin:
        path.append(curr)
        curr = route[curr]
    path.append(origin)
    return reversed(path)

def spawn(args):
    mt_spawn(dijkstra_sssp, args["dijkstra_sssp"])
    # mt_spawn(route, args["route"])
    mt_die()


def main(stream=sys.stdin) -> None:
    tic = time.perf_counter()
    origin, destination, graph = read_csv('graph2.csv')
    
    args = {"dijkstra_sssp": [origin, destination, graph], "route": [origin, destination, route]}

    distance, visited = mt_run(spawn, args, 0, 0, 16)

    # migration_matrix_constructor(16)
 
    # for key in graph:
        # vertex = []
        # for char in key:
            # vertex.append(ord(char))
        # mt_array_malloc(graph, level_1_hash, [vertex, len(vertex), 16])
        # edge = mt_array_read(graph, key, True)
        # print(edge)
    

    # distance, visited = dijkstra_sssp(origin, destination, graph)
    path = route(origin, destination, visited)
    toc = time.perf_counter()

    print(f'Distance: {distance}, Route: {"->".join(path)}')
    print(f'Time takes to SSSP graph: {toc - tic:0.8f}')

if __name__ == '__main__':
    main()
        
    
