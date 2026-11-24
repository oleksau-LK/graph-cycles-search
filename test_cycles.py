import unittest
from itertools import combinations, permutations

from cycles import find_all_cycles


def cycle_edges(cycle):
    return frozenset(
        frozenset((cycle[index - 1], vertex))
        for index, vertex in enumerate(cycle)
    )


class FindAllCyclesTests(unittest.TestCase):
    def assert_cycles(self, graph, expected):
        original = {vertex: list(neighbors) for vertex, neighbors in graph.items()}
        actual = find_all_cycles(graph)
        for cycle in actual:
            self.assertGreaterEqual(len(cycle), 3)
            self.assertEqual(len(cycle), len(set(cycle)))
            for index, vertex in enumerate(cycle):
                self.assertIn(vertex, graph[cycle[index - 1]])
        self.assertCountEqual(
            [cycle_edges(cycle) for cycle in actual],
            [cycle_edges(cycle) for cycle in expected],
        )
        self.assertEqual(graph, original)

    def test_acyclic_graphs(self):
        for graph in (
            {},
            {0: []},
            {0: [], 1: []},
            {0: [1], 1: [0]},
            {0: [1], 1: [0, 2, 3], 2: [1], 3: [1]},
        ):
            with self.subTest(graph=graph):
                self.assert_cycles(graph, [])

    def test_single_cycle(self):
        self.assert_cycles(
            {0: [1, 2], 1: [0, 2], 2: [0, 1, 3], 3: [2]},
            [[0, 1, 2]],
        )

    def test_overlapping_cycles(self):
        self.assert_cycles(
            {0: [1, 2, 3], 1: [0, 2], 2: [0, 1, 3], 3: [0, 2]},
            [[0, 1, 2], [0, 2, 3], [0, 1, 2, 3]],
        )

    def test_disconnected_graph(self):
        self.assert_cycles(
            {
                0: [1, 2], 1: [0, 2], 2: [0, 1],
                3: [4, 5], 4: [3, 5], 5: [3, 4],
                6: [], 7: [8], 8: [7],
            },
            [[0, 1, 2], [3, 4, 5]],
        )

    def test_incomparable_vertices(self):
        self.assert_cycles(
            {None: ["a", 7], "a": [None, 7], 7: [None, "a"]},
            [[None, "a", 7]],
        )

    def test_repeated_calls(self):
        graph = {0: [1, 2], 1: [0, 2], 2: [0, 1]}
        self.assert_cycles(graph, [[0, 1, 2]])
        self.assert_cycles({}, [])
        self.assert_cycles(graph, [[0, 1, 2]])

    def test_all_graphs_on_five_vertices(self):
        vertices = range(5)
        edges = list(combinations(vertices, 2))
        candidates = []
        for length in range(3, 6):
            for subset in combinations(vertices, length):
                for tail in permutations(subset[1:]):
                    if tail[0] < tail[-1]:
                        cycle = (subset[0],) + tail
                        candidates.append((cycle, cycle_edges(cycle)))
        for mask in range(1 << len(edges)):
            graph = {vertex: [] for vertex in vertices}
            selected = set()
            for index, (left, right) in enumerate(edges):
                if mask & (1 << index):
                    graph[left].append(right)
                    graph[right].append(left)
                    selected.add(frozenset((left, right)))
            expected = [cycle for cycle, required in candidates if required <= selected]
            with self.subTest(mask=mask):
                self.assert_cycles(graph, expected)


if __name__ == "__main__":
    unittest.main()
