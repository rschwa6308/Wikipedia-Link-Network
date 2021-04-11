# class Node:
#     def __init__(self, value, children):
#         self.value = value
#         self.children = children


class DiGraph:
    def __init__(self):
        self.nodes = {}

    def add_node(self, node):
        if node not in self.nodes:
            self.nodes[node] = set()

    def add_link(self, a, b):
        self.nodes[a].add(b)

    def entry_to_line(self, node):
        return f"{node}: " + ", ".join(sorted(self.nodes[node]))

    def write_to_file(self, filename):
        with open(filename, "w") as file:
            for node in sorted(self.nodes):
                file.write(self.entry_to_line(node) + "\n")

    def write_node_to_file(self, file, node):
        file.write(self.entry_to_line(node) + "\n")

    def read_from_filename(self, filename):
        with open(filename, "r", encoding="utf-8") as file:
            for line in file.readlines():
                # print(line)
                node, tail = line.split(": ")
                links = tail.split(", ")
                if node in self.nodes: continue
                self.add_node(node)
                for link in links:
                    self.add_link(node, link.rstrip())

    def get_to_traverse(self):
        all_values = set().union(*self.nodes.values())

        return {value for value in all_values if value not in self.nodes}

    def shortest_path(self, o1, o2):
        ret = []

        queued = set()
        queue = [o1]

        back_links = {}

        while queue:
            next_node = queue.pop(0)

            # visited.add(next_node)

            if next_node == o2:
                cur = next_node
                while cur != o1:
                    ret.append(cur)
                    cur = back_links[cur]
                ret.append(o1)
                return ret[::-1]

            children = list(self.nodes[next_node])
            for c in children:
                if c not in self.nodes: continue
                if c in queued: continue
                back_links[c] = next_node
                queue.append(c)
                queued.add(c)
        return None


