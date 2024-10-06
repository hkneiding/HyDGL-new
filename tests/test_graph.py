import unittest
import torch
import networkx as nx
from torch_geometric.data import Data
from parameterized import parameterized

from HyDGL.node import Node
from HyDGL.edge import Edge
from HyDGL.graph import Graph
from tests.utils import Utils


class TestGraph(unittest.TestCase):

    @parameterized.expand([

        [
            Graph([Node(features=[0], label='A', position=[0,0,0]),
                   Node(features=[0], label='A', position=[0.5,0.5,0.5]), 
                   Node(features=[0], label='B', position=[1,1,1]),
                   Node(features=[0], label='B', position=[1.5,1.5,1.5]), 
                   Node(features=[0], label='C', position=[2e1,2e-1,0])],
                  [Edge([0, 1], features=[0]),
                   Edge([0, 2], features=[0]),
                   Edge([0, 3], features=[0]),
                   Edge([3, 2], features=[0]),
                   Edge([2, 4], features=[0])], meta_data={'id': 'TestGraph'}),
            '5\nid: TestGraph\nA 0.0000 0.0000 0.0000\nA 0.5000 0.5000 0.5000\nB 1.0000 1.0000 1.0000\nB 1.5000 1.5000 1.5000\nC 20.0000 0.2000 0.0000\n'
        ],

    ])
    def test_get_xyz_data_with_incomplete_data(self, graph, expected):

        self.assertEqual(graph.get_xyz_data(), expected)

    @parameterized.expand([

        [
            Graph([Node(features=[0], label='A', position=[0,0,0]),
                   Node(features=[0], label='A'), 
                   Node(features=[0], label='B', position=[1,1,1]),
                   Node(features=[0], label='B', position=[1.5,1.5,1.5]), 
                   Node(features=[0], label='C', position=[2,2,2])],
                  [Edge([0, 1], features=[0]),
                   Edge([0, 2], features=[0]),
                   Edge([0, 3], features=[0]),
                   Edge([3, 2], features=[0]),
                   Edge([2, 4], features=[0])], meta_data={'id': 'TestGraph'}),
            ValueError
        ],

        [
            Graph([Node(features=[0], label='A', position=[0,0,0]),
                   Node(features=[0], position=[0.5,0.5,0.5]), 
                   Node(features=[0], label='B', position=[1,1,1]),
                   Node(features=[0], label='B', position=[1.5,1.5,1.5]), 
                   Node(features=[0], label='C', position=[2,2,2])],
                  [Edge([0, 1], features=[0]),
                   Edge([0, 2], features=[0]),
                   Edge([0, 3], features=[0]),
                   Edge([3, 2], features=[0]),
                   Edge([2, 4], features=[0])], meta_data={'id': 'TestGraph'}),
            ValueError
        ],

    ])
    def test_get_xyz_data(self, graph, expected_exception):

        self.assertRaises(expected_exception, graph.get_xyz_data)

    @parameterized.expand([

        [
            Graph([Node(features=[0]), Node(features=[0]), Node(features=[0]), Node(features=[0]), Node(features=[0])],
                  [Edge([0, 1], features=[0]), Edge([0, 2], features=[0]), Edge([0, 3], features=[0]), Edge([3, 2], features=[0]), Edge([2, 4], features=[0])], meta_data={'id': 'TestGraph'}),
            True
        ],

        [
            Graph([Node(features=[0]), Node(features=[0]), Node(features=[0]), Node(features=[0]), Node(features=[0])],
                  [Edge([0, 1], features=[0]), Edge([0, 2], features=[0]), Edge([0, 3], features=[0]), Edge([3, 2], features=[0])], meta_data={'id': 'TestGraph'}),
            False
        ],

    ])
    def test_is_connected(self, graph, expected):

        self.assertEqual(graph.is_connected(), expected)

    @parameterized.expand([

        [
            Graph([Node(features=[0]), Node(features=[1]), Node(features=[2])],
                  [Edge([0, 1], features=[3])], meta_data={'id': 'TestGraph'}),
            [
                Graph([Node(features=[0]), Node(features=[1])], [Edge([0, 1], features=[3])], meta_data={'id': 'TestGraph-subgraph-0'}),
                Graph([Node(features=[2])], edges=[], meta_data={'id': 'TestGraph-subgraph-1'}),
            ]
        ],

    ])
    def test_get_disjoint_sub_graphs(self, graph, expected):

        result = graph.get_disjoint_sub_graphs()
        Utils.assert_are_almost_equal(result, expected)

    @parameterized.expand([

        [
            Graph([Node(features=[0]), Node(features=[0]), Node(features=[0]), Node(features=[0]), Node(features=[0])],
                  [Edge([0, 1], features=[0]), Edge([0, 2], features=[0]), Edge([0, 3], features=[0]), Edge([3, 2], features=[0]), Edge([2, 4], features=[0])], meta_data={'id': 'TestGraph'}),
            [[0, 1, 2, 3, 4]]
        ],

        [
            Graph([Node(features=[0]), Node(features=[0]), Node(features=[0]), Node(features=[0]), Node(features=[0])],
                  [Edge([0, 1], features=[0]), Edge([0, 2], features=[0]), Edge([0, 3], features=[0]), Edge([3, 2], features=[0])], meta_data={'id': 'TestGraph'}),
            [[0, 1, 2, 3], [4]]
        ],

    ])
    def test_get_disjoint_sub_graphs_node_indices(self, graph, expected):

        self.assertEqual(graph.get_disjoint_sub_graphs_node_indices(), expected)

    @parameterized.expand([

        [
            Graph([Node(features=[0]), Node(features=[0]), Node(features=[0]), Node(features=[0]), Node(features=[0])],
                  [Edge([0, 1], features=[0]), Edge([0, 2], features=[0]), Edge([0, 3], features=[0]), Edge([3, 2], features=[0]), Edge([2, 4], features=[0])]),
            0,
            [1, 2, 3]
        ],

        [
            Graph([Node(features=[0]), Node(features=[0]), Node(features=[0]), Node(features=[0]), Node(features=[0])],
                  [Edge([0, 1], features=[0]), Edge([0, 2], features=[0]), Edge([0, 3], features=[0]), Edge([3, 2], features=[0]), Edge([2, 4], features=[0])]),
            4,
            [2]
        ],

        [
            Graph([Node(features=[0]), Node(features=[0]), Node(features=[0]), Node(features=[0]), Node(features=[0])],
                  [Edge([0, 1], features=[0]), Edge([0, 2], features=[0]), Edge([0, 3], features=[0]), Edge([3, 2], features=[0])]),
            4,
            []
        ],

    ])
    def test_get_adjacent_nodes_with_valid_input(self, graph, node, expected):

        self.assertEqual(graph.get_adjacent_nodes(node), expected)

    @parameterized.expand([

        [
            Graph([Node(features=[0]), Node(features=[0]), Node(features=[0]), Node(features=[0]), Node(features=[0])],
                  [Edge([0, 1], features=[0]), Edge([0, 2], features=[0]), Edge([0, 3], features=[0]), Edge([3, 2], features=[0])]),
            -1
        ],

        [
            Graph([Node(features=[0]), Node(features=[0]), Node(features=[0]), Node(features=[0]), Node(features=[0])],
                  [Edge([0, 1], features=[0]), Edge([0, 2], features=[0]), Edge([0, 3], features=[0]), Edge([3, 2], features=[0])]),
            7
        ]
    ])
    def test_get_adjacent_nodes_with_invalid_input(self, graph, node):

        self.assertRaises(ValueError, graph.get_adjacent_nodes, node)

    @parameterized.expand([

        [
            Graph([Node(features=[0]), Node(features=[0]), Node(features=[0]), Node(features=[0]), Node(features=[0])],
                  [Edge([0, 1], features=[0], is_directed=True), Edge([0, 2], features=[0], is_directed=True), Edge([0, 3], features=[0], is_directed=True), Edge([3, 2], features=[0], is_directed=True), Edge([2, 4], features=[0], is_directed=True)]),
            0,
            []
        ],

        [
            Graph([Node(features=[0]), Node(features=[0]), Node(features=[0]), Node(features=[0]), Node(features=[0])],
                  [Edge([0, 1], features=[0], is_directed=True), Edge([0, 2], features=[0], is_directed=True), Edge([0, 3], features=[0], is_directed=True), Edge([3, 2], features=[0], is_directed=True), Edge([2, 4], features=[0], is_directed=True)]),
            4,
            [2]
        ],

        [
            Graph([Node(features=[0]), Node(features=[0]), Node(features=[0]), Node(features=[0]), Node(features=[0])],
                  [Edge([0, 1], features=[0], is_directed=True), Edge([0, 2], features=[0], is_directed=True), Edge([0, 3], features=[0], is_directed=True), Edge([3, 2], features=[0], is_directed=True), Edge([2, 4], features=[0], is_directed=True)]),
            2,
            [0, 3]
        ],

    ])
    def test_get_incoming_adjacent_nodes_with_valid_input(self, graph, node, expected):

        self.assertEqual(graph.get_incoming_adjacent_nodes(node), expected)

    @parameterized.expand([

        [
            Graph([Node(features=[0]), Node(features=[0]), Node(features=[0]), Node(features=[0]), Node(features=[0])],
                  [Edge([0, 1], features=[0], is_directed=True), Edge([0, 2], features=[0], is_directed=True), Edge([0, 3], features=[0], is_directed=True), Edge([3, 2], features=[0], is_directed=True), Edge([2, 4], features=[0], is_directed=True)]),
            0,
            [1, 2, 3]
        ],

        [
            Graph([Node(features=[0]), Node(features=[0]), Node(features=[0]), Node(features=[0]), Node(features=[0])],
                  [Edge([0, 1], features=[0], is_directed=True), Edge([0, 2], features=[0], is_directed=True), Edge([0, 3], features=[0], is_directed=True), Edge([3, 2], features=[0], is_directed=True), Edge([2, 4], features=[0], is_directed=True)]),
            4,
            []
        ],

        [
            Graph([Node(features=[0]), Node(features=[0]), Node(features=[0]), Node(features=[0]), Node(features=[0])],
                  [Edge([0, 1], features=[0], is_directed=True), Edge([0, 2], features=[0], is_directed=True), Edge([0, 3], features=[0], is_directed=True), Edge([3, 2], features=[0], is_directed=True), Edge([2, 4], features=[0], is_directed=True)]),
            2,
            [4]
        ],

    ])
    def test_get_outgoing_adjacent_nodes_with_valid_input(self, graph: Graph, node, expected):

        self.assertEqual(graph.get_outgoing_adjacent_nodes(node), expected)

    @parameterized.expand([

        [
            Graph([Node(features=[0]), Node(features=[0]), Node(features=[0]), Node(features=[0]), Node(features=[0])],
                  [Edge([0, 1], features=[0], is_directed=True), Edge([0, 2], features=[0], is_directed=False), Edge([0, 3], features=[0], is_directed=True), Edge([3, 2], features=[0], is_directed=True), Edge([2, 4], features=[0], is_directed=False)]),
            [
                [0, 0, 1, 0, 0],
                [1, 0, 0, 0, 0],
                [1, 0, 0, 1, 1],
                [1, 0, 0, 0, 0],
                [0, 0, 1, 0, 0]
            ]
        ],

        [
            Graph([Node(features=[0]), Node(features=[0]), Node(features=[0]), Node(features=[0]), Node(features=[0])],
                  [Edge([0, 1], features=[0], is_directed=False), Edge([0, 2], features=[0], is_directed=True), Edge([0, 3], features=[0], is_directed=False), Edge([3, 2], features=[0], is_directed=True), Edge([2, 4], features=[0], is_directed=False)]),
            [
                [0, 1, 0, 1, 0],
                [1, 0, 0, 0, 0],
                [1, 0, 0, 1, 1],
                [1, 0, 0, 0, 0],
                [0, 0, 1, 0, 0]
            ]
        ],

    ])
    def test_get_adjacency_matrix(self, graph: Graph, expected):

        self.assertEqual(graph.get_adjacency_matrix(), expected)

    @parameterized.expand([

        [
            Graph([Node(features=[0]), Node(features=[0]), Node(features=[0]), Node(features=[0]), Node(features=[0])],
                  [Edge([0, 1], features=[0], is_directed=True), Edge([0, 2], features=[0], is_directed=False), Edge([0, 3], features=[0], is_directed=True), Edge([3, 2], features=[0], is_directed=True), Edge([2, 4], features=[0], is_directed=False)]),
            [1.61803399+0j, 0.0+0j, 0.0+0j, -0.61803399+0j, -1.0+0j]
        ],

        [
            Graph([Node(features=[0]), Node(features=[0]), Node(features=[0]), Node(features=[0]), Node(features=[0])],
                  [Edge([0, 1], features=[0], is_directed=False), Edge([0, 2], features=[0], is_directed=True), Edge([0, 3], features=[0], is_directed=False), Edge([3, 2], features=[0], is_directed=True), Edge([2, 4], features=[0], is_directed=False)]),
            [1.41421356+0j, 1.0+0j, 0.0+0j, -1.0+0j, -1.41421356+0j]
        ],

    ])
    def test_get_spectrum(self, graph: Graph, expected):

        Utils.assert_are_almost_equal(graph.get_spectrum(), expected, places=7)

    @parameterized.expand([

        [
            Graph(
                [Node(features=[0]), Node(features=[1]), Node(features=[3]), Node(features=[-2]), Node(features=[0])],
                [Edge([0, 1], features=[-2]), Edge([0, 2], features=[3]), Edge([0, 3], features=[4]), Edge([2, 3], features=[1]), Edge([2, 4], features=[10])],
                targets={'a': 12.34}
            ),
            {},
            Data(
                x=torch.tensor([[0], [1], [3], [-2], [0]], dtype=torch.float),
                edge_index=torch.tensor([[0, 1, 0, 2, 0, 3, 2, 3, 2, 4],
                                         [1, 0, 2, 0, 3, 0, 3, 2, 4, 2]], dtype=torch.long),
                edge_attr=torch.tensor([[-2.], [-2.], [3.], [3.], [4.], [4.], [1.], [1.], [10.], [10.]], dtype=torch.float),
                y=torch.tensor([12.34], dtype=torch.float),
                num_nodes=5,
                graph_attr=torch.tensor([], dtype=torch.float),
                id=None
            )
        ],

        [
            Graph(
                [Node(features=[0]), Node(features=[1]), Node(features=[3]), Node(features=[-2]), Node(features=[0])],
                [Edge([0, 1], features=[-2]), Edge([0, 2], features=[3]), Edge([0, 3], features=[4], is_directed=True), Edge([3, 2], features=[1], is_directed=True), Edge([2, 4], features=[10])],
                targets={'a': 12.34}
            ),
            {},
            Data(
                x=torch.tensor([[0], [1], [3], [-2], [0]], dtype=torch.float),
                edge_index=torch.tensor([[0, 1, 0, 2, 0, 3, 2, 4],
                                         [1, 0, 2, 0, 3, 2, 4, 2]], dtype=torch.long),
                edge_attr=torch.tensor([[-2.], [-2.], [3.], [3.], [4.], [1.], [10.], [10.]], dtype=torch.float),
                y=torch.tensor([12.34], dtype=torch.float),
                num_nodes=5,
                graph_attr=torch.tensor([], dtype=torch.float),
                id=None
            )
        ],

        [
            Graph(
                [Node(features=[0]), Node(features=[1]), Node(features=[3]), Node(features=[-2]), Node(features=[0])],
                [Edge([0, 1], features={'test_feature': 'A'}), Edge([0, 2], features={'test_feature': 'B'}), Edge([0, 3], features={'test_feature': 'A'}, is_directed=True), Edge([3, 2], features={'test_feature': 'C'}, is_directed=True), Edge([2, 4], features={'test_feature': 'D'})],
                targets={'a': 12.34}, graph_features={'gr': 1.35}, meta_data={'id': 'test-id'}
            ),
            {'test_feature': ['B', 'A', 'C', 'D']},
            Data(
                x=torch.tensor([[0], [1], [3], [-2], [0]], dtype=torch.float),
                edge_index=torch.tensor([[0, 1, 0, 2, 0, 3, 2, 4],
                                         [1, 0, 2, 0, 3, 2, 4, 2]], dtype=torch.long),
                edge_attr=torch.tensor([[0, 1, 0, 0], [0, 1, 0, 0], [1, 0, 0, 0], [1, 0, 0, 0], [0, 1, 0, 0], [0, 0, 1, 0], [0, 0, 0, 1], [0, 0, 0, 1]], dtype=torch.float),
                y=torch.tensor([12.34], dtype=torch.float),
                num_nodes=5,
                graph_attr=torch.tensor([1.35], dtype=torch.float),
                id="test-id"
            )
        ],

    ])
    def test_get_pytorch_data_object(self, graph, edge_class_feature_dict, expected):

        result = graph.get_pytorch_data_object(edge_class_feature_dict=edge_class_feature_dict)
        self.assertEqual(len(result.keys), len(expected.keys))

        for key in result.keys:
            if key == 'num_nodes' or key == 'id':
                self.assertTrue(result[key] == expected[key])
            else:
                self.assertTrue(torch.equal(result[key], expected[key]))

    @parameterized.expand([

        [
            Graph([Node(features=[0], position=[0, 1]), Node(features=[0], position=[2, 3]), Node(features=[0], position=[4, 7]),
                   Node(features=[0], position=[9, 0]), Node(features=[0], position=[2, 1])], []),

            {
                0: [0, 1],
                1: [2, 3],
                2: [4, 7],
                3: [9, 0],
                4: [2, 1]
            }
        ],

    ])
    def test_get_node_position_dict(self, graph, expected):

        self.assertEqual(graph.get_node_position_dict(), expected)

    @parameterized.expand([

        [
            Graph([Node(features=[0], label='C'), Node(features=[0], label='H'), Node(features=[0], label='O'),
                   Node(features=[0], label='N'), Node(features=[0], label='S')], []),

            {
                0: 'C',
                1: 'H',
                2: 'O',
                3: 'N',
                4: 'S'
            }
        ],

    ])
    def test_get_node_label_dict(self, graph, expected):

        self.assertEqual(graph.get_node_label_dict(), expected)

    @parameterized.expand([

        [
            Graph(
                [Node(), Node()],
                [Edge([0, 1])],
                targets={}, meta_data={'id': 'TestGraph'}
            ),
            {
                'graph': nx.MultiGraph(),
                'meta_data': {'id': 'TestGraph'},
                'targets': {},
                'nodes': [(0), (1)],
                'edges': [(0, 1)]
            },
        ],

        [
            Graph(
                [Node(features=[0, 1]), Node(features=[1, 0])],
                [Edge([0, 1], features=[-2, 2])],
                targets={'a': 12.34, 'b': 23.45, 'c': 34.56}, meta_data={'id': 'TestGraph'}
            ),
            {
                'graph': nx.MultiGraph(),
                'meta_data': {'id': 'TestGraph'},
                'targets': {'target_a': 12.34, 'target_b': 23.45, 'target_c': 34.56},
                'nodes': [(0, {'feature_0': 0, 'feature_1': 1}), (1, {'feature_0': 1, 'feature_1': 0})],
                'edges': [(0, 1, {'feature_0': -2, 'feature_1': 2})]
            },
        ],

        [
            Graph(
                [Node(features=[0, 1]), Node(features=[1, 0])],
                [Edge([0, 1], features=[-2, 2], is_directed=True)],
                targets={'a': 12.34, 'b': 23.45, 'c': 34.56}, meta_data={'id': 'TestGraph'}
            ),
            {
                'graph': nx.MultiDiGraph(),
                'meta_data': {'id': 'TestGraph'},
                'targets': {'target_a': 12.34, 'target_b': 23.45, 'target_c': 34.56},
                'nodes': [(0, {'feature_0': 0, 'feature_1': 1}), (1, {'feature_0': 1, 'feature_1': 0})],
                'edges': [(0, 1, {'feature_0': -2, 'feature_1': 2})]
            },
        ],

        [
            Graph(
                [Node(features=[0, 1], position=[0, 1, 2], label='A'), Node(features=[1, 0], position=[3, 4, 5], label='B')],
                [Edge([0, 1], features=[-2, 2], is_directed=True)],
                targets={'a': 12.34, 'b': 23.45, 'c': 34.56}, meta_data={'id': 'TestGraph', 'some_meta_info': 123}
            ),
            {
                'graph': nx.MultiDiGraph(),
                'meta_data': {'id': 'TestGraph', 'some_meta_info': 123},
                'targets': {'target_a': 12.34, 'target_b': 23.45, 'target_c': 34.56},
                'nodes': [(0, {'feature_0': 0, 'feature_1': 1, 'node_label': 'A', 'node_position': [0, 1, 2]}), (1, {'feature_0': 1, 'feature_1': 0, 'node_label': 'B', 'node_position': [3, 4, 5]})],
                'edges': [(0, 1, {'feature_0': -2, 'feature_1': 2})]
            },
        ],

    ])
    def test_get_networkx_graph_object(self, graph, expected):

        # setup expected graph
        expected_graph = expected['graph']

        expected_graph.graph['meta_data'] = expected['meta_data']

        if not expected['targets'] == {}:
            for key in expected['targets'].keys():
                expected_graph.graph[key] = expected['targets'][key]
        expected_graph.add_nodes_from(expected['nodes'])
        expected_graph.add_edges_from(expected['edges'])

        result: nx.MultiGraph = graph.get_networkx_graph_object()

        Utils.tc.assertEqual(type(result), type(expected_graph))
        Utils.assert_are_almost_equal(result.graph, expected_graph.graph)
        Utils.assert_are_almost_equal(list(result.nodes(data=True)), list(expected_graph.nodes(data=True)))
        Utils.assert_are_almost_equal(list(result.edges(data=True)), list(expected_graph.edges(data=True)))

    @parameterized.expand([

        [
            Graph(
                [Node(), Node(), Node()],
                [Edge([0, 1]), Edge([1, 2], is_directed=True)],
                targets={}
            ),
            NotImplementedError
        ],

    ])
    def test_get_networkx_graph_object_with_invalid_data(self, graph, expected_exception):

        Utils.tc.assertRaises(expected_exception, graph.get_networkx_graph_object)

    @parameterized.expand([

        [
            Graph(
                [Node(features={'node_feature': 1}), Node(features={'node_feature': 2}), Node(features={'node_feature': 3})],
                [Edge([0, 1], features={'edge_feature': 1}), Edge([1, 2], features={'edge_feature': 1})],
                targets={'some_target': 1.2},
                graph_features={'graph_feature': 2, 'graph_feature_1': 'type'},
                meta_data={'id': 'TestGraph'}
            ),
        ],

        [
            Graph(
                [Node(label='A', position=[0, 1, 2]), Node(label='B', position=[3, 4, 5]), Node(label='C', position=[6, 7, 8])],
                [Edge([0, 1]), Edge([1, 2])],
                targets={}, meta_data={'id': 'TestGraph'}
            ),
        ],

        [
            Graph(
                [Node(), Node(), Node()],
                [Edge([0, 1]), Edge([1, 2])],
                targets={}, meta_data={'id': 'TestGraph'}
            ),
        ],

        [
            Graph(
                [Node(), Node(), Node()],
                [Edge([0, 1], is_directed=True), Edge([1, 2], is_directed=True)],
                targets={}, meta_data={'id': 'TestGraph'}
            ),
        ],

    ])
    def test_from_networkx(self, graph):

        nx_graph = graph.get_networkx_graph_object()
        result = Graph.from_networkx(nx_graph)
        Utils.assert_are_almost_equal(result, graph)
