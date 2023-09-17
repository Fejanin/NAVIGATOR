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


class Vertex:
    def __init__(self):
        self._links = [] # - список связей с другими вершинами графа (список объектов класса Link).

    @property
    def link(self):
        return self._links

    def __str__(self):
        return str(id(self))

class Link:
    def __init__(self, v1, v2):
        self._v1 = v1
        self._v2 = v2
        self._dist = 1

    @property
    def v1(self):
        return self._v1

    @property
    def v2(self):
        return self._v2

    @property
    def dist(self):
        return self._dist

    @dist.setter
    def dist(self, value):
        self._dist = value

class LinkedGraph:
    def __init__(self):
        self._links = [] # - список из всех связей графа (из объектов класса Link)
        self._vertex = [] # - список из всех вершин графа (из объектов класса Vertex)

    def add_vertex(self, v):
        # - для добавления новой вершины v в список _vertex (если она там отсутствует)
        if not self.is_in_vertex_lst(v):
            self._vertex.append(v)

    def add_link(self, link):
        #  - для добавления новой связи link в список _links (если объект link с указанными вершинами в списке отсутствует)
        # В методе add_link() при добавлении новой связи следует автоматически добавлять вершины этой связи в список _vertex, если они там отсутствуют
        # Проверку наличия связи в списке _links следует определять по вершинам этой связи. Например, если в списке имеется объект:
        # _links = [Link(v1, v2)]
        # то добавлять в него новые объекты Link(v2, v1) или Link(v1, v2) нельзя (обратите внимание у всех трех
        # объектов будут разные id, т.е. по id определять вхождение в список нельзя)
        if not self.is_in_links_lst(link):
            self._links.append(link)
            for v in (link.v1, link.v2):
                self.add_vertex(v)

    def find_path(self, start_v, stop_v):
        #  - для поиска кратчайшего маршрута из вершины start_v в вершину stop_v
        # Метод find_path() должен возвращать список из вершин кратчайшего маршрута и список из связей этого же маршрута в виде кортежа:
        result_deicstra_func = self.export_data_for_deicstra_func(start_v, stop_v)
        result = self.translate_result_deicstra_func(result_deicstra_func)
        # >>> ([вершины кратчайшего пути], [связи между вершинами])
        return result

    def is_in_vertex_lst(self, v):
        return str(v) in [str(i) for i in self._vertex]

    def is_in_links_lst(self, link):
        return any([{link.v1, link.v2} == {i.v1, i.v2} for i in self._links])

    def export_data_for_deicstra_func(self, start_v, stop_v):
        return deicstra(start_v, stop_v, self._vertex, {(i.v1, i.v2): i._dist for i in self._links})

    def translate_result_deicstra_func(self, result_deicstra_func):
        vertexes = result_deicstra_func[0]
        pair_of_vertexes = [(vertexes[i - 1], vertexes[i]) for i in range(1, len(vertexes))]
        return (vertexes, [j for i in pair_of_vertexes for j in self._links if set(i) == {j.v1, j.v2}]) # TODO 
    

class Station(Vertex):
    #  - для описания станций метро
    # Объекты класса Station должны создаваться командой:
    # >>> st = Station(name)
    # где name - название станции (строка). В каждом объекте класса Station должен дополнительно формироваться локальный атрибут:
    # name - название станции метро.
    # В самом классе Station переопределите магические методы __str__() и __repr__(), чтобы они возвращали название станции метро (локальный атрибут name).
    def __init__(self, name):
        super().__init__()
        self.name = name

    def __str__(self):
        return self.name

    def __repr__(self):
        return self.name

class LinkMetro(Link):
    # - для описания связей между станциями метро
    # Объекты второго класса LinkMetro должны создаваться командой:
    # >>> link = LinkMetro(v1, v2, dist)
    # где v1, v2 - вершины (станции метро); dist - расстояние между станциями (любое положительное число).
    # (Также не забывайте в инициализаторе этого дочернего класса вызывать инициализатор базового класса).
    def __init__(self, v1, v2, dist):
        super().__init__(v1, v2)
        self._dist = dist


#=======================================================================================================================================================================

# Test. func deicstra
print('\nTest. func deicstra')
vertexes = [1, 2, 3, 4, 5, 6]
edges = {(1, 2): 7, (1, 3): 9, (1, 6): 14, (2, 3): 10, (2, 4): 15, (3, 6): 2, (3, 4): 11, (4, 5): 6, (5, 6): 9}

res = deicstra(1, 6, vertexes, edges)
print(res)
print('*' * 80)

# Test. class Vertex
print('Test. class Vertex')
v1 = Vertex()
print(v1)
print(v1.link)
v2 = Vertex()
print(v2)
print(v2.link)
print('*' * 80)

# Test. class Link
print('\nTest. class Link')
ln1 = Link(v1, v2)
print(ln1)
print(ln1.v1)
print(ln1.v2)
print(ln1.dist)
ln1.dist = 2
print(ln1.dist)
print('*' * 80)

# Test. class LinkedGraph
print('\nTest. class LinkedGraph')
LnGr = LinkedGraph()
print(LnGr)
print(LnGr._links, f'\nДлина списка _links - {len(LnGr._links)}')
print(LnGr._vertex, f'\nДлина списка _vertex - {len(LnGr._vertex)}')
print('-add_vertex-')
LnGr.add_vertex(v1)
LnGr.add_vertex(v2)
LnGr.add_vertex(v1) # не должна добавиться
print('-add_link-')
LnGr.add_link(ln1)
ln2 = Link(v2, v1)
LnGr.add_link(ln2) # не должна добавиться
print(LnGr._links, f'\nДлина списка _links - {len(LnGr._links)}')
print(LnGr._vertex, f'\nДлина списка _vertex - {len(LnGr._vertex)}')
print('*' * 80)
# Test. class LinkedGraph. method find_path
print('\nTest. class LinkedGraph. method find_path')
res = LnGr.find_path(v1, v2)
print(res)
print('*' * 80)


print('\nTest. от Балакирева 1')
map_graph = LinkedGraph()

v1 = Vertex()
v2 = Vertex()
v3 = Vertex()
v4 = Vertex()
v5 = Vertex()
v6 = Vertex()
v7 = Vertex()

map_graph.add_link(Link(v1, v2))
map_graph.add_link(Link(v2, v3))
map_graph.add_link(Link(v1, v3))

map_graph.add_link(Link(v4, v5))
map_graph.add_link(Link(v6, v7))

map_graph.add_link(Link(v2, v7))
map_graph.add_link(Link(v3, v4))
map_graph.add_link(Link(v5, v6))

print(len(map_graph._links))   # 8 связей
print(len(map_graph._vertex))  # 7 вершин
path = map_graph.find_path(v1, v6)
print(path)
print('*' * 80)


print('\nTest. от Балакирева 2')
map_metro = LinkedGraph()
v1 = Station("Сретенский бульвар")
v2 = Station("Тургеневская")
v3 = Station("Чистые пруды")
v4 = Station("Лубянка")
v5 = Station("Кузнецкий мост")
v6 = Station("Китай-город 1")
v7 = Station("Китай-город 2")

map_metro.add_link(LinkMetro(v1, v2, 1))
map_metro.add_link(LinkMetro(v2, v3, 1))
map_metro.add_link(LinkMetro(v1, v3, 1))

map_metro.add_link(LinkMetro(v4, v5, 1))
map_metro.add_link(LinkMetro(v6, v7, 1))

map_metro.add_link(LinkMetro(v2, v7, 5))
map_metro.add_link(LinkMetro(v3, v4, 3))
map_metro.add_link(LinkMetro(v5, v6, 3))

print(len(map_metro._links))
print(len(map_metro._vertex))
path = map_metro.find_path(v1, v6)  # от сретенского бульвара до китай-город 1
print(path[0])    # [Сретенский бульвар, Тургеневская, Китай-город 2, Китай-город 1]
print(sum([x.dist for x in path[1]]))  # 7

print('*' * 80)


