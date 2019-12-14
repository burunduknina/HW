"""
E - dict(<V> : [<V>, <V>, ...])
Ключ - строка, идентифицирующая вершину графа
значение - список вершин, достижимых из данной
Сделать так, чтобы по графу можно было итерироваться(обходом в ширину)
"""
import collections


class Graph:
    def __init__(self, E):
        if isinstance(E, dict):
            self.E = E
        else:
            raise TypeError('You gave a not dictionary object')

    def __iter__(self):
        marked = set()
        for key, value in self.E.items():
            if key not in marked:
                marked.add(key)
                yield key
                next_level = collections.deque(value)
                while next_level:
                    vert = next_level.popleft()
                    if vert not in marked:
                        marked.add(vert)
                        next_level.extend(self.E.get(vert, []))
                        yield vert


E = {'A': ['B', 'C', 'D'], 'B': ['C'], 'C': [], 'D': ['A']}
graph = Graph(E)

for vertex in graph:
    print(vertex)
