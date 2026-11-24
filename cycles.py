def find_all_cycles(graph):
    order = {vertex: index for index, vertex in enumerate(graph)}
    cycles = []

    def dfs(vertex):
        for neighbor in graph[vertex]:
            if neighbor == start:
                if len(path) >= 3 and order[path[1]] < order[path[-1]]:
                    cycles.append(path.copy())
            elif order[neighbor] > order[start] and neighbor not in visited:
                visited.add(neighbor)
                path.append(neighbor)
                dfs(neighbor)
                path.pop()
                visited.remove(neighbor)

    for start in graph:
        path = [start]
        visited = {start}
        dfs(start)

    return cycles
