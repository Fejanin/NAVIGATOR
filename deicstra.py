from copy import copy


def deicstra(start_vertex: int, end_vertex: int, vertexes: list, edges: dict) -> list:
    paths = {i: None for i in vertexes} # 1: 0, 2: [[1, 2], 7], 3: [[1, 4, 3], 12]
    paths[start_vertex] = [[start_vertex], 0]
    old_vertexes = []
    while True:
        # создать список открытых верщин
        current_vertexes = [i for i in paths.keys() if paths[i] and not i in old_vertexes]
        if not current_vertexes:
            break        
        # найти среди них вершину с минимальным значением
        min_vertex = min([i for i in current_vertexes], key=lambda x: paths[x][1])
        # создать список ребер от данной вершины к "доступным" вершинам
        edges_of_min_vertex = [(i, edges[i])  for i in edges if min_vertex in i]
        # пройти по ним в цикле, сохраняя в них результат и новый путь, если он меньше текущего значения
        for i, value in edges_of_min_vertex:
            if i[i.index(min_vertex) - 1] in old_vertexes:
                continue
            if paths[i[i.index(min_vertex) - 1]] is None:
                paths[i[i.index(min_vertex) - 1]] = [paths[min_vertex][0] + [i[i.index(min_vertex) - 1]], paths[min_vertex][1] + value]
            else:
                if paths[i[i.index(min_vertex) - 1]][1] > paths[min_vertex][1] + value:
                    paths[i[i.index(min_vertex) - 1]] = [paths[min_vertex][0] + [i[i.index(min_vertex) - 1]], paths[min_vertex][1] + value]
        # "спрятать" отработанную вершину в old_vertexes
        old_vertexes.append(min_vertex)
    return paths[end_vertex]


if __name__ == "__main__":
    # список вершин
    vertexes = [1, 2, 3, 4, 5, 6]
    # словарь ребер, где ключ - это соедененные вершины, а значения - расстояние
    edges = {(1, 2): 7, (1, 3): 9, (1, 6): 14, (2, 3): 10, (2, 4): 15, (3, 6): 2, (3, 4): 11, (4, 5): 6, (5, 6): 9}

    res = deicstra(1, 5, vertexes, edges)
    print(res)
