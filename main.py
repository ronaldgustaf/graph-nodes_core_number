from collections import defaultdict
import networkx as nx

import time

# Create classes for doubly linked list (own_method)
class Node:
    def __init__(self, value):
        self.value = value
        self.prev = None
        self.next = None

class DoublyLinkedList:
    def __init__(self):
        self.head = Node(None)
        self.tail = Node(None)
        self.head.next = self.tail
        self.tail.prev = self.head
        self.nodes = {}
    
    def add_node(self, node):
        new_node = Node(node)
        new_node.next = self.tail
        new_node.prev = self.tail.prev
        self.tail.prev.next = new_node
        self.tail.prev = new_node
        self.nodes[node] = new_node
    
    def remove_node(self, node):
        if node.value is None:
            return
        node.prev.next = node.next
        node.next.prev = node.prev
    
    def is_empty(self):
        return self.head.next == self.tail

    def find_node(self, value):
        return self.nodes.get(value, None)
    
def own_core_numbers(filename):
    # Read the graph from file and construct a dictionary of adjacency lists
    adj_list = defaultdict(list)
    with open(filename, 'r') as file:
        for line in file:
            if line.startswith('# Nodes') or line.startswith('# FromNodeId'):
                continue
            else:
                u, v = map(int, line.strip().split())
                adj_list[u].append(v)
                adj_list[v].append(u)

    # Initialize the degree of each node to be the number of its neighbors
    degrees = {node: len(adj_list[node]) for node in adj_list}
    # Create degree list of doubly linked lists to store the degree lists
    degree_lists = [DoublyLinkedList() for _ in range(max(degrees.values())+1)]
    # Add each node to the doubly linked lists according to he number of degree
    for node, degree in degrees.items():
        degree_lists[degree].add_node(node)
    
    # Initialize core numbers dict to store the result
    core_numbers = {}
    k = 1
    # Iterate over the degree lists and remove nodes until all nodes have degree < k
    while degree_lists:
        # Conditions to increase k
        while k < len(degree_lists) and degree_lists[k].is_empty():
            k += 1
        # Condition to end the loop
        if k == len(degree_lists):
            break
        # Find all nodes u in G with degree <= k
        node = degree_lists[k].head.next
        # Remove node u from the graph
        degree_lists[k].remove_node(node)
        # Update the degree of its neighbors and move them to the correct degree list
        for neighbor in adj_list[node.value]:
            if degrees[neighbor] > k:
                neighbor_node = degree_lists[degrees[neighbor]].find_node(neighbor)
                # Remove neighbor from original degree list
                degree_lists[degrees[neighbor]].remove_node(neighbor_node)
                # Decrease neighbor's degree by 1
                degrees[neighbor] -= 1
                # Add neighbor to updated degree list
                degree_lists[degrees[neighbor]].add_node(neighbor)
        # Set the core number of the node u as k
        core_numbers[node.value] = k
    # Sort the result based on nodes for comparing with networkx result
    core_numbers = dict(sorted(core_numbers.items()))

    return core_numbers

def networkx_core_numbers(filename):
    # Read the graph from file and construct a networkx graph object
    G = nx.Graph()
    with open(filename, 'r') as file:
        for line in file:
            if line.startswith('# Nodes') or line.startswith('# FromNodeId'):
                continue
            else:
                u, v = map(int, line.strip().split())
                G.add_edge(u, v)

    # Compute the core numbers by calling core_number function from the library
    core_numbers = nx.core_number(G)

    return core_numbers

if __name__ == '__main__':
    filename = 'data.txt'

    # Compute core numbers using own method
    print("========= Own Method =========")
    start_time = time.time()

    own_core_numbers = own_core_numbers(filename)
    # Output the result to a txt file
    with open("result_own.txt", "w") as f:
        for node, core_number in own_core_numbers.items():
            f.write(f"{node}: {core_number}\n") 
    
    duration = time.time() - start_time
    print(f"Total Duration Own: {duration: 4f} s")

    # Compute core numbers using networkx library
    print("========= NetworkX Method =========")
    start_time = time.time()

    networkx_core_numbers = networkx_core_numbers(filename)
    # Output the result to a txt file
    with open("result_networkx.txt", "w") as f:
        for node, core_number in networkx_core_numbers.items():
            f.write(f"{node}: {core_number}\n") 
    
    duration = time.time() - start_time
    print(f"Total Duration NetworkX: {duration: 4f} s")

    # Check if result is the same
    import filecmp
    import os

    def compare_files(file1, file2):
        compare = filecmp.cmp(file1,file2)

        if compare == True:
            print("SAME")
        else:
            print("DIFFERENT")

    compare_files('result_own.txt', 'result_networkx.txt')