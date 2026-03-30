"""
Humanitarian Logistics Optimizer

Optimizes supply chain routes, schedules deliveries, and computes efficiency 
for relief deployment.
"""

import heapq

def optimize_routes(nodes, edges, start_node, target_nodes):
    """
    Finds the shortest paths from a warehouse to affected regions using Dijkstra's algorithm.
    nodes: list of node names
    edges: dict of {node1: {node2: weight, node3: weight}}
    start_node: str (e.g., Warehouse)
    target_nodes: list of str (e.g., Affected Regions)
    """
    
    # Initialize distances and previous nodes tracker
    distances = {node: float('inf') for node in nodes}
    distances[start_node] = 0
    previous_nodes = {node: None for node in nodes}
    
    # Priority queue to hold (distance, node)
    pq = [(0, start_node)]
    
    while pq:
        current_distance, current_node = heapq.heappop(pq)
        
        # Nodes can get added to priority queue multiple times, skip obsolete entries
        if current_distance > distances[current_node]:
            continue
            
        # Check neighbors
        if current_node in edges:
            for neighbor, weight in edges[current_node].items():
                distance = current_distance + weight
                
                # If shorter path found
                if distance < distances[neighbor]:
                    distances[neighbor] = distance
                    previous_nodes[neighbor] = current_node
                    heapq.heappush(pq, (distance, neighbor))
                    
    # Reconstruct paths for target nodes
    optimized_plans = {}
    for target in target_nodes:
        path = []
        current = target
        while current is not None:
            path.append(current)
            current = previous_nodes[current]
        
        path.reverse()
        if path[0] == start_node:
            optimized_plans[target] = {
                'route': path,
                'total_distance': distances[target]
            }
        else:
             optimized_plans[target] = {
                'route': [],
                'total_distance': float('inf'),
                'note': 'Unreachable'
            }
            
    return optimized_plans

