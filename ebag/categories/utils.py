import json

from categories.models import Category, Similarity


class Graph:
    """
    Python program to print connected
    components in an undirected graph
    """

    def __init__(self, vertex):
        self.vertex = vertex
        self.matrix = [[] * i for i in range(vertex)]

    def add_edge(self, x, y):
        self.matrix[x].append(y)
        self.matrix[y].append(x)

    def dfs_util(self, temporary, vertex, visited):
        visited[vertex] = True
        temporary.append(vertex)
        for i in self.matrix[vertex]:
            if not visited[i]:
                temporary = self.dfs_util(temporary, i, visited)
        return temporary

    def connected_components(self):
        visited = []
        connected = []
        for i in range(self.vertex):
            visited.append(False)
        for vertex in range(self.vertex):
            if not visited[vertex]:
                temporary = []
                connected.append(self.dfs_util(temporary, vertex, visited))
        return connected


def get_category_islands(node, by_type):
    indexes = []
    for category in Category.objects.exclude(name=Category.ROOT_NAME):
        indexes.append(node_to_string(category, by_type))

    graph = Graph(len(indexes))

    for similarity in Similarity.objects.select_related().all():
        graph.add_edge(
            indexes.index(node_to_string(similarity.node_one, by_type)),
            indexes.index(node_to_string(similarity.node_two, by_type)),
        )

    category_islands = graph.connected_components()

    for island in range(len(category_islands)):
        for category in range(len(category_islands[island])):
            index = category_islands[island][category]
            category_islands[island][category] = indexes[index]
        category_islands[island].sort()

    category_islands.sort()

    if node.name != Category.ROOT_NAME:
        category_islands = list(filter(lambda it: node_to_string(node, by_type) in it, category_islands))

    return category_islands


def get_category_islands_to_string(node):
    category_islands = get_category_islands(node, 'by_link')
    category_islands = json.dumps(category_islands, indent=4)
    category_islands = category_islands.replace(' ' * 4, '&nbsp;' * 4)
    category_islands = category_islands.replace('"', '').replace(',', '')

    return category_islands


def get_category_nodes(node):
    return list(node.sub_categories.all())


def get_category_parents(node):
    parents = []
    while node.parent:
        parents.append(node.parent)
        node = node.parent
    return parents[::-1]


def get_category_siblings(node):
    if node.parent:
        return list(Category.objects.filter(parent=node.parent.id).exclude(id=node.id))
    return []


def get_category_similarities(node):
    list_one = list(map(lambda it: (it.node_two, it), node.related_node_one.all()))
    list_two = list(map(lambda it: (it.node_one, it), node.related_node_two.all()))
    # return list(
    #     Category.objects.filter(
    #         Q(related_node_one__node_two=node) | Q(related_node_two__node_one=node)
    #     ).distinct()
    # )
    return list_one + list_two


def get_category_tree(node, by_type):
    def get_next_depth(inner, level):
        key = node_to_string(inner, by_type)
        tree = {key: {}}
        for child in Category.objects.filter(parent=inner.id):
            tree[key].update(get_next_depth(child, level + 1))
        return tree

    return get_next_depth(node, 0)


def get_category_tree_nodes(node):
    def get_next_depth(inner, level):
        nodes = {inner.id}
        for child in Category.objects.filter(parent=inner.id):
            nodes.update(get_next_depth(child, level + 1))
        return nodes

    return get_next_depth(node, 0)


def get_category_tree_to_string(node):
    category_tree = get_category_tree(node, 'by_link')
    category_tree = json.dumps(category_tree, sort_keys=True, indent=4)
    category_tree = category_tree.replace(': {}', '').replace(' ' * 4, '&nbsp;' * 4)
    category_tree = category_tree.replace('"', '').replace(',', '')

    return category_tree


def node_to_string(node, by_type):
    if by_type == 'by_name':
        return node.name
    elif by_type == 'by_link':
        return f"<a href='{node.get_absolute_url()}'>{node.name}</a>"
