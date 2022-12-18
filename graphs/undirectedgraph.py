from typing import Generic, TypeVar
from typing import List, Tuple, Set, Dict
from collections import defaultdict

T = TypeVar('T')


class Node(Generic[T]):
    def __init__(self, _id: str, _neighbours: Set[str] = None):
        self.id = _id
        if _neighbours is None:
            self.neighbours = set([])
        else:
            self.neighbours = _neighbours

    def __repr__(self):
        return f'Node(id={self.id}, neighbours={self.neighbours})'

    def __str__(self):
        return self.__repr__()

    def __hash__(self):
        return hash(self.id)

    def __eq__(self, other):
        if other is None:
            return False
        return self.id == other.id


class Edge:
    def __init__(self, _v1: str, _v2: str):
        self.v1 = _v1
        self.v2 = _v2


class UndirectedGraph:
    def __init__(self, _graph: Dict[Node, Node] = None):
        if _graph is None:
            self.graph = {}
        else:
            self.graph = _graph

    @staticmethod
    def _check_graph(graph: Dict[Node, Node]):
        for k, v in graph.items():
            if k != v and k.neighbours != v.neighbours:
                raise GraphValidationError(f'key: {k} and value: {v} are not equals.')

    def add_edge(self, src: str, dst: str):
        if Node(src) not in self.graph and Node(dst) not in self.graph:
            node_src = Node(src, {dst})
            node_dst = Node(src)
            self.graph[node_src] = node_src
            self.graph[node_dst] = node_dst
        elif Node(src) not in self.graph and Node(dst) in self.graph:
            node_src = Node(src, {dst})
            self.graph[node_src] = node_src
        elif Node(src) in self.graph and Node(dst) not in self.graph:
            self.graph[Node(src)].neighbours.add(dst)
            node_dst = Node(dst)
            self.graph[node_dst] = node_dst

    def get_vertices(self) -> List[str]:
        result = []
        for k in self.graph:
            result.append(k.id)
        return result

    def edges(self) -> List[Tuple[str, str]]:
        edges = set([])
        for node in self.graph:
            for v1 in node.neighbours:
                if (node.id, v1) not in edges and (v1, node.id) not in edges:
                    edges.add((node.id, v1))

        return list(edges)


class GraphValidationError(Exception):
    def __init__(self, message: str, errors=None):
        super().__init__(message)
        self.errors = errors
