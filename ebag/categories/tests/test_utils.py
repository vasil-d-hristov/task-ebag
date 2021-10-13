from categories.models import Category
from categories.tests.utils import create_category, create_similarity
from categories.utils import (
    get_category_islands,
    get_category_nodes,
    get_category_parents,
    get_category_siblings,
    get_category_similarities,
    get_category_tree,
)
from django.test import TestCase


def set_relations():
    root_node = create_category(Category.ROOT_NAME)
    categories = [create_category(f'Category {i}') for i in range(1, 9)]
    categories = [root_node] + categories

    # root tree - branch one
    categories[1].parent = categories[0]
    categories[3].parent = categories[1]
    categories[5].parent = categories[3]
    categories[7].parent = categories[3]
    # root tree - branch two
    categories[2].parent = categories[0]
    categories[4].parent = categories[2]
    categories[6].parent = categories[4]
    categories[8].parent = categories[2]

    for it in categories:
        it.save()

    # similarities
    create_similarity(categories[1], categories[2])
    create_similarity(categories[1], categories[4])
    create_similarity(categories[3], categories[5])
    create_similarity(categories[5], categories[2])
    create_similarity(categories[4], categories[6])
    create_similarity(categories[6], categories[7])
    create_similarity(categories[7], categories[8])
    create_similarity(categories[8], categories[1])

    return categories


class GetCategoryNodesTests(TestCase):

    @classmethod
    def setUpTestData(cls):
        cls.categories = set_relations()

    def test_get_category_nodes_from_node_0(self):
        calculated = get_category_nodes(self.categories[0])
        expected = [self.categories[1], self.categories[2]]
        self.assertQuerysetEqual(calculated, expected, ordered=False)

    def test_get_category_nodes_from_node_1(self):
        calculated = get_category_nodes(self.categories[1])
        expected = [self.categories[3]]
        self.assertQuerysetEqual(calculated, expected, ordered=False)

    def test_get_category_nodes_from_node_2(self):
        calculated = get_category_nodes(self.categories[2])
        expected = [self.categories[4], self.categories[8]]
        self.assertQuerysetEqual(calculated, expected, ordered=False)

    def test_get_category_nodes_from_node_3(self):
        calculated = get_category_nodes(self.categories[3])
        expected = [self.categories[5], self.categories[7]]
        self.assertQuerysetEqual(calculated, expected, ordered=False)

    def test_get_category_nodes_from_node_4(self):
        calculated = get_category_nodes(self.categories[4])
        expected = [self.categories[6]]
        self.assertQuerysetEqual(calculated, expected, ordered=False)

    def test_get_category_nodes_from_node_5(self):
        calculated = get_category_nodes(self.categories[5])
        expected = []
        self.assertQuerysetEqual(calculated, expected, ordered=False)

    def test_get_category_nodes_from_node_6(self):
        calculated = get_category_nodes(self.categories[6])
        expected = []
        self.assertQuerysetEqual(calculated, expected, ordered=False)

    def test_get_category_nodes_from_node_7(self):
        calculated = get_category_nodes(self.categories[7])
        expected = []
        self.assertQuerysetEqual(calculated, expected, ordered=False)

    def test_get_category_nodes_from_node_8(self):
        calculated = get_category_nodes(self.categories[8])
        expected = []
        self.assertQuerysetEqual(calculated, expected, ordered=False)


class GetCategoryParentsTests(TestCase):

    @classmethod
    def setUpTestData(cls):
        cls.categories = set_relations()

    def test_get_category_parents_from_node_0(self):
        calculated = get_category_parents(self.categories[0])
        expected = []
        self.assertEqual(calculated, expected)

    def test_get_category_parents_from_node_1(self):
        calculated = get_category_parents(self.categories[1])
        expected = [self.categories[0]]
        self.assertEqual(calculated, expected)

    def test_get_category_parents_from_node_2(self):
        calculated = get_category_parents(self.categories[2])
        expected = [self.categories[0]]
        self.assertEqual(calculated, expected)

    def test_get_category_parents_from_node_3(self):
        calculated = get_category_parents(self.categories[3])
        expected = [self.categories[0], self.categories[1]]
        self.assertEqual(calculated, expected)

    def test_get_category_parents_from_node_4(self):
        calculated = get_category_parents(self.categories[4])
        expected = [self.categories[0], self.categories[2]]
        self.assertEqual(calculated, expected)

    def test_get_category_parents_from_node_5(self):
        calculated = get_category_parents(self.categories[5])
        expected = [self.categories[0], self.categories[1], self.categories[3]]
        self.assertEqual(calculated, expected)

    def test_get_category_parents_from_node_6(self):
        calculated = get_category_parents(self.categories[6])
        expected = [self.categories[0], self.categories[2], self.categories[4]]
        self.assertEqual(calculated, expected)

    def test_get_category_parents_from_node_7(self):
        calculated = get_category_parents(self.categories[7])
        expected = [self.categories[0], self.categories[1], self.categories[3]]
        self.assertEqual(calculated, expected)

    def test_get_category_parents_from_node_8(self):
        calculated = get_category_parents(self.categories[8])
        expected = [self.categories[0], self.categories[2]]
        self.assertEqual(calculated, expected)


class GetCategorySiblingsTests(TestCase):

    @classmethod
    def setUpTestData(cls):
        cls.categories = set_relations()

    def test_get_category_siblings_from_node_0(self):
        calculated = get_category_siblings(self.categories[0])
        expected = []
        self.assertQuerysetEqual(calculated, expected, ordered=False)

    def test_get_category_siblings_from_node_1(self):
        calculated = get_category_siblings(self.categories[1])
        expected = [self.categories[2]]
        self.assertQuerysetEqual(calculated, expected, ordered=False)

    def test_get_category_siblings_from_node_2(self):
        calculated = get_category_siblings(self.categories[2])
        expected = [self.categories[1]]
        self.assertQuerysetEqual(calculated, expected, ordered=False)

    def test_get_category_siblings_from_node_3(self):
        calculated = get_category_siblings(self.categories[3])
        expected = []
        self.assertQuerysetEqual(calculated, expected, ordered=False)

    def test_get_category_siblings_from_node_4(self):
        calculated = get_category_siblings(self.categories[4])
        expected = [self.categories[8]]
        self.assertQuerysetEqual(calculated, expected, ordered=False)

    def test_get_category_siblings_from_node_5(self):
        calculated = get_category_siblings(self.categories[5])
        expected = [self.categories[7]]
        self.assertQuerysetEqual(calculated, expected, ordered=False)

    def test_get_category_siblings_from_node_6(self):
        calculated = get_category_siblings(self.categories[6])
        expected = []
        self.assertQuerysetEqual(calculated, expected, ordered=False)

    def test_get_category_siblings_from_node_7(self):
        calculated = get_category_siblings(self.categories[7])
        expected = [self.categories[5]]
        self.assertQuerysetEqual(calculated, expected, ordered=False)

    def test_get_category_siblings_from_node_8(self):
        calculated = get_category_siblings(self.categories[8])
        expected = [self.categories[4]]
        self.assertQuerysetEqual(calculated, expected, ordered=False)


class GetCategorySimilaritiesTests(TestCase):

    @classmethod
    def setUpTestData(cls):
        cls.categories = set_relations()

    def test_get_category_similarities_from_node_0(self):
        calculated = get_category_similarities(self.categories[0])
        calculated = list(map(lambda it: it[0], calculated))
        expected = []
        self.assertQuerysetEqual(calculated, expected, ordered=False)

    def test_get_category_similarities_from_node_1(self):
        calculated = get_category_similarities(self.categories[1])
        calculated = list(map(lambda it: it[0], calculated))
        expected = [self.categories[2], self.categories[4], self.categories[8]]
        self.assertQuerysetEqual(calculated, expected, ordered=False)

    def test_get_category_similarities_from_node_2(self):
        calculated = get_category_similarities(self.categories[2])
        calculated = list(map(lambda it: it[0], calculated))
        expected = [self.categories[1], self.categories[5]]
        self.assertQuerysetEqual(calculated, expected, ordered=False)

    def test_get_category_similarities_from_node_3(self):
        calculated = get_category_similarities(self.categories[3])
        calculated = list(map(lambda it: it[0], calculated))
        expected = [self.categories[5]]
        self.assertQuerysetEqual(calculated, expected, ordered=False)

    def test_get_category_similarities_from_node_4(self):
        calculated = get_category_similarities(self.categories[4])
        calculated = list(map(lambda it: it[0], calculated))
        expected = [self.categories[1], self.categories[6]]
        self.assertQuerysetEqual(calculated, expected, ordered=False)

    def test_get_category_similarities_from_node_5(self):
        calculated = get_category_similarities(self.categories[5])
        calculated = list(map(lambda it: it[0], calculated))
        expected = [self.categories[2], self.categories[3]]
        self.assertQuerysetEqual(calculated, expected, ordered=False)

    def test_get_category_similarities_from_node_6(self):
        calculated = get_category_similarities(self.categories[6])
        calculated = list(map(lambda it: it[0], calculated))
        expected = [self.categories[4], self.categories[7]]
        self.assertQuerysetEqual(calculated, expected, ordered=False)

    def test_get_category_similarities_from_node_7(self):
        calculated = get_category_similarities(self.categories[7])
        calculated = list(map(lambda it: it[0], calculated))
        expected = [self.categories[8], self.categories[6]]
        self.assertQuerysetEqual(calculated, expected, ordered=False)

    def test_get_category_similarities_from_node_8(self):
        calculated = get_category_similarities(self.categories[8])
        calculated = list(map(lambda it: it[0], calculated))
        expected = [self.categories[1], self.categories[7]]
        self.assertQuerysetEqual(calculated, expected, ordered=False)


class CategoryTreeBehaviorTests(TestCase):

    def setUp(self):
        root_node = create_category(Category.ROOT_NAME)
        categories = [create_category(f'Category {i}', root_node) for i in range(1, 6)]
        self.categories = [root_node] + categories

    def test_behavior_category_tree_initial(self):
        calculated = get_category_tree(self.categories[0], 'by_name')
        expected = {
            self.categories[0].name: {
                self.categories[1].name: {},
                self.categories[2].name: {},
                self.categories[3].name: {},
                self.categories[4].name: {},
                self.categories[5].name: {},
            },
        }
        self.assertEqual(calculated, expected)

    def test_behavior_category_tree_changed(self):
        # change one
        self.categories[5].parent = self.categories[3]
        self.categories[4].parent = self.categories[2]
        self.categories[3].parent = self.categories[1]

        for it in self.categories:
            it.save()

        calculated = get_category_tree(self.categories[0], 'by_name')
        expected = {
            self.categories[0].name: {
                self.categories[1].name: {
                    self.categories[3].name: {
                        self.categories[5].name: {},
                    },
                },
                self.categories[2].name: {
                    self.categories[4].name: {},
                },
            },
        }
        self.assertEqual(calculated, expected)

        # change two
        self.categories[3].parent = self.categories[4]
        self.categories[2].parent = self.categories[1]

        for it in self.categories:
            it.save()

        calculated = get_category_tree(self.categories[0], 'by_name')
        expected = {
            self.categories[0].name: {
                self.categories[1].name: {
                    self.categories[2].name: {
                        self.categories[4].name: {
                            self.categories[3].name: {
                                self.categories[5].name: {},
                            },
                        },
                    },
                },
            },
        }
        self.assertEqual(calculated, expected)


class CategoryIslandsBehaviorTests(TestCase):

    def setUp(self):
        root_node = create_category(Category.ROOT_NAME)
        categories = [create_category(f'Category {i}', root_node) for i in range(1, 6)]
        self.categories = [root_node] + categories

    def test_behavior_category_islands_initial(self):
        calculated = get_category_islands(self.categories[0], 'by_name')
        expected = [
            [self.categories[1].name],
            [self.categories[2].name],
            [self.categories[3].name],
            [self.categories[4].name],
            [self.categories[5].name],
        ]
        self.assertEqual(calculated, expected)

    def test_behavior_category_islands_changed(self):
        # change one
        create_similarity(self.categories[1], self.categories[2])
        create_similarity(self.categories[3], self.categories[4])
        create_similarity(self.categories[4], self.categories[5])

        calculated = get_category_islands(self.categories[0], 'by_name')
        expected = [
            [
                self.categories[1].name,
                self.categories[2].name,
            ],
            [
                self.categories[3].name,
                self.categories[4].name,
                self.categories[5].name,
            ],
        ]
        self.assertEqual(calculated, expected)

        # change two
        create_similarity(self.categories[1], self.categories[5])

        calculated = get_category_islands(self.categories[0], 'by_name')
        expected = [
            [
                self.categories[1].name,
                self.categories[2].name,
                self.categories[3].name,
                self.categories[4].name,
                self.categories[5].name,
            ],
        ]
        self.assertEqual(calculated, expected)
